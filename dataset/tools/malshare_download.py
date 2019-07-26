import configparser
import requests
import pandas as pd
import logging
from os import listdir
import hashlib
import numpy as np
import datetime

BLOCK_SIZE = 65536


def main():
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

    config = configparser.ConfigParser()
    config.read('configuration.conf')

    # Parse config file and store values
    run_type = int(config['MalShare']['run_type'])
    api_key = config['MalShare']['api_key']
    malware_folder = config['Folders']['malware_folder']
    csv_path = config['Folders']['csv_path']
    file_type = config['MalShare']['file_type']

    limit = get_api_limit(api_key)  # API requests remaining (1000 per day)
    if limit == -1:
        logging.error("UNABLE TO RETRIEVE API LIMIT.  MAKE SURE YOUR API KEY IS ENTERED CORRECTLY.")
        return
    elif limit <= 0:
        logging.error("OVER DAILY API LIMIT")
        return
    else:
        logging.info(f'{limit} API requests remaining')  # Display number of API requests remaining

    limit = limit - 1  # One API request has already been used to get number of remaining requests
    if run_type == 0:
        logging.info("Creating new CSV file...")
        new_malwares = update_csv(api_key, file_type)
    elif run_type == 1:     # Using existing csv file
        logging.info("Reading from existing csv file...")
        malwares = pd.read_csv(csv_path, index_col=0)  # Open csv file and store in DataFrame
        new_malwares = update_csv(api_key, file_type, malwares)
    else:
        logging.error(f'ERROR: INVALID RUNTYPE {run_type}')
        return

    n_downloads = min(len(new_malwares), limit)     # Number of files to be downloaded
    if n_downloads != len(new_malwares):        # More files to download than API requests remaining
        logging.warning(f'WARNING: Only {n_downloads} files out of {len(new_malwares)} will be downloaded.')
    else:
        logging.info(f'{n_downloads} files will be downloaded')

    files = (file_name for i, file_name in enumerate(new_malwares.index) if i < n_downloads)
    for file_name in files:
        logging.info(f'Downloading {file_name}...')
        download_files(api_key, file_name, malware_folder)

    if run_type == 1:
        logging.info("Appending new file names to existing csv...")
        new_malwares = malwares.append(new_malwares)  # Append new DataFrame to existing

    # Check each downloaded file to make sure its md5 hash matches its name (since MalShare labels each sample with its
    # md5 hash)
    file_names = listdir(malware_folder)  # Get all file names in malware sample directory
    for name in file_names:
        if check_hash(name, malware_folder) == -1:  # Something has gone wrong with the download.  Return without saving
            logging.error(f'{name} does not match given hash')
            return

    logging.info('Exporting to CSV...')
    new_malwares.to_csv(csv_path)  # Export csv file


def get_api_limit(key):
    """
    Get the number of MalShare API requests remaining for the day.  If the daily limit is exceeded, every downloaded
    file will be an error message.
    :param key: MalShare API key
    :return: number of daily API requests remaining or error code
    """

    url = f'https://malshare.com/api.php?api_key={key}&action=getlimit'  # API endpoint
    response = requests.get(url)

    return int(response.json()['REMAINING']) if response.status_code == 200 else -1


def update_csv(api_key, file_type, malwares=None):
    """
    Create or update csv file with records for each downloaded sample.
    :param api_key: MalShare API key
    :param file_type: type of files to be downloaded (ex. pe32)
    :param malwares: existing malware DataFrame
    :return: new DataFrame with records for each new sample
    """
    url = f'https://malshare.com/api.php?api_key={api_key}&action=type&type={file_type}'  # API endpoint
    response = requests.get(url)
    daily_digest = response.json()  # JSON response that contains name of each file

    if malwares is None:
        new_files = [item['md5'] for item in daily_digest]  # List for storing these new file names
    else:
        new_files = [item['md5'] for item in daily_digest if
                     item['md5'] not in malwares.index]  # Check that file is not already represented in dataset

    new_malwares = pd.DataFrame(index=new_files)  # Create DataFrame using new file names as index
    new_malwares['scanned'] = False  # Has sample been scanned by VirusTotal?
    new_malwares['retrieved'] = False  # Has sample been retrieved from VirusTotal?
    new_malwares['scan_results'] = np.nan  # Number of detections from VirusTotal
    new_malwares['analyzed'] = False  # Has the sample been analyzed on any.run?
    new_malwares['pcap_success'] = False  # Did the sample produce a pcap file?
    new_malwares['download_date'] = datetime.date.today()       # Put timestamp on download
    new_malwares['file_type'] = file_type       # Record file type

    return new_malwares


def download_files(api_key, file_name, malware_folder):
    """
    Downloads files from MalShare given a file name and destination folder.
    :param api_key: MalShare API key
    :param file_name: name of file to be downloaded.  MalShare uses the sample's md5 hash as its name
    :param malware_folder: folder to which to download sample
    :return: None; download file from MalShare
    """

    url = f'https://malshare.com/api.php?api_key={api_key}&action=getfile&hash={file_name}'
    local_filename = malware_folder + '/' + file_name  # Create path for file download
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:  # Open new file and download
        f.write(r.content)


def check_hash(file_name, malware_folder):
    """
    Check that the md5 hash of a downloaded sample matches the sample's label.  Ensures that downloaded samples have
    been downloaded correctly.
    :param file_name: Name of downloaded sample
    :param malware_folder: Folder into which malware sample was downloaded
    :return: error code 0 (hash matches label) or 1 (hash does not match label)
    """

    md5_hash = md5(file_name, malware_folder)  # Calculate hash of file
    if md5_hash != file_name:  # Return error code
        return -1

    return 0


def md5(f_name, in_file):
    """
    Calculate the md5 hash of a given file.
    :param f_name: Name of file to be hashed
    :param in_file: path to file's directory
    :return: md5 hash of file 'f_name'
    """

    hasher = hashlib.md5()
    with open(in_file + '/' + f_name, "rb") as f:
        buf = f.read(BLOCK_SIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(BLOCK_SIZE)
    return hasher.hexdigest()


if __name__ == "__main__":
    main()
