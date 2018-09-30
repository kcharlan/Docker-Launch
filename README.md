# Docker-Launch
Automated process for Docker container bring-up on a platform
## Description
The docker-launch utility was designed to be inserted into the bootup process
of a Docker platform server, and to intelligently start the Docker containers
specified in a configuration file.

The intent was to provide an easy to configure and easy to manage solution to
automate container bring-up on platform server initial boot or reboot.

## Dependencies
The target platform system must have installed and in working order:
* Python 3.6.3 or higher (or a virtual environment hosting such)
* Docker
* Docker Compose
* Bash (can be replaced with another shell, as long as it supports the
source command. NOTE: sh does NOT support source, and will not work
* Be run as a user that has native access to the Docker and Docker Compose
commands
* Current implementation is only for Unix/Linux platforms. Pathing, scripting,
OS commands, and setup routine are not designed for non-Unix (e.g. Windows),
and will not work on other platforms.

## Configuration
The config.py file contains settings specifying install-to and run-at folder
and file locations. The following settings should be reviewed and modified if
necessary, prior to running the setup routine (setup.py):

CONFIG_FILE - This specifies the location and filename for the file that will
contain info to instruct docker-launch what containers or services need to be
started up at launch. If that default location does not match the intended
deployment, edit that parameter to reflect the desired location and/or
filename.

INIT_PATH - This points to where the deployment environment init.d daemon
expects to find its boot-up scripts and uses to link into its various
runlevels. If the deployment environment init.d uses a different directory,
then modify this parameter to point to the correct location.

INSTALLED_PATH - This setting indicates the location where docker-launch will
be installed (have all its files copied to), and where it is expected to reside
during execution. If a different install-to location is desired, modify this
parameter to indicate the desired install and run location.

An example docker-launch configuration file is supplied in the samples
directory, named 'sample-docker-launch.conf'. The header lines contain detailed
comments explaining the format and options. The setup routine will copy this
template file to the CONFIG_FILE destination. Once copied over, this file
should be modified to properly indicate what containers and directories should
be used at boot-time to launch containers and services.

## Deployment
1. If necessary, make any modifications to the config.py file.  
  a. Modify CONFIG_FILE path and filename to point to the configuration file.
  b. Only if necessary, modify the INIT_PATH to point to the proper init.rd
  target directory.  
  c. Modify the INSTALLED_PATH to point to the directory where the 
docker-launch routines will be installed and will run from in normal operation.  
2. Change into the directory where docker-launch was cloned into, or where it
currently resides in the target deployment system. These files should NOT be
deployed into or reside in INSTALLED_PATH prior to running setup.py in the next
step.
3. Change directory into the location where setup.py is located. If necessary,
setup a virtual environment prior to running setup.py, to configure the proper
python version and install the required packages, and then activate the
virtual environment before proceeding to the next step.
4. Run setup.py as a priviledged user (e.g. "sudo python setup.py"). NOTE:
Depending on your shell and environment, you might need to invoke a
priviledged shell first, to maintain priviledge across instructions.  
  Setup will:  
  a. Copy the docker-launch files into the INSTALLED_PATH.  
  b. Copy the samples/sample-docker-launch.conf to CONFIG_FILE.  
  c. Copy the samples/docker-launch.sh script into /etc/init.d  
5. If your general (non-virtual) deployment environment does not meet the 
requirements.txt and/or Python 3.6.3 or above requirements, or if you wish to
run docker-launch in a virtual environment, go to the INSTALL_PATH directory
and setup your virtual environment. Be sure to specify the python version and
install the requirements.txt modules. Also be sure to make the changes in
step 8 to invoke this virtual environment prior to running docker-launch.py
(see the comments inside the script).
6. Modify the configuration file (CONFIG_FILE specified path and filename) to
reflect the containers/directories to launch at startup.
7. If there are any directories specified in the configuration file, set them
up to contain the container names (e.g. touch /a/directory/container-name) or 
copy the docker-compose yaml file(s) into them.
8. Modify the docker-launch.sh script to match your environment.
9. Install the docker-launch.sh in your init services (e.g. "sudo update-rc.d docker-launch.sh defaults").
