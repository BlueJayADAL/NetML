import configparser
import logging
import pandas as pd


def main():
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

    config = configparser.ConfigParser()
    config.read('configuration.conf')

    # Parse config file and store values
    csv_path = config['Folders']['csv_path']

    malwares = pd.read_csv(csv_path, index_col=0)       # Read in csv file
    logging.info('CSV file imported...')
    n_analyzed = 0
    n_pcap = 0

    file_list = malwares[(malwares['scan_results'] >= 10) & (malwares['analyzed'] == False)].index
    for md5_hash in get_next_file(file_list):     # Only analyze files with >10 detections
        logging.info(f'Currently analyzing file: {md5_hash}')

        submitted = input(f'Has {md5_hash} been submitted?')
        if submitted == 'y':
            n_analyzed = n_analyzed + 1
            malwares.loc[md5_hash, 'analyzed'] = True
        else:
            logging.info(f'Error submitting file {md5_hash}...')
            logging.info('Exporting to csv...')
            malwares.to_csv(csv_path)
            return

        pcap = input(f'Did {md5_hash} produce a pcap file?')
        if pcap == 'y':
            n_pcap = n_pcap + 1
            malwares.loc[md5_hash, 'pcap_success'] = True

    logging.info('Exporting to csv...')
    malwares.to_csv(csv_path)


def get_next_file(file_list):
    for md5_hash in file_list:
        if input('Continue analysis?') == 'y':
            yield md5_hash
        else:
            logging.info('Exiting...')
            return


if __name__ == "__main__":
    main()
