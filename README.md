# Genshin Accounts Switcher
Account switching tool for Genshin Impact (CN Server)

## Principle

- Genshin Impact (at least in CN server) save login session data in a specific Regedit path (`\{Windows_SID}\SOFTWARE\miHoYo\原神`)
  - Using Windows commands to overwrite and export data will allows user to switch accounts easier
- In this script, the program are able to 
  - Save current login session to a `reg` backup file
    - backup files are saved in `backups` folder
  - Restore login session data from a `reg` backup file
    - The program will change the SID in the backup files in order to accept backup files comes from other Windows devices
  - Restore and run Genshin Impact Game
    - You must copy and paste a link for Yuanshen.exe, name it as `YuanShen`, and save it at this folder to make it works
    - A sample link is provided in the folder, you need to overwrite it, unless your Genshin Impact game has exact same path as I have
  - Delete backup files
    - You can actually delete it directly from `backups` folder

## Usage

- Run `main.py`
- Follow the instructions from the console output

## Language

- The program has a language package in `languages.py` in a Python dictionary format
  - Currently it has `Simplified Chinese` and `English`
  - The function will detect your local display language and try to use it as the preference
    - `English` is the default language
    - You can always overwrite it at line 184 of `main.py`

