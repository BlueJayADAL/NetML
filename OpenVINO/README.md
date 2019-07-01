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
8. Go to the Model Optimizer Directory
    - `cd <INSTALL_DIR>/deployment_tools/model_optimizer/`
9. Next, we will create a new `virtualenv` to install further requirements into a sandbox environment. To do this we will give it a path to the directory we will create it in, a path to the python interpreter we will use (*Tested with Python 3.7*), and specify to inherit the global system python packages.
    - `virtualenv DESTDIR -p /path/to/python/interpreter --system-site-packages` 
10. Activate the `virtualenv`.
    - `source /vinoEnv/bin/activate`
    - *NOTE: The above command will be needed everytime you wish to work in this environment when you start a new shell. The `virtualenvwrapper` tool may be used to aid with the management of virtual environments. Read more about this [here](https://realpython.com/python-virtual-environments-a-primer/).
11. Install framework dependencies into the `virtualenv`, for this demo we will be using TensorFlow.
    - `pip3 install -r requirements_tf.txt`
12. In order to compile and run OpenVINO applications, we must update several environment variables.
    - Run following script script to temporarily set env variables: `source /opt/intel/openvino/bin/setupvars.sh`
    - Add this line to the end of your .bashrc to set your env variables on shell startup: `source /opt/intel/openvino/bin/setupvars.sh`
