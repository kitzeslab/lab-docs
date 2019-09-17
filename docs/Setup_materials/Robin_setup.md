# Robin setup

Table of contents:

* [Downloads](#downloads)
* [Anaconda & JupyterHub](#anaconda)
* [JHub/Mongo maintenance](#service-maintenance)
* [User Setup](#user-setup)
    * [Personal package management](#personal-package-management)
* [Hard drives](#hard-drives)
* [MongoDB](#mongodb)
* [Login problems](#login-problems)


# Downloads 
* [Google Chrome](https://www.google.com/chrome/), [iTerm2](https://www.iterm2.com/), [XQuartz](https://www.xquartz.org/), [Java Development Kit](http://www.oracle.com/technetwork/java/javase/downloads/index.html), [Raven Pro](http://ravensoundsoftware.com/raven-pricing); [Kaleidoscope](https://www.wildlifeacoustics.com/download/kaleidoscope-software)
* [Homebrew](https://brew.sh/)
    * Use this to install: `brew install vim git libsamplerate tmux wget`
    * To update Homebrew itself and download package updates: ` brew update`
    * To install package upgrades: `brew upgrade`
* [Anaconda](https://www.anaconda.com/download/#macos), Python 3.7 version
    * Use the command line installer to install in root; see setup instructions below

Move all `.dmg`s and other download files to trash!

# Anaconda

* Download Anaconda by `wget`ing the command line installer.
* Run the downloaded installer with `sudo bash` and specify the install location as `/anaconda3`.
* Change ownership of the file to `admin`: `sudo chown -R admin /anaconda3`

#TODO: automatically add conda/python to new users' `.bashrc`; ensure `.bashrc` is sourced in `.bash_profile`
```
# added by Anaconda3 5.2.0 installer
export PATH="/anaconda3/bin:$PATH"
. /anaconda3/etc/profile.d/conda.sh
```

### JupyterHub setup

* Install JuypterHub and R in base conda (the only package that should be installed in base conda!)

        (base) $ conda install jupyterhub
        (base) $ conda install -c r r-irkernel

* Create config file for Jupyter, `/etc/jupyterhub/jupyterhub_config.py`:

        $ jupyterhub --generate-config 
        $ sudo mkdir /etc/jupyterhub
        $ sudo mv jupyterhub_config.py /etc/jupyterhub/
        $ sudo vim /etc/jupyterhub/jupyterhub_config.py

  Add the following lines to the config file (all of the defaults are commented out in the generated config file; they can be kept around for reference):

        c.JupyterHub.cookie_secret_file = '/etc/jupyterhub/jupyterhub_cookie_secret'
        c.JupyterHub.port = 80
        c.Spawner.cmd = ['/anaconda3/bin/jupyter-labhub']
        c.Spawner.default_url = '/lab'
        c.Authenticator.admin_users = {'admin'}

* Make directory for cookie-secret: `$ sudo mkdir /etc/jupyterhub/jupyterhub_cookie_secret`
* At this point you can run Jupyterhub with `$ sudo jupyterhub -f /etc/jupyterhub/jupyterhub_config.py`


### Set up as service

* Create `/Library/LaunchDaemons/local.jupyterhub.plist` using [this file](https://github.com/kitzeslab/lab-docs/blob/master/config-files/jupyterhub-plist.md)
* Change permissions on that file: `chmod 644 /Library/LaunchDaemons/local.jupyterhub.plist`
* Load into launchd: `sudo launchctl load /Library/LaunchDaemons/local.jupyterhub.plist`
* Start it: `sudo launchctl start local.jupyterhub`
* This should start JupyterHub, and it should restart on every reboot.

### R for JupyterHub

R should already be installed on the machine at this point--it was installed with JupyterHub. (See above)
Manage R using R's command line package manager
```
$ R
> install.packages("spatstat", "nimble")
```

### Make `/Volumes/lacie` accessible on JupyterLab

For some reason, JupyterLab wasn't allowing users to navigate to `/Volumes/lacie`. Instead we made a symlink to it on `/`: `$ sudo ln -s /Volumes/lacie /lacie`

# Service maintenance

Both MongoDB and JupyterHub are system services under `/Library/LaunchDaemons/`.
To maintain these services, use `launchctl`.

If you need to edit the services' configurations, you can do so by editing the respective
`.plist` file under `/Library/LaunchDaemons/` and reloading the service using the following code. 
Before doing this, **ensure that no processes will be interrupted**, e.g. choose "Running" from the 
side menu in JupyterLab and double-check that any notebooks with running kernels are saved and
aren't actively running code.

```
sudo launchctl unload /Library/LaunchDaemons/<.plist name>
sudo launchctl load /Library/LaunchDaemons/<.plist name>
sudo launchctl start /Library/LaunchDaemons/<.plist name>
sudo launchctl list | grep local #sudo is required due to root having a separate list than user
```

If `launchctl start` doesn't start the service, restart the computer.


### Check logs

As specified by our plist files above, we have logs for MongoDB and JupyterHub in the following locations:
* MongoDB: `/usr/local/var/log/mongodb/output.log`
* JupyterHub:
   * Error: `/var/log/jupyterhub.stdout`
   * Output: `/var/log/jupyterhub.stderr`



# User setup

### Install SSH for users
Make sure Eric has enabled the desired port/hostname. Open System Preferences > Sharing > enable Remote Login.

For more information about setting up SSH for users, see [Computing setup](https://github.com/kitzeslab/lab-docs/wiki/Computing-setup)

### Create user accounts
Add conda/python to new users' `.bashrc` (see below); ensure `.bashrc` is sourced in `.bash_profile`
```
# added by Anaconda3 5.2.0 installer
export PATH="/anaconda3/bin:$PATH"
. /anaconda3/etc/profile.d/conda.sh
```


### Create JupyterHub server
Have user log into VPN and then enter their username and password into JupyterHub server. The server will take a long time to initialize, but after waiting and refreshing, should work. Refer to instructions below about setting up virtual environments on a per-user basis.



### Personal package management

Read this section in its entirety before running any commands.

#### Creating an environment

No conda packages should be installed on the `base` environment. Create conda environments for your projects by doing the following. These packages will be placed in your own home directory (`~/.conda/envs/myenvironmentname`) instead of in the base conda environment (`/anaconda3/`).

        $ conda create --name myenvironmentname
        $ conda activate myenvironmentname
        (myenvironmentname) $ conda install packagesineed
        (myenvironmentname) $ conda deactivate #when you're done
        $ conda env list # Confirm the location of your environment
        # conda environments:
        #
        myenvironmentname        /Users/kitzeslab/.conda/envs/myenvironmentname
        base                  *  /anaconda3


If you need to `pip install` packages, *you must `conda install pip` within the environment first*. You should also only `pip install` any packages after all desired conda packages have been installed (per the [best practices checklist](https://www.anaconda.com/using-pip-in-a-conda-environment/). To install pip within the environment first:
        
        (myenvironmentname) $ which pip
        /anaconda3/bin/pip  # DO NOT USE THIS PIP!!! :-(

        (myenvironmentname) $ conda install pip  # install pip within your environment
        (myenvironmentname) $ which pip
        /Users/kitzeslab/.conda/envs/myenvironmentname/bin/pip # THIS IS A GOOD PIP :-)

        (myenvironmentname) $ pip install packagesineed


Once your environment is made, export it to an `environment.yml` file within the folder for the project that the environment was created for. This way, future users can install the environment themselves and run your code. Since you installed pip with anaconda, this will also export all pip-installed packages.

        (myenvironmentname) $ conda env export --name myenvironmentname > ./environment.yml


#### Environments in Jupyter

With the above actions, you should be able to run Python scripts in an environment using a shell, e.g. when SSH'd into Robin. To run Python code in your environment in Jupyter, you have to add the environment to your list of available "kernelspecs."


First, if you are working from the Jupyter shell, do the following to gain access to `conda activate`, etc.:

        $ source ~/.bashrc

Activate the environment and create/install a kernel for it:

        $ conda activate myenvironmentname
        (myenvironmentname) $ conda install ipykernel
        (myenvironmentname) $ ipython kernel install --user --name myenvironmentname --display-name "Python (birds)"
        (myenvironmentname) $ conda deactivate

This will make a kernel that is accessible when logged in to your account on JupyterHub. You may have to log in and out of JuypterHub for `jupyter kernelspec` changes to take place. After the changes have taken effect, when you use the Launcher screen to make a new notebook, you will see an option to make a notebook in your environment. You can also change an existing notebook to execute in your new environment by clicking on the "Python 3" option in the top right of the notebook screen, and using the drop-down to select your environment.

To remove unwanted kernels, remove from both `conda` and `jupyter`:
 
        (myenvironmentname) $ conda deactivate # Must deactivate an env before deleting it
        $ conda env remove --name myenvironmentname
        $ jupyter kernelspec uninstall myenvironmentname

Again, you may have to log in and out of JuypterHub for `jupyter kernelspec` changes to take place. 


# Hard drives
### Organization

The structure of our external hard drives should be maintained as follows:
* `lacie`
    - `projects1`: folders for individual lab members
    - other non-acoustic data folders
    - outside code
* `seagate1`: time machine backup of computer except for external HDs
* `seagate2`: windows NTFS-formatted hard drive
* `seagate3`: acoustic data
    - `tests`: data generated for tests of equipment, etc.
    - `field-data`: date-labeled folders for our own data
    - other data, e.g., from collaborators, open datasets, etc.


*Note: backups of external hard drives are stored elsewhere. For more information, see the Backups section.*

### Mounting

Some helpful maintenance commands:
* List devices to be mounted: `diskutil list`
* Mount a device, e.g. `/dev/disk1s1`: `diskutil mount /dev/disk1s1`
* Show where filesystems are mounted: `mount`
* View percentage storage capacity used on mounts: `df -h`





# MongoDB

Set up MongoDB as a service.

<!--

Set up Homebrew service manager - don't do this. Brew services manager assumes you want single-user services.

```
$ brew tap homebrew/services
$ brew services start mongodb
$ brew services list

Thanks to `brew services start mongodb`, mongodb is started and will restart on startup.
```
-->

* See commented-out notes above about not using `brew services`...
* Install `mongodb`: `$ brew install mongodb`
* Save [this document](https://github.com/kitzeslab/lab-docs/blob/master/config-files/local.mongodb.plist) in `/Library/LaunchDaemons/local.mongodb.plist`
* Change permissions on that file: `chmod 644 /Library/LaunchDaemons/local.mongodb.plist`
* Load into launchd: `launchctl load /Library/LaunchDaemons/local.mongodb.plist`
* Start it: `launchctl start local.mongodb`

Now MongoDB should start automatically on login. Its data are stored in `/data/db`.


# Login problems

Occasionally too many logins will be active and Mac will not allow more logins. (The maximum is 10 logins.) This happens, for instance, when SSH sessions are disconnected without logging out--so one user can be "logged in" multiple times.

To kill these inactive logins via the terminal:
* Use `tty` to see what session you're currently using. (You don't want to kill your own session.)
* Investigate what users are idle using the `w` command.
    - If the TTY is "console" then the user physically accessed the computer.
    - If the TTY is is `s001` or similar, then the user accessed the session through bash. These are the sessions to kill; remove any that have been inactive for a long time.

     $ w
     13:19  up 54 days, 18:55, 10 users, load averages: 2.05 2.10 2.13
     USER     TTY      FROM              LOGIN@  IDLE WHAT
     admin    s002     -                10Jan19 54days -

* Find the inactive sessions' PIDs by looking up their TTY: 

      $ ps -ft s002
      UID   PID  PPID   C STIME   TTY           TIME CMD
      0  6014  6013   0 11Jan19 ttys002    0:00.02 login -pflq admin /bin/bash


* Kill the session(s) using `sudo kill <PID> <PID> ...`. Use `-9` flag to force if you have to. For instance,

      $ sudo kill -9 6014 

# Backups

We have two main components of our system to back up: the system itself, and our stored files and data. Our system is backed up using Time Machine, which saves regular captures of the system to `seagate1`. Our external data are backed up using Backblaze cloud service. See [Hard drives](#hard-drives) for more information.

We used to use Box. It was not an automated process. To replicate this process: After all data from a certain field date are added to the computer, zip the date folder and store the zipped folder on the desktop. Then use FileZilla to log into the Kitzes Lab Pitt account and back up the zipped folder to Box. Use server `ftp.box.com` and port `21`.
