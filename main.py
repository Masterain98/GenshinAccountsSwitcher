import string
import time

import core
import locale
from languages import *


def menuHeader():
    # Welcome statements
    print("=" * 30)
    print("GenshinAccountSwitcher")
    print("=" * 30)


def mainMenu():
    print(MainMenu[language])
    userInput = input(MainMenuUserInputPrompt[language])
    if userInput.lower() == "l":
        loadBackups()
    elif userInput.lower() == "r":
        runGameBackup()
    elif userInput.lower() == "s":
        saveNewBackup()
    elif userInput.lower() == "d":
        deleteBackup()
    else:
        print(UserInputError[language])


def loadBackups():
    count = 1
    getCorrectInput = False
    backupsData = core.getBackupFiles()
    if len(backupsData) != 0:
        print("\n" + "=" * 30)
        print(ShowCurrentBackup[language])
        for backups in backupsData:
            print(str(count) + ". " + backups["name"].replace(".reg", ""))
            count += 1

        while not getCorrectInput:
            try:
                userInput = input(DigitsUserInputPrompt[language])
                if str(userInput.lower()) == "q":
                    print("\n" * 50)
                    mainMenu()
                elif 0 < int(userInput) <= len(backupsData):
                    userInput = int(userInput)
                    getCorrectInput = True
            except:
                print(UserInputError[language])

        restoreTargetName = backupsData[userInput - 1]["name"].replace(".reg", "")
        # print("User Trying to restore: " + restoreTargetName)
        # Core function
        result = core.RestoreDataFromFile(restoreTargetName)
        if result:
            print(RestoreSuccessfully[language])
        else:
            print(RestoreFailed[language])
        time.sleep(1)
        print("\n" * 3)
        mainMenu()
    else:
        print(NoBackupError[language])
        mainMenu()


def runGameBackup():
    count = 1
    getCorrectInput = False
    backupsData = core.getBackupFiles()
    print(RunGameMenuPrompt[language])
    if len(backupsData) != 0:
        print("\n" + "=" * 30)
        print(ShowCurrentBackup[language])
        for backups in backupsData:
            print(str(count) + ". " + backups["name"].replace(".reg", ""))
            count += 1

        while not getCorrectInput:
            try:
                userInput = input(DigitsUserInputPrompt[language])
                if str(userInput.lower()) == "q":
                    print("\n" * 50)
                    mainMenu()
                elif 0 < int(userInput) <= len(backupsData):
                    userInput = int(userInput)
                    getCorrectInput = True
            except:
                print(UserInputError[language])

        restoreTargetName = backupsData[userInput - 1]["name"].replace(".reg", "")
        # print("User Trying to restore: " + restoreTargetName)
        # Core function
        result = core.RestoreDataFromFile(restoreTargetName)
        if result:
            print(RestoreSuccessfully[language])
            runResult = core.runGenshin()
            if runResult == 1:
                print(StartGamePrompt[language])
            elif runResult == 2:
                print(NoLinkError[language])
            elif runResult == 3:
                print(UserCancelError[language])
            else:
                print(UnknownErrorPrompt[language])
        else:
            print(RestoreFailed[language])
        time.sleep(1)
        print("\n" * 3)
        mainMenu()
    else:
        print(NoBackupError[language])
        mainMenu()


def saveNewBackup():
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    # print(valid_chars)
    all_valid_char = False

    while not all_valid_char:
        all_valid_char = True
        userInput = input(NewBackupNamePrompt[language])
        for char in userInput:
            if char not in valid_chars:
                print(char + NotValidCharError[language] + "\n")
                all_valid_char = False
                break

    result = core.SaveCurrentRegeditData(userInput)
    if result:
        print(NewBackupCreated[language])
    else:
        print(UnknownErrorPrompt[language])
    print("\n" * 3)
    mainMenu()


def deleteBackup():
    count = 1
    getCorrectInput = False
    backupsData = core.getBackupFiles()
    if len(backupsData) != 0:
        print("\n" + "=" * 30)
        print(ShowCurrentBackup[language])
        for backups in backupsData:
            print(str(count) + ". " + backups["name"].replace(".reg", ""))
            count += 1

        while not getCorrectInput:
            try:
                userInput = input(DeleteBackupPrompt[language])
                if str(userInput.lower()) == "q":
                    print("\n" * 50)
                    mainMenu()
                elif 0 < int(userInput) <= len(backupsData):
                    userInput = int(userInput)
                    getCorrectInput = True
            except:
                print(UserInputError[language])

        fileNameToBeDeleted = backupsData[userInput-1]["name"].replace(".reg", "")
        result = core.deleteBackupFile(fileNameToBeDeleted)
        if result:
            print(DeleteBackupSuccessfully[language])
        else:
            print(DeleteBackupFailed[language])
        print("\n" * 3)
        mainMenu()
    else:
        print(NoBackupError[language])


if __name__ == "__main__":
    backupsData = core.getBackupFiles()
    print(backupsData)

    # Load language
    language = locale.getdefaultlocale()[0]
    if language not in SupportedLanguages:
        language = "en_US"

    # Welcome statements
    menuHeader()

    # Main Menu
    mainMenu()
