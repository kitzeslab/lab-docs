# Using the shell

Table of contents:

* [Standard commands](#standard-commands)
* [Helpful programs](#helpful-programs)
* [MongoDB](#mongodb)
* [Cluster computing](#cluster-computing)

# Standard commands

* `ssh kitzeslab@<robin's URL>`
* `pwd` - print working directory. This is the directory, aka the "folder", that you're issuing commands from.
* `ls` - list contents of the current working directory
* `ls /Volumes/seagate1/` - list the contents of the directory `/Volumes/seagate1/`
* `ls -lh` - list the files with more information: `l` = long list, `h` = human-readable file sizes
* `cd` - change directories into your home directory
* `cd ..` - go up one directory, e.g. from `/Volumes/seagate1/` to `/Volumes/`.
* `cd seagate1/` - change directories into `seagate1/`. This is a relative path, i.e. the shell attempts to change into a directory contained within the current working directory.
* `cd /Volumes/seagate1` - change directories into `/Volumes/seagate1/`. This is an absolute path, i.e. you can do this from any working directory
* `mkdir hello` - make a directory called `hello` within the current directory
* `mkdir /Users/tessa/Recordings/MSD-0001` - make the directory `MSD-0001` within preexisting directory `/Users/tessa/Recordings/`. 
* `scp kitzeslab@<robin's URL>:/Volumes/seagate1/data/field-data/<date folder>/<card folder>/<filename>.WAV .` - copy a file into your current working directory (specified by `.`). 
* `scp kitzeslab@<robin's URL>:/Volumes/seagate1/data/field-data/<date folder>/<card folder>/<filename>.WAV /Users/<username>/Recordings` - copy a file into the directory `/Users/<username>/Recordings`.

# Helpful programs

### Watch your processor usage: `htop`

### Run long programs: `tmux`

This package allows you run programs in the background. Use this for long programs that you'd like to keep running, even if you leave, exit your SSH session, etc.

* New tmux session: `tmux new -s <descriptive-session-name>`
* Detach from session: ^B then D
* View sessions: `tmux ls`
* Reattach to session: `tmux attach -t <descriptive-session-name>`

# MongoDB

Working data for our analyses, e.g., statistics, generated spectrograms, etc. are stored in MongoDB. Mongo is a nesting structure: many collections can lie within a single database. Mongo can be investigated from within the mongo shell (accessed by typing `mongo`) or from within the Bash shell.

### Mongo shell

```
$ mongo
> help # help for large-scale Mongo methods
> db.help() # help for methods to manage DBs
> show dbs # view all databases
> use <db name> # use a databse
> db.getCollectionNames() # get collection names while using a database
> db.<collection name>.drop() # drop a collection while using a database
> db.dropDatabase() # drop an entire database
```


### Mongo in bash

#### Move a collection
Dump a collection into the current directory:
```
$ mongodump -d <db_name> -c <collection_name>
```

Dump will be stored in `./dump/<db name>/<collection name>`.

Compress the dump to move it easily: (naming convention: `<db>-<collection>-<date>`)

```
$ tar cvf <name>.tar.gz dump
```


#### Load/restore a collection

Will automatically try to load to a database & collection with the same name as the one it came from. (Or you can specify a new collection name using `-d` and `-c`). If the collection already exists, the `mongorestore` will fail.

```
$ mongorestore -d <new name of database> -c <new name of collection> <.bson file to restore from>
```


# Cluster computing

Get onto the cluster with 
```
ssh h2p.crc.pitt.edu
```

For software shared between nodes:
`module spider python` 

Other helpful commands:
* `module load`
* `module list`
* `module unload` 
* `module purge`
* `which python`