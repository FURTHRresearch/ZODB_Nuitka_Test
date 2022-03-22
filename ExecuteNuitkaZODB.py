import os
import subprocess
filePath = os.path.abspath(__file__)
dirName = os.path.dirname(filePath)
from CreateZip import createZip

print(dirName)


commandList = ["-m", "nuitka",
               # "--include-package-data=persistent",
               # "--include-package-data=ZODB",
               "--include-package=persistent",

               "--standalone",
               "--msvc=14.3",
               "--lto=no",
               f"{dirName}/ZODB_Nuitka_Test.py"]


runList = ["pipenv", "run", "python",]
runList.extend(commandList)
subprocess.run(runList)
filePathList = [f"ZODB_Nuitka_Test.dist"]
zipFilePath = f"ZODB_Nuitka_Test.zip"
createZip(filePathList, zipFilePath)
