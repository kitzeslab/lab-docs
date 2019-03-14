'''
TODO: before using
- EST/DST problems?

TODO: potential next steps
- Date & time to directory structure
- Split files to decrease their length 
  (split files should NOT be backed up--we should always retain
  original copies of the files)
- Name split files
'''
                       

import time

def rename_hex_filename(fname):
    '''
    '5B7E8A14-000128.split.WAV' --> '20190220_070000'
    '''

    hex_name = fname.split('-')[0]
    seconds = int(hex_name, 16)
    
    return time.strftime('%Y%m%d_%H%M%S', time.localtime(seconds))
