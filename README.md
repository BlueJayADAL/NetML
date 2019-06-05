# NetML
The NetML project using the Intel Distribution for Python.

## Walkthrough Guide
1. It is recommended to have [Anaconda](https://docs.anaconda.com/anaconda/install/linux/) installed, as this guide will use Anaconda to create a virtual environment with Intel packages (**Python 3**).
2. Install [Joy](https://github.com/cisco/joy) (with "-gzip-enabled") and run it successfully. Refer here for sample install steps for Ubuntu system.
3. Note that the current Joy cannot generate the DNS data correctly when the 'bidir' is enabled which is required by TLS data. In order to fix this issue, please overwrite the current dns.c of Joy with the one in the JoyFix.
4. Have the raw PCAP dataset folder ready. The following is only an example (CICAndMal2017/PCAPs), however our codes are currently only tested with such tree structure (Only 1 "Benign" and multiple "ware" folders). Under each folder, it should contain the raw pcap files. Be sure that all folder names only include alphanumeric characters, or errors will arise down the road when the names are parsed (for CICAndMAL2017 rename AndroidSpy277 + FakeAppAL). In order to quickly run through this guide, let's call this pathRAW.
```
├── Adware
│   ├── Dowgin
│   ├── Ewind
│   ├── Feiwo
│   ├── Gooligan
│   ├── Kemoge
│   ├── koodous
│   ├── Mobidash
│   ├── Selfmite
│   ├── Shuanet
│   └── Youmi
├── Benign
│   ├── 2015
│   ├── 2016
│   └── 2017
├── Ransomware
│   ├── Charger
│   ├── Jisut
│   ├── Koler
│   ├── LockerPin
│   ├── Pletor
│   ├── PornDroid
│   ├── RansomBO
│   ├── Simplocker
│   ├── Svpeng
│   └── WannaLocker
├── Scareware
│   ├── AndroidDefender
│   ├── AndroidSpy277
│   ├── AVforandroid
│   ├── AVpass
│   ├── FakeApp
│   ├── FakeAppAL
│   ├── FakeAV
│   ├── FakeJobOffer
│   ├── FakeTaoBao
│   ├── Penetho
│   └── VirusShield
└── SMSMalware
    ├── Beanbot
    ├── Biige
    ├── fakeinst
    ├── fakemart
    ├── fakenotify
    ├── jifake
    ├── mazarbot
    ├── Nandrobox
    ├── plankton
    ├── smssniffer
    └── zsone
```
