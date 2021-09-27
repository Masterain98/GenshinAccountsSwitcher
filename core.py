import time
import winreg
# pip install pywin32
import win32security
import os
import codecs
from languages import *


def SaveCurrentRegeditData(backupFileName):
    """
    :param backupFileName: New backup file name to be created
    :return:
    True: create new backup file successfully
    False: Failed to create new backup file
    """
    userSID = getSID()
    genshinPATH = userSID + "\SOFTWARE\miHoYo\原神"
    # print(genshinPATH)
    PowershellBackupCommand = "reg export HKU\\" + genshinPATH + " " + os.getcwd() + "/backups/" + backupFileName + ".reg -y"
    # print("CMD: " + PowershellBackupCommand)
    try:
        os.system(PowershellBackupCommand)
        return True
    except:
        return False

    '''
    # Way to enum reg
    hKey = winreg.OpenKey(winreg.HKEY_USERS, genshinPATH)
    try:
        count = 0
        while 1:
            name, value, type = winreg.EnumValue(hKey, count)
            print(name)
            count = count + 1
    except WindowsError as err:
        print(err)
        pass
    '''


def RestoreDataFromFile(backupFileName):
    """
    :param backupFileName: backup file name without .reg
    :return: True when success, False when failed
    """
    updateSID(backupFileName)
    PowershellRestoreCommand = 'reg import ' + ' "' + os.getcwd() + '/backups/' + backupFileName + '.reg"'
    try:
        os.system(PowershellRestoreCommand)
        return True
    except:
        return False


def getSID():
    # https://stackoverflow.com/questions/61886730/in-python-how-can-i-get-current-users-sid-in-windows
    desc = win32security.GetFileSecurity(
        ".", win32security.OWNER_SECURITY_INFORMATION
    )
    sid = desc.GetSecurityDescriptorOwner()

    # https://www.programcreek.com/python/example/71691/win32security.ConvertSidToStringSid
    sidstr = win32security.ConvertSidToStringSid(sid)
    assert isinstance(sidstr, object)
    return sidstr


def getBackupFiles():
    files = os.listdir(os.getcwd() + "/backups/")
    backupFiles = []
    for file in files:
        if ".reg" in file:
            createTime = time.ctime(os.stat(os.getcwd() + "/backups/" + file).st_mtime)
            ModifyTime = time.ctime(os.stat(os.getcwd() + "/backups/" + file).st_ctime)
            currentFileData = {"name": file, "create_time": createTime, "modify_time": ModifyTime}
            backupFiles.append(currentFileData)
    return backupFiles


def runGenshinWithTXT():
    file = open(os.getcwd() + "/backups/path.txt")
    path = file.readlines()[0]
    try:
        os.startfile(path + r"/YuanShen.exe")
        print("Genshin launched!")
    except WindowsError:
        print("Genshin failed launched for Windows Error!")


def deleteBackupFile(backupFileName):
    """
    :param backupFileName: name of backup file that need to be deleted
    :return:
    Ture: If delete successfully
    False: If failed to delete
    """
    # print("User is trying to delete " + backupFileName + ".reg")
    os.remove(os.getcwd() + "/backups/" + backupFileName + ".reg")
    return True


def runGenshin():
    """
    :return:
    1 : Run successfully
    2 : No link in the folder
    3 : Windows Error (user cancel the program)
    4 : Unknown Error
    """
    files = os.listdir(os.getcwd())
    if "YuanShen.lnk" not in files:
        return 2
    else:
        try:
            os.startfile("YuanShen.lnk")
            return 1
        except WindowsError:
            return 3
        except:
            return 4


def updateSID(backupFileName):
    file = open(os.getcwd() + "/backups/" + backupFileName + ".reg", 'r+', encoding="UTF-16", errors='ignore')
    lines = file.readlines()
    lines[2] = "[HKEY_USERS\\" + getSID() + "\SOFTWARE\miHoYo\原神]\n"
    file.close()
    file = open(os.getcwd() + "/backups/" + backupFileName + ".reg", 'w+', encoding="UTF-16", errors='ignore')
    file.writelines(lines)
    file.close()