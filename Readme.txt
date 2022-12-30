Readme.txt

To use pip and particular python packages for this project, we create a virtual environment.

To create the virtual environment (just the first time):
cd to project dir
sudo apt install python3.8-venv
python3 -m venv env


To activate the virtual environment each time we want to use it, for that bash shell:
cd to project dir
source env/bin/activate


It will look like:
(env) adrian@adrian-computer:~/Professional/KidsApp$

To make sure it's working:
which python3
Result: It should be in the env directory:
/home/adrian/Professional/KidsApp/env/bin/python3


To quit the environment:
deactivate


To install a library:
python3 -m pip install requests

https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
