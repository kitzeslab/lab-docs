# Backups


# Rook

Our acoustic data are stored in the `/volume1/data` folder on Rook. Box backs up this folder to the lab's Box account folder, `data-backup`. 

When new data comes in, we:
* Create a folder on an external hard drive, named after the first date that recorders from this deployment were brought back
* Use a personal computer to transfer all data from microSD cards to the date folder on the external HD
* Create a `.csv` describing what data from these recordings should be used
    * Only use data taken after the last deployment date, and before the first return date. 
    * Removing boundary days avoids people/handling noise, and makes sure all our recordings start and end on the same date
* Connect external hard drive to Rook
* Drag & drop the date folder on Rook so it sits within `/volume1/data/field-data/<location_code_name>`, replacing `<location_code_name>` with the 4-letter code, e.g. `pnre`, `ssfo`.

# Robin

* Project files are stored on `lacie`, attached to Robin
* `seagate2` and `seagate3` are used for generic data storage and transfer.
* **Time machine** backups of Robin's hard drive are stored on `seagate1`. 
* **Backblaze** backs up Robin and all external hard drives except for `seagate1`. 
    * Warning: if an external drive has been detached for over 30 days, Backblaze will stop backing it up and delete the remote copy of its backups!


# Globus

Coming soon



# Box

Box's FTP server & FileZilla can be used to upload data to the cloud.

### Create a Box external password

* Sign in at https://pitt.app.box.com
* Click on your icon in the top-right corner and navigate to Account Settings
* Under "Authentication" add an external password to use in place of Single Sign On > click "Save Changes"

### Set up FileZilla

