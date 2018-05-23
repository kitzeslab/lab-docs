## Converting AudioMoth hexadecimal filenames to UTC date & time
Written for OS X

### Step 1: Hex to seconds after Linux epoch
`for f in *.WAV; do HEXNUM=$(echo $f | cut -f 1 -d '.'); DECNAME=$(echo "ibase=16; $HEXNUM" | bc).WAV; mv -- $f $DECNAME; done`

### Step 2: Step 1, plus seconds after Linux epoch to UTC date & time
Desired output: YYYYMMDD_hhmmss.WAV

`for FILE in *.WAV; do HEXNUM=$(echo $FILE | cut -f 1 -d '.'); DECNUM=$(echo "ibase=16; $HEXNUM" | bc); DATENAME=$(date -ur $DECNUM "+%Y%m%d_%H%M%S").WAV; mv -- $FILE $DATENAME; done`

### Step 3: Steps 1 & 2, plus adding MSD-XXXX to beginning of filename
Files assumed to be nested in directory `MSD-XXXX/`

`for FILE in *.WAV; do HEXNUM=$(echo $FILE | cut -f 1 -d '.'); DECNUM=$(echo "ibase=16; $HEXNUM" | bc); DATENAME=$(date -ur $DECNUM "+%Y%m%d_%H%M%S").WAV; mv -- $FILE $DATENAME; done`

### Step 4: Date & time to directory structure
# todo

# TODO: split files
# TODO: naming convention for split files
# TODO: calling splitting script from python
