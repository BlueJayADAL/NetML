# Intel VTUNE Amplifier for Performance Analysis
Using Intel VTUNE to analyze performance efficiency and bottlenecks.

## Walkthrough Guide
1. Download [package](https://software.intel.com/en-us/vtune/choose-download) from Intel.
2. Install required packages:
    - `sudo apt-get install libgtk-3-0 libasound2 libxss1 libnss3`
3. Extract installation package:
    - `tar -xzf vtune_amplifier_<version>.tar.gz`
4. Navigate to directory containing extracted files.
5. Launch the installer:
    - `sudo ./install_GUI.sh` (**There is also CL version**)
6. After installation succeeds, run following command to establish the VTUNE Amplifier environment:
    - `source <install-dir>/amplxe-vars.sh`
7. Launch VTUNE Amplifier
    - Run: `amplxe-gui` (**There is also CL version**)
8. If running in Ubuntu, and get error on main screen regarding data collection, in `/etc/sysctl.d/10-ptrace.conf` set *kernel.yama.ptrace_scope* to 0 using root permissions and reboot.
9. Be sure to be in Intel environment:
    `conda activate idp`
