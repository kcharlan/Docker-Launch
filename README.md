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
* Be run as a user that has native access to the Docker and Docker Compose
commands
* Current implementation is only for Unix/Linux platforms. Pathing, scripting,
OS commands, and setup routine are not designed for non-Unix (e.g. Windows),
and will not work on other platforms.

## Configuration
The config.py file contains a default setting for the configuration file
location and filename, specified as the CONFIG_FILE parameter. If that default
location does not match the intended deployment, simply edit that parameter
to reflect the desired location and/or filename.

An example configuration file is supplied in the samples directory, named
'sample-docker-launch.conf'. The header lines contain detailed comments
explaining the format and options. You can copy this file to the target path
and filename of the intended configuration file, and then edit it to reflect
the target Docker environment.

The config.py parameter INSTALLED_PATH indicates the default location where
docker-launch will be installed, and where it is expected to reside during
execution. If its install location will be different, modify this parameter
as well.

You should modify all config.py parameters prior to running setup.py. If setup
has already been run, you will need to move files around manually (or remove
the prior files and redeploy by running setup.py again).

## Deployment
1. If necessary, make any modifications to the config.py file.  
  a. Modify CONFIG_FILE path and filename to point to the configuration file.  
  b. Modify the INSTALLED_PATH to point to the directory where the 
docker-launch routines will be installed and will run from in normal operation.  
2. Change into the directory where docker-launch was cloned or where it
currently resides. They should not reside in INSTALLED_PATH before running
setup.py in the next step.
3. Change directory into the location where setup.py is located, and then
run setup.py as a priviledged user (e.g. "sudo python3 setup.py"). This
will:  
  a. Copy the docker-launch files into the INSTALLED_PATH.  
  b. Copy the samples/sample-docker-launch.conf to CONFIG_FILE.  
  c. Copy the samples/docker-launch.sh script into /etc/init.d  
4. If your environment does not meet the requirements.txt and Python 3.6.3 or
above, or if you wish to run docker-launch in a virtual environment, go to the
INSTALL_PATH directory and setup your virtual environment. Be sure to specify
the python version and install the requirements.txt modules. Also be sure to
make the changes in step 6 to invoke this virtual environment prior to
running docker-launch.py (see the comments inside the script).
5. Modify the configuration file to reflect the containers/directories to
run against.
6. If there are any directories specified in the configuration file, set them
up to contain the container names (e.g. touch /a/directory/container-name) or 
copy the docker-compose yaml file(s) into them.
7. Modify the docker-launch.sh script to match your environment
8. Install the docker-launch.sh in your init services (e.g. "sudo update-rc.d docker-launch.sh defaults")