* Download FileZilla Client from https://filezilla-project.org/
* Open FileZilla and find the "QuickConnect" bar near the top of the window
* Complete the "QuickConnect" fields as follows:
   - Host: `ftp.box.com`
   - Username: `yourusername@pitt.edu`
   - Password: `your-external-password`
   - Port: We use `21`. See [Box's page about FTP](https://community.box.com/t5/Upload-and-Download-Files-and/Using-Box-with-FTP-or-FTPS/ta-p/26050) for more information.
* Click the "QuickConnect" button and wait for the connection to establish

### Use FileZilla & troubleshoot

* Your local filesystem appears in the left window; the Box filesystem appears on the right
* To transfer files from local to remote, navigate on both the local and remote filesystems to the desired source & destination folders. Drag the files/folders from the local filesystem, and drop them to the desired containing folder on your Box filesystem. 
* After your transfer is complete, check the "Failed Transfers" tab. If any transfers failed, right click and select "Reset & requeue all" 
* More troubleshooting tips are available on the [Box website](https://community.box.com/t5/Upload-and-Download-Files-and/Using-Box-with-FTP-or-FTPS/ta-p/26050)

<!--
# Time machine-like

This option is used to back up home folders (`/home`), 
user settings (`/etc`), 
service configurations (`/srv`), 
and helpful scripts (`/usr/local/scripts`)


The list of directories to save is itself saved in `/usr/local/scripts/globbing-filelist.txt`:

```
+ /home/ 
+ /etc/ 
+ /srv/ 
+ /root/
+ /usr/local/scripts/
- **
```


We just use `duplicity`, an incremental backup manager that comes with Ubuntu.
It assumes that safety of data is paramount and that storage
is cheap--which is true for us. 

The command:

```
sudo duplicity --verbosity 8 --no-encryption --include-filelist /usr/local/scripts/globbing-filelist.txt / file:///media/seagate/phoebe-backup/ > /home/kitzeslab/dup-dump.txt
```

To make this command run frequently, edit the root's `cron` job:

```
sudo crontab -e
```

And add this line to it (note that since this is in `root`'s crontab, `sudo` is not required):

```
# Back up our lab's data at 12AM daily
0 0 * * * duplicity --verbosity 8 --no-encryption --include-filelist /usr/local/scripts/globbing-filelist.txt / file:///media/seagate/phoebe-backup/ > /home/kitzeslab/dup-dump.txt
```

# TODO: full backup--monthly?


# Box data backup
# Recovery protocol

This document is a WIP. It includes protocols for both backing up and recovering data.

# Backup Protocol

The following steps were used to set up backups of lab data stored on `phoebe` and its associated 
hard drive mounted at `/media/seagate`. First, an overview of what files are stored where:

#### Acoustic data
Acoustic data exists in only one place locally--on the external hard drive. 
The hard drive's data folder is at `/media/seagate/data/`. In addition to this local copy, one remote 
copy of these data is stored on Box.com through `rsync` to a WebDAV folder. 
Thus, there are no *local* backups for these data--there is not enough storage space to keep a copy on `phoebe` proper.

#### TODO: SEAGATE READ ONLY

#### Home directories & programs
User home directories (i.e. `/home/`) and programs/configurations are backed up two ways.
1. Local `rdiff-backup` copy: Home directories are backed up locally at `/media/seagate/home-backup/`and programs and configurations are backed up at `/media/seagate/program-backup`. Because these files and settings
are changed more frequently than data, they are backed up on the hard drive using `rdiff-backup`.

2. Remote synchronized copy: the original files (i.e. not the rdiff'd copies) are also backed up to Box. 

## 1. Set up Box access on `phoebe`
#### TODO: automount Box

### Set up WebDAV
* Install `davfs2`: 

  ```$ sudo apt-get install davfs2```

* Add myself and other users to the `davfs2` group (had to log out + log in for these changes to take effect): 

  ```$ usermod -a -G davfs2 username```

* Append an option to the `davfs2.conf` file at the mount point to not use locks:

  ```$ sudo bash -c 'printf "use_locks\t0" >> /etc/davfs2/davfs2.conf'```

* Copy the `.davfs2` folder--which includes the newly modified config file--to my home directory: 

  ```$ sudo cp -r /etc/davfs2 ~/.davfs2```
  
### Set up a mount point for the Box server
* Create a directory to use as the mount point for the Box server: 

  `$ mkdir /media/box/`

* Add a tab-separated entry to `/etc/fstab` to allow mounting:

  ```
  # box.com server mount
  https://dav.box.com/dav/ /media/box davfs rw,user,noauto	0	0
  ```

* Edit the `/media/box/.davfs2/secrets` file. Add a single line in this format:

  ```
  https://dav.box.com/dav ter38@pitt.edu
  ```

  Can also add a password after (in format `"box_password"`).
  This is required for automated mount/sync, but will require
  that the file is NOT readable by others:

  ```$ chmod 600 /media/box/.davfs2/secret```


## 2. Automated sync with `rsync` + `cron`
Once a day, changes made to data, programs, etc. are synced to the appropriate destinations.

### TODO: cron output location
### TODO: bash script instead of cron output

```
# Back up our lab's data at 12AM daily
0 0 * * * rsync -a /media/seagate/data/ /media/box/data-backup/

# Back up home folders to seagate at 6PM daily using rdiff
0 18 * * * rdiff-backup -a /home/ /media/seagate/home-backup/

# Back up home folders to Box at 8PM daily using rsync
0 20 * * * rsync -a /home/ /media/box/home-backup/


####

# Back up home data at 6PM
0 6 * * * rsync -a --relative /usr/share/lab-data/./ /media/seagate/data-backup/

# Back up our lab's data at 12AM
0 0 * * * rsync -a --relative /home/ /media/seagate/other-backup/daily/

```

## Preparation: Mount external backup drive if it isn't already mounted
If the external hard drive is attached at boot, it will be mounted at `/media/seagate`.

If not, then mount it by running `sudo mount -a`.

## DAILY: Back up our lab's data

(mkdir: data-backup)
```rsync -a --relative /usr/share/lab-data/./ /media/seagate/data-backup/```

## DAILY, WEEKLY, MONTHLY: Back up personal data and settings
### TODO: Add --delete 
Back up user home directories such that they appear within `/media/seagate/other-backup/daily/home/`
(mkdir: other-backup/)
```rsync -a --relative /home/ /media/seagate/other-backup/daily/```

## DAILY, WEEKLY, MONTHLY: Back up programs
Source: this 
[AskUbuntu question](https://askubuntu.com/questions/9135/how-to-backup-settings-and-list-of-installed-packages)  

Get a list of installed packages 

```dpkg --get-selections > /usr/share/lab-packages/Package.list```

Get all package sources in `/etc/apt/sources.list` and `/etc/apt/sources.list.d`

```sudo cp -r /etc/apt/sources.list* /usr/share/lab-packages/```

Get all trusted package keys

```sudo apt-key exportall > /usr/share/lab-packages/Repo.keys```



# Recovery protocol

## Restore personal files
### TODO: Recover accounts first, update backup location

`rsync --progress /path/to/user/profile/backup/here /home/`

## Reinstall packages on a fresh system
### TODO: change path to ~/Repo.keys, /Package.list, etc.

Replace keys

`sudo apt-key add ~/Repo.keys`

Replace sources

`sudo cp -r ~/sources.list* /etc/apt/`

Get dselect and use it to update the available packages database
```
sudo apt-get update
sudo apt-get install dselect
sudo dselect update
```

Select packages to install and install everything in the list
```
sudo dpkg --set-selections < ~/Package.list
sudo apt-get dselect-upgrade -y
```
-->