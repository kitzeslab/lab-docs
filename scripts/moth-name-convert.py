'''
TODO: before using
- EST/DST problems?
- Test for SDC
- Let user input field_data directory
- TODOs in code

TODO: potential next steps
- Date & time to directory structure
- Split files to decrease their length 
  (split files should NOT be backed up--we should always retain
  original copies of the files)
- Name split files 
- Call splitting script from Python 
  (we've had memory issues trying to use whole hourlong audio files in Python)
'''
                                                                                                                                                          
from os.path import join, isdir, exists
from os import listdir, makedirs, system
import shutil
import time

_MAC_MOUNT_POINT = '/Volumes'

def rename_wavs(wav_dir):
    '''
    Renames all .WAVs in a directory:
    from hexadecimal-formatted epoch times to times in EST with format YYYYMMDD_HHMMSS
    '''

    #TODO .WAV or .wav

    wavs = [path for path in listdir(wav_dir) if path[-4:].upper() == '.WAV']

    for filename in wavs:
        # convert hexadecimal epoch time to seconds
        seconds = int(filename[:-4], 16)

        #TODO: ensure that the time is converted to the time in this timezone
        #   depending on whether it was DST on YYYYMMDD, not on whether it is currently DST

        # Convert epoch time to date & time at current eastern time
        real_date = time.strftime('%Y%m%d_%-H%M%S', time.localtime(seconds))

        # Move filename
        source = join(wav_dir, filename)
        # TODO: .WAV or .wav
        destination = join(wav_dir, real_date+'.WAV')
        shutil.move(source, destination)

def copy_wavs(from_dir, to_dir):
    '''
    Uses rsync to transfer .WAV files from `from_dir` to `to_dir`
    '''

    #Create list of filenames from .WAV files in from_dir
    #wavs = [filename for filename in listdir(from_dir) if filename[-4:].upper() == '.WAV']

    # Copy all .WAV files (TODO: *.WAV or .wav)
    wav_wildcard = join(from_dir, '*.WAV')
    system("rsync -a --info=progress2 --stats {} {}".format(wav_wildcard, to_dir))

def get_card_mount_point(mount_point, card_name):
    '''
    For a particular mount point, see if a card volume is mounted there.

    Expected mount points:
        - If `card_name` starts with MSD, card mounted at 'mount_point/card_name'
        - Otherwise, asks user where card is mounted

    Returns:
        False: if no card is mounted in the expected way
        absolute path to card: if card is mounted
    '''

    card_prefix = card_name[0:3]
    volumes_dirs = listdir(mount_point)

    if card_prefix == 'MSD':
        # The volume itself should be named card_name
        if card_name in volumes_dirs:
            return join(mount_point, card_name)
        else:
            print('No card {} found in {}. Please check the volume name and try again.'.format(card_name, mount_point))
            return False
    else:
        # Ask the user what the volume is named
        vol_name = raw_input('What is the card\'s volume name? ')
        if vol_name in volumes_dirs:
            return join(mount_point, vol_name)
        else:
            print('No card {} found in {}. Please check the volume name and try again.'.format(vol_name, mount_point))
            return False

def get_card_storage_dir(date_dir, card_name):
    '''
    Makes a new directory named `card_name` in `date_dir`, but does not overwrite previously made directories

    Returns:
        - If directory didn't exist: returns the path to the new directory
        - If directory already exists, returns False
    '''

    card_storage_dir = join(date_dir, card_name)

    # Return False if directory already exists
    if exists(card_storage_dir):
        print("That SD card directory already exists. Check & try again.")
        return False

    # Make the directory & return path to it if it doesn't already exist
    print("Making directory for {}.".format(card_name))
    makedirs(card_storage_dir)
    return card_storage_dir

def get_card_name():
    '''
    Get a card name from a user.
    Checks input to ensure that card name is in format either MSD-XXXX or SDC-XXXX.

    Returns:
        the validated card name
    '''

    card_name = ''

    while not card_name:
        # Get user input for card name
        card_name = raw_input("What is the card name? ")

        # Ensure card name is correct length
        if len(card_name) != 8:
            print('Card name must be 8 characters long')
            card_name = ''
            continue

        # Check both prefix and suffix
        card_prefix = card_name[:4]
        card_num = card_name[4:]

        if card_prefix == 'MSD-' or card_prefix == 'SDC-':
            # Make sure card suffix is a number
            try:
                int(card_num)
                return card_name
            except ValueError:
                print('Card suffix must be 4 numbers')
        else:
            print('Card name must start with "MSD-" or "SDC-"')

        # Card name hasn't returned at this point --> reset it
        card_name = ''

def is_datelike(string):
    '''
    Checks if a string is "datelike", i.e., if it is in format 20XXXXXX

    Returns: True (datelike) or False (not datelike)
    '''

    # TODO: Better date validation
    if len(string) == 8:
        if string[0:2] == '20':
            return True

    return False

def get_date_dir(storage_dir):
    '''
    Ask user what field-date the files are from

    Makes a directory for the date within `storage_dir` if dir doesn't already exist

    Returns: path to the date directory
    '''

    # Get folder named with most recent date in storage_dir
    paths_in_storage = listdir(storage_dir)
    dirs_in_storage = [path for path in paths_in_storage if is_datelike(path) and isdir(join(storage_dir, path))]
    dirs_in_storage.sort()
    most_recent_date = dirs_in_storage[-1]

    finished = False
    while not finished:
        # Check to see if user wants to upload data to the most recent return date folder (most frequently used option)
        correct_date = raw_input("Are you uploading data from return date {}? (y/n) ".format(most_recent_date))
        if correct_date.upper() == 'Y':
            uploading_from_most_recent = True
            finished = True
        elif correct_date.upper() == 'N':
            uploading_from_most_recent = False
            finished = True
        else:
            print("Please answer yes or no. ")

    if uploading_from_most_recent:
        # Return directory for most recent date
        return join(storage_dir, most_recent_date)
    else:
        # Get a valid date
        finished = False
        while not finished:
            user_date = raw_input("What return date? ")
            if is_datelike(user_date):
                finished = True
            else:
                print("Enter a date in format YYYYMMDD.")

        # Return date directory, creating it if it doesn't already exist
        date_dir = join(storage_dir, user_date)
        if not exists(date_dir):
            print("Making directory for {}".format(user_date))
            makedirs(date_dir)
        else:
            print("Using preexisting directory {}/.".format(user_date))
        return date_dir

def main(mount_point):
    '''Storage dir = dir on the computer where data will be stored
    External dir = dir from which data came'''
    field_data_dir = '/Users/admin/Scripts/test'
    original_card = ''

    # Make/get date superdirectory under field data directory
    date_storage_dir = get_date_dir(field_data_dir)

    # Get SD card name
    card_name = get_card_name()

    # Make SD card dir; returns False if directory DOES exist
    card_storage_dir = get_card_storage_dir(date_storage_dir, card_name)
    if not card_storage_dir: return

    # Get mount point of card itself
    card_mount_point = get_card_mount_point(mount_point, card_name)

    #If can't find mount point, exit the program
    if not card_mount_point: return

    print("---")
    print("Files will be copied from {} to {}.".format(card_mount_point, card_storage_dir))
    proceed = raw_input("If this looks correct, press ENTER to proceed (or ^C to quit).")

    # Copy the data
    copy_wavs(card_mount_point, card_storage_dir)

    # Rename the data
    print("Renaming files.")
    rename_wavs(card_storage_dir)

main(_MAC_MOUNT_POINT)
                                                                                                      234,23        All
