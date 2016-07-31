
import __init__
import zipfile
import glob, os

zipFName = 'parasol_v%s.zip'%__init__.__version__.strip()


# open the zip file for writing, and write stuff to it

file = zipfile.ZipFile(zipFName, "w")

for name in glob.glob("*.py"):
    if name != 'make_zip.py':
        file.write(name, os.path.basename(name), zipfile.ZIP_DEFLATED)

file.close()

# open the file again, to see what's in it

file = zipfile.ZipFile(zipFName, "r")
for info in file.infolist():
    print info.filename, info.date_time, info.file_size, info.compress_size

