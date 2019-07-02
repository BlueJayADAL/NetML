# NetML
The NetML project using the Intel Distribution for Python.

## Walkthrough Guide
1. It is recommended to have [Anaconda](https://docs.anaconda.com/anaconda/install/linux/) installed, as this guide will use Anaconda to create a virtual environment with Intel packages (**Python 3**).
2. Install [Joy](https://github.com/cisco/joy) (with "-gzip-enabled") and run it successfully. Refer [here](sampleJoyInstall.md) for sample install steps for Ubuntu system.
    - If `joy` is not automatically added to your system path after installing, you will need to do so manually.
3. Note that the current Joy cannot generate the DNS data correctly when the 'bidir' is enabled which is required by TLS data. In order to fix this issue, please overwrite the current dns.c of Joy with the one in the JoyFix.
4. Have the raw PCAP dataset folder ready. The following is only an example ([CICAndMal2017/PCAPs](https://www.unb.ca/cic/datasets/andmal2017.html)), however our code is currently only tested with such tree structure (Only 1 "Benign" and multiple "ware" folders). Under each folder, it should contain the raw pcap files. Be sure that all folder names only include alphanumeric characters, or errors will arise down the road when the names are parsed (for CICAndMAL2017 rename AndroidSpy277 + FakeAppAL). In order to quickly run through this guide, let's call this ***pathRAW***.
5. Setup Python virtualenv using `conda` to install Intel Python. 
    - Sample Ubuntu [setup](sampleVirtualEnvSetup.md).
    - Official Intel `conda` install [documentatation](https://software.intel.com/en-us/articles/using-intel-distribution-for-python-with-anaconda).
6. Other ways of setting up Intel Distribution for Python can be found on Intel's dedicated [page](https://software.intel.com/en-us/distribution-for-python).
7. Now we will begin processing the data, but first you may want to create a dedicated test output folder, whose path we will refer to as ***pathGen***.
8. Our main script ***daalMaster.py*** provides functionality to streamline the entire data processing to training process by providing the dedicated commands, listed below.
    - -i, --input [INPATH]: Path to input folder containing raw PCAPs (**pathRAW**)
    - -o, --output [OUTPATH]: Output folder for processed files from Cisco Joy (**pathGen**)
    - -j, --joy: Process raw PCAPs and generate output zip files using Cisco Joy
    - -f, --files: Generate output feature JSON files from Joy files
    - -c, --collect: Collect common features of DNS, HTTP, and TLS
    - -s, --selectData: Generate train and test JSON files
    - -t, --train [MODELTYPE]: Train specified model


8. Run the script ***daalMaster.py*** to convert the raw PCAP files into processed zipped files, and further generate JSON files for each feature (DNS, TLS, HTTP and META).
    - For example, `python daalAnalyze.py -i pathRAW -o pathGen`
9. Once it finishes, under the **pathGen**, we can find ***data*** folder which contains all the processed zipped files by Joy, and ***DNS_JSON, TLS_JSON, HTTP_JSON, and META_JSON*** folders which contain the JSON files that represent the corresponding feature of each dataset.
10. Before we train and test the machine learning model, we need to generate a JSON file which contains selected malware and benign datasets using ***daalSelectDataset.py***. 
    - For example, `python daalSelectDataset.py --input pathGen/TLS_JSON/ --output pathGen/train.json --tls` which generates the ***train.json*** file under the **pathGen** folder.
    - The generated JSON files contain only one dataset from each malware and mutiple benign datasets to balance the number of flows. If you want to generate a JSON file which contains all the datasets, please uncomment line 27-29 and modify them accordingly.
11. One last step before we train the model. To ensure we are analyzing the most common features of the dataset, we will need to collect these features to use in the final classification. Running the ***daalCollectCommon\*.py*** scripts will do this for our ***DNS_JSON, TLS_JSON, and HTTP_JSON*** folder data.
    - For example, `python daalCollectCommon<DNS|TLS|HTTP>.py -i pathGen/<DNS|TLS|HTTP>_JSON`
    - The output those three commands will generate the ***DNS_COMMON, TLS_COMMON, and HTTP_COMMON*** folders under **pathGen**, each containing their corresponding JSON file.
    - Next, copy and paste each of these JSON files' data into their corresponding variables within the ***daalClassifyWithTime.py*** script (at the top), replacing the default data that is already there.
    - *You may choose to skip this step entirely if you think the default data contains all of the values present in your dataset, but take note you may get a key error that will indicate the need to collect this data.*
12. Finally, we can train and test the model, and time the process for comparison using **daalClassifyWithTime.py** (Logistic Regression).
    - For example, `python daalClassifyWithTime.py --workDir=pathGen --select=pathGen/train.json --classify --output=pathGen/params.txt --http --tls` will train and test the model with datasets in the given **train.json** and with "http" and "tls" features.
    - This will also generate the output file ***params.txt*** which can be used to test other datasets. (*to be implemented/tested*)
## Demo Steps
### 1. python daalAnalyze.py -i pathRAW -o pathGen
### 2. python daalSelectDataset.py --input pathGen/TLS_JSON/ --output pathGen/train.json --tls
### 3. python daalCollectCommonTLS.py -i pathGen/TLS_JSON
### 4. python daalCollectCommonHTTP.py -i pathGen/HTTP_JSON
### 5. python daalClassifyWithTime.py --workDir=pathGen --select=pathGen/train.json --classify --output=pathGen/params.txt --http --tls
## Additional Resources
### daal4py Documentation Home
#### - https://intelpython.github.io/daal4py/index.html
### Intel DAAL Developer Guide
#### - https://software.intel.com/en-us/download/intel-data-analytics-acceleration-library-developer-guide
