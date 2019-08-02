import configparser
import logging
import pandas as pd
import requests
import time


def main():
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

    config = configparser.ConfigParser()
    config.read('configuration.conf')

    # Parse config file and store values
    csv_path = config['Folders']['csv_path']
    api_key = config['VirusTotal']['api_key']
    label_file = config['Folders']['Labels']

    malwares = pd.read_csv(csv_path, index_col=0)       # Read in csv file

    url = 'https://www.virustotal.com/vtapi/v2/file/report'     # API endpoint
    count = 0       # Number of reports retrieved

    length = len(malwares[(malwares["scanned"] == True) & (malwares["retrieved"] == False)])        # Number of reports that need to be received
    logging.info(f'{length} files must be retrieved...')
    logging.info(f'Estimated time: {length / 4} minutes')

    while length > 0:       # Condition ensures that files that were initially still being scanned are still retrieved
        for md5_hash in malwares[(malwares["scanned"] == True) & (malwares["retrieved"] == False)].index:
            params = {'apikey': api_key, 'resource': md5_hash}

            try:
                response = requests.get(url, params=params)
            except requests.exceptions.SSLError:
                logging.error(f'Error connecting with VirusTotal on file {md5_hash}')
                malwares.to_csv(csv_path)  # Export progress
                raise requests.exceptions.SSLError

            if response.status_code == 200 and response.json()['response_code'] == 1:       # Scan has finished; get report
                malwares.loc[md5_hash, 'scan_results'] = response.json()['positives']        # Number of detections for sample
                malwares.loc[md5_hash, 'retrieved'] = True      # Sample's report has been retrieved
                count = count + 1  # Another report retrieved

                with open(label_file, 'a') as f:        # Export detected labels
                    for scan in response.json()['scans']:
                        if response.json()['scans'][scan]['detected']:
                            f.write("%s\n" % response.json()['scans'][scan]['result'])

                length = length - 1     # One fewer report that needs retrieval
            elif response.status_code == 200 and response.json()['response_code'] == -2:        # Scan is ongoing
                logging.warning(f'{md5_hash} is still being scanned')
            else:       # Error with retrieving file
                logging.error(f"Error with file {md5_hash}")
                malwares.to_csv(csv_path)       # Export progress

            logging.info(f'{count} files have been retrieved; {length} files remaining')
            time.sleep(15)      # API requests limited to 4 per minute

    malwares.to_csv(csv_path)


if __name__ == "__main__":
    main()
