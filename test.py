import os
import glob


fileList = glob.glob('*.txt', recursive=True)

for name in fileList:
    os.remove(name)
    print('delete file {}'.format(name) )