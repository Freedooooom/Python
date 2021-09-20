from pathlib import Path
import os
import time

TimeStamp = time.mktime(time.strptime("2013-10-10 23:40:00","%Y-%m-%d %H:%M:%S"))

def ModifyFile(dirstr:str):
    dirname = Path(dirstr)
    for f in dirname.iterdir():
        if f.is_file():
            os.utime(f,(TimeStamp,TimeStamp))
        else:
            os.utime(f,(TimeStamp,TimeStamp))
            ModifyFile(dirname/f)
            
if __name__ == "__main__":
    ModifyFileDir = input("Your want modify file path >> ")
    
    ModifyFile (ModifyFileDir)