from zipfile import ZipFile, ZIP_DEFLATED
import os


class ZipUtilities:
    def __init__(self, dirName):
        self.dirName = dirName

    def toZip(self, file, zipFile):
        if os.path.isfile(file):
            arcName = file.replace(self.dirName, "")
            zipFile.write(file, arcname=arcName)
        else:
            self.addFolderToZip(zipFile, file)

    def addFolderToZip(self, zipFile, folder):
        for file in os.listdir(folder):
            full_path = os.path.join(folder, file)
            if os.path.isfile(full_path):
                print("add file")
                arcName = full_path.replace(self.dirName, "")
                zipFile.write(full_path, arcname=arcName)
            elif os.path.isdir(full_path):
                print("add Folder")
                self.addFolderToZip(zipFile, full_path)


def createZip(pathList, zipFilePath):
    dirName = os.path.dirname(zipFilePath)

    zipUtil = ZipUtilities(dirName)
    with ZipFile(zipFilePath, "w", ZIP_DEFLATED) as zipFile:
        for file in pathList:
            zipUtil.toZip(file, zipFile)
