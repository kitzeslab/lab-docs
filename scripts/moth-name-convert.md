## Converting AudioMoth hexadecimal filenames to UTC date & time

### Step 1: Hex to seconds after Linux epoch
Can be run directly from terminal:
```
for f in *.WAV; do HEXNUM=$(echo $f | cut -f 1 -d '.'); DECNAME=$(echo "ibase=16; $HEXNUM" | bc).WAV; mv -- $f $DECNAME; done
```

### Step 2: Step 1, plus seconds after Linux epoch to UTC date & time
Desired output: `YYYYMMDD_hhmmss.WAV`

Can be run directly from terminal:
```
for FILE in *.WAV; do HEXNUM=$(echo $FILE | cut -f 1 -d '.'); DECNUM=$(echo "ibase=16; $HEXNUM" | bc); TIMENAME=$(date -ur $DECNUM "+%Y%m%d_%H%M%S").WAV; mv -- $FILE $TIMENAME; done
```

### Step 3: Steps 1 & 2, plus adding MSD-XXXX to beginning of filename
Files assumed to be nested in directory `MSD-XXXX/`.
Desired output: `MSD-XXXX_YYYYMMDD-hhmmss.WAV`

Save this as a file, `moth-convert.sh`, within the DATE directory:

```
#! /bin/bash

clear

# loop over all directories named MSD-
for MSD in MSD-*
do
	for FILEPATH in $MSD/*.WAV
	do
		FILE=${FILEPATH##*/} # retain the part after the /
		HEXNUM=$(echo $FILE | cut -f 1 -d '.')
		DECNUM=$(echo "ibase=16; $HEXNUM" | bc)
		TIMENAME=$(date -d @$DECNUM "+%Y%m%d-%H%M%S").WAV
		NEWPATH="${MSD}/${MSD}_${TIMENAME}"
		echo renaming $FILEPATH to $NEWPATH
		mv -- $FILEPATH $NEWPATH
	done
done
```

Run this file from within the DATE directory:

```
bash moth-convert.sh
```


### Step 4: Date & time to directory structure
# todo

# TODO: split files
# TODO: naming convention for split files
# TODO: calling splitting script from python
