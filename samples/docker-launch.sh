#!/bin/sh

### BEGIN INIT INFO
# Provides:          docker-launch
# Required-Start:    $local_fs $network $named $time $syslog $docker
# Required-Stop:     $local_fs $network $named $time $syslog $docker
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Description:       Automated launching of Docker containers
### END INIT INFO

# Modify if necessary, to reflect your install location
INSTALL_PATH="/usr/local/sbin/docker-launch"

# If your system does not natively have Python 3.6.3 or above, and you are
# using virtualenv or similar to provide the higher level of Python, then
# edit this path and uncomment this seciton.
# PYENV="env"
# source ${BASE_PATH}/${PYENV}/bin/activate

# If using a virtual environment, and you already set your default python
# to python3 (or whatever version needed at 3.6.3 or above), then modify the 
# below line to start with "python' instead of "python3".

python3 $INSTALL_PATH/docker-launch.py
