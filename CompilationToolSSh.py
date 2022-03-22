import sys
import time

import paramiko
from stat import S_ISDIR
import os

def compileClient(gitURL, gitBranch, rootFolderName,
                  sshHost, sshUser, sshPassword=None, sshKeyFile=None,
                  deleteCompilationFolder=True):

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if sshKeyFile is None:
        client.connect(sshHost, username=sshUser, password=sshPassword)
    else:
        client.connect(sshHost, username=sshUser, key_filename=sshKeyFile)

    gitURL = gitURL.replace("https://", "")

    sftp = client.open_sftp()
    dirList = sftp.listdir()
    totalCommandList = []
    if "Compile" not in dirList:
        stdin, stdout, stderr = client.exec_command("mkdir Compile")
        waitForCommand(stdout, stderr)

    sftp.chdir("Compile")
    dirList = sftp.listdir()
    print(dirList)
    if rootFolderName in dirList:
        stdin, stdout, stderr = client.exec_command(f"rmdir Compile\\{rootFolderName} /s /q")
        waitForCommand(stdout, stderr)

    commandList = ["cd Compile",
                   f"git clone https://{gitURL} {rootFolderName}",
                   f"cd {rootFolderName}",
                   f"git checkout {gitBranch}",
                   "mkdir .venv",
                   "pipenv.exe install",
                   "pipenv run python ExecuteNuitkaZODB.py"]

    totalCommandList.extend(commandList)
    totalCommand = ""
    for command in commandList:
        totalCommand += f"{command} && "

    # channel = client.invoke_shell()
    # stdin = channel.makefile('wb')
    # stdout = channel.makefile('rb')
    # stdin.write(totalCommand)
    # print(stdout.readlines())

    totalCommand = totalCommand[:-2]
    stdin, stdout, stderr = client.exec_command(totalCommand)
    waitForCommand(stdout, stderr)


    sftp = client.open_sftp()
    sftp.chdir(f"C:/Users/danie/Compile/{rootFolderName}")

    sftp.get("ZODB_Nuitka_TestZODB_Nuitka_Test.zip", "ZODB_Nuitka_Test.zip")
    sftp.close()

    if deleteCompilationFolder:
        client.exec_command(f"rmdir Compile/{rootFolderName} /s /q")
    client.close()


def waitForCommand(stdout, stderror):
    lineBuf = ""
    ready = stdout.channel.exit_status_ready()
    while not ready: # Blocking call
        lineBufByte = stdout.read(1)
        lineBuf += lineBufByte.decode("utf-8")
        if lineBuf.endswith("\n"):
            print(lineBuf)
            lineBuf = ""

        # time.sleep(1)
        ready = stdout.channel.exit_status_ready()
        # print(1)



    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        print(stdout.readlines())
        return 
    else:
        raise ValueError(stderror.readlines())

def isdir(path, sftp):
    try:
        return S_ISDIR(sftp.stat(path).st_mode)
    except IOError:
        return False

def rm(path, sftp):
    files = sftp.listdir(path=path)

    for f in files:
        filepath = os.path.join(path, f)
        if isdir(filepath, sftp):
            rm(filepath, sftp)
        else:
            sftp.remove(filepath)

if __name__ == "__main__":
    gitURL = "https://github.com/FURTHRresearch/ZODB_Nuitka_Test.git"
    gitBranch = "main"
    host = "10.10.10.3"
    user = "danie"
    keyPath = r"C:\users\danie\.ssh\office"

    compileClient(gitURL, gitBranch, "ZODB_Nuitka_Test", host, user, sshKeyFile=keyPath,
                  deleteCompilationFolder=False)




