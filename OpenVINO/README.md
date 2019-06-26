# OpenVINO Implementation of NetML Project
The OpenVINO implementation of the NetML project for deep learning.

## Walkthrough Guide
1. First download [Intel Distribution of OpenVINO Toolkit](https://software.intel.com/en-us/openvino-toolkit/choose-download/free-download-linux).
2. Switch directories to the location of the downloaded .tgz file.
3. Unpack the .tgz file using the following commmand: `tar -xvzf l_openvino_toolkit_p_<version>.tgz`
4. Change to the newly unpacked `l_openvino_toolkit_p_<version>` directory.
5. Install the prerequisite dependencies OpenVINO requires using the ready-made script: `sudo -E ./install_openvino_dependencies.sh`
6. Choose the Installation style you would like:
    - GUI: `sudo ./install_GUI.sh`
    - cmd: `sudo ./install.sh`
7. Follow on screen instructions to install.
8. Traverse to the new `install_prerequisites` directory (by default `/opt/intel/openvino/deployment_tools/model_optimizer/install_prerequisites`) to setup the prerequisites for the model framework you will be using (for this guide we will be using TensorFlow).
9. Run prereq script: `sudo ./install_prerequisites_tf.sh`
10. In order to compile and run OpenVINO applications, we must update several environment variables.
    - Run following script script to temporarily set env variables: `source /opt/intel/openvino/bin/setupvars.sh`
    - Add this line to the end of your .bashrc to permanently set your env variables: `source /opt/intel/openvino/bin/setupvars.sh`
