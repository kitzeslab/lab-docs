# Change AudioMoth filenames

AudioMoth saves its filenames in UNIX time,
i.e. seconds after 00:00:00 Coordinated Universal Time (UTC), 
Thursday, 1 January 1970.
The filenames are also saved in hexadecimal format, 
a 16-numeral system (vs. our typical 10-numeral system).

To instead save the filenames as desired output 
`MSD-XXXX_YYYYMMDD-hhmmss.WAV`, we have to take 3 steps:
* Convert the hex filename to decimal
* Convert the decimal UNIX epoch name to a human-readable UTC date
* Wrap the filename with the desired information about the SD card number.


To do this, save this code as a file, 
`moth-convert.sh`, within the DATE directory.
Files are assumed to be nested under the
DATE directory in directories `MSD-XXXX/`.


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

## Steps it took to get to the above:

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

This is the script above.


# TODO: potential next steps
Date & time to directory structure

Split files to decrease their length (split files should NOT be backed up--we should always retain
original copies of the files)

Name split files 

Call splitting script from Python (we've had memory issues trying to use whole hourlong audio files in Python)
