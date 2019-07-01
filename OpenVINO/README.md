# OpenVINO Implementation of NetML Project
The OpenVINO implementation of the NetML project for deep learning.

## Walkthrough Guide
1. Be sure to have completed the entirety of the DAAL NetML Walkthrough, as this will be required later in this guide.
2. First download [Intel Distribution of OpenVINO Toolkit](https://software.intel.com/en-us/openvino-toolkit/choose-download/free-download-linux).
3. Switch directories to the location of the downloaded .tgz file.
4. Unpack the .tgz file using the following commmand: `tar -xvzf l_openvino_toolkit_p_<version>.tgz`
5. Change to the newly unpacked `l_openvino_toolkit_p_<version>` directory.
6. Install the prerequisite dependencies OpenVINO requires using the ready-made script.
    - `sudo -E ./install_openvino_dependencies.sh`
7. Choose the Installation style you would like:
    - GUI: `sudo ./install_GUI.sh`
    - cmd: `sudo ./install.sh`
8. Follow on screen instructions to install.
9. Go to the Model Optimizer Directory
    - `cd <INSTALL_DIR>/deployment_tools/model_optimizer/`
10. Next, we will create a new `virtualenv` to install further requirements into a sandbox environment. To do this we will give it a path to the directory we will create it in, a path to the python interpreter we will use (*Tested with Python 3.7*), and specify to inherit the global system python packages.
    - `virtualenv DESTDIR -p /path/to/python/interpreter --system-site-packages` 
11. Activate the `virtualenv`.
    - `source /vinoEnv/bin/activate`
    - *NOTE: The above command will be needed everytime you wish to work in this environment when you start a new shell. The `virtualenvwrapper` tool may be used to aid with the management of virtual environments. Read more about this [here](https://realpython.com/python-virtual-environments-a-primer/).*
12. Install framework dependencies into the `virtualenv`, for this demo we will be using TensorFlow.
    - `pip3 install -r requirements_tf.txt`
13. In order to compile and run OpenVINO applications, we must update several environment variables.
    - Run following script script to temporarily set env variables: `source /opt/intel/openvino/bin/setupvars.sh`
    - Add this line to the end of your .bashrc to set your env variables on shell startup: `source /opt/intel/openvino/bin/setupvars.sh`
14. Run the following command to retreive the absolute path for the environment python.
    - `which python`
15. Using this absolute path, modify the shebang interpreter path in the `vinoInference.py` and `mo_tf.py` scripts.
16. Deactivate the openVINO environment, and activate the Anaconda Intel environment.
    - `deactivate`
    - `conda activate idp`
17. Navigate to the directory containing all of the DAAL scripts.
    - `cd <PATH>/NetML/`
18. Using the pre-built Artificial Neural Network (ANN) from the DAAL walkthrough, we will construct an optimized OpenVINO ANN using OpenVINO's Model Optimizer and Inference Engine.
19. The "training" of the OpenVINO ANN entails transforming the current (trained) TensorFlow model into an optimized format that the OpenVINO Inference Engine can work with. To do this, we will use the same `daalClassifyWithTime.py` script used before, but with the vinoANN spec for the model. The command will run the `mo_tf.py` script, which invokes the Model Optimizer for a TensorFlow model.
    - `python daalClassifyWithTime.py --workDir=<PATH>/daalTestJoy --select=<PATH>/daalTestJoy/train.json --classify --output=params.txt --model=vinoANN --http --tls`
    
