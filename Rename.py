from pathlib import Path

file = Path(r"C:\Users\Mr_Guo\Desktop\bootyfullsebi")
for n,f in enumerate(file.iterdir()):
    name = file / f.parent.name
    if f.suffix == '.jpg':
        f.rename(str(name)+ '_' + str(n+1) + ".jpg")

# test
