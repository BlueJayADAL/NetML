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

8. Our main script ***daalMaster.py*** provides functionality to streamline all data processing steps through training and testing by providing dedicated commands, listed below.
    - -i, --input [INPATH]: Path to input folder containing raw PCAPs (**pathRAW**)
    - -o, --output [OUTPATH]: Output folder for processed files from Cisco Joy (**pathGen**)
    - -j, --joy: Process raw PCAPs and generate output zip files using Cisco Joy
    - -f, --files: Generate output feature JSON files from Joy files
    - -c, --collect: Collect common features of DNS, HTTP, and TLS
    - -s, --selectData: Generate train and test JSON files
    - -t, --train [MODELTYPE]: Train specified model (supported: LR, SVM, DF, ANN)
    - -e, --test [MODELTYPE]: Test specified model (supported: LR, SVM, DF, ANN)

9. All we currently have are the raw PCAP files, so we will include all options to perform all data processing and train an initial model.
    - `python daalMaster --input=pathRAW --output=pathGen -jfcs --train=ANN`
    
10. Next, we can go ahead and test our model.
    - `python daalMaster --input=pathRAW --output=pathGen --test=ANN`

11. Steps 9 and 10 can then be repeated (omitting data processing options) for the additional models for comparison.

## Additional Resources
### daal4py Documentation Home
#### - https://intelpython.github.io/daal4py/index.html
### Intel DAAL Developer Guide
#### - https://software.intel.com/en-us/download/intel-data-analytics-acceleration-library-developer-guide
