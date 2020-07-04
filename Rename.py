from pathlib import Path
import shutil
from shutil import ignore_patterns

def rename(srcdir:str):
    file = Path(srcdir)
    for n,f in enumerate(file.iterdir()):
        name = file / f.parent.name
        if f.suffix == '.jpg':
            f.rename(str(name)+ '_' + str(n+1) + ".jpg")


def copyfile(src:str,dst:str,ignore:str):
    srcdir = Path(src)
    dstdir = Path(dst)

    shutil.copytree(srcdir,dstdir,ignore=shutil.ignore_patterns(ignore))
