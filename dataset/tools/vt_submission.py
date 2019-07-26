import configparser
import logging
import pandas as pd
import time
import requests


def main():
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

    config = configparser.ConfigParser()
    config.read('configuration.conf')

    # Parse config file and store values
    csv_path = config['Folders']['csv_path']
    api_key = config['VirusTotal']['api_key']
    malware_folder = config['Folders']['malware_folder']

    malwares = pd.read_csv(csv_path, index_col=0)       # Open csv file

    count = 0       # Number of files submitted
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'       # API endpoint
    params = {'apikey': api_key}

    length = len(malwares[malwares["scanned"] == False])        # Number of files that must be submitted
    logging.info(f'{length} files must be scanned...')
    logging.info(f'Estimated time: {length / 4} minutes')

    for md5_hash in malwares[malwares['scanned'] == False].index:       # Only submit samples that have not been previously submitted
        file_path = malware_folder + f'/{md5_hash}'
        files = {'file': (file_path, open(file_path, 'rb'))}
        try:
            response = requests.post(url, files=files, params=params)       # Submit sample using API endpoint and get response
            if response.status_code == 200:  # Successful submission
                count = count + 1  # Another file has been scanned
                logging.info(f'{count} files have been submitted; {length - count} files remaining')
                malwares.loc[md5_hash, 'scanned'] = True  # Sample has been submitted
            else:  # Error with submission (ex. incorrect API key)
                logging.error(f"PROBLEM SUBMITTING {md5_hash} FOR SCAN.  MAY WANT TO RUN AGAIN")
                malwares.to_csv()  # Save submission status of files
        except:
            logging.error(f'PROBLEM POSTING {md5_hash} FOR SCAN.  VIRUSTOTAL WILL NOT ACCEPT.  DROPPING SAMPLE...')
            malwares.drop(index = md5_hash, inplace = True)
            malwares.to_csv()  # Save submission status of files

        time.sleep(15)      # API requests limited to four per minute

    malwares.to_csv(csv_path)       # Export csv file


if __name__ == "__main__":
    main()
