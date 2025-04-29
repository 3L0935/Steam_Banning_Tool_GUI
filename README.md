# Steam_Ban_GUI

A graphical tool to interface with the Steam Banning API — this upgraded fork of [KillaBoi's Steam Banning API](https://github.com/KillaBoi/Steam-Banning-API) introduces a full-featured GUI using Python's `tkinter` and `Pillow`. Easily fetch player information, issue bans, or revoke them, all from a *modern* visual interface.

## 🧰 Features

- 🔍 Retrieve Steam user information via SteamID64 or profile URL  
- 🚫 Ban players (temporary or permanent) with optional cheat descriptions  
- ✅ Unban players via a single click  
- 📊 View ban history (VAC, Game, Economy, Last Ban)  
- 🪟 Simple, clean GUI with background theming  
- 🧾 Built-in logging area for all actions and responses
- 🌄 Modular background (although, a dark one will work better 👀)   

## 🛠 Requirements

- Python 3.8 or newer  
- A valid [Steam Web API Key](https://steamcommunity.com/dev/apikey)  
- Your game’s `AppID`  

## 📦 Dependencies

Install the required packages via pip:

```
pip install pillow requests
```

## 🚀 Setup

Before running, edit Steam_Ban_GUI_V3.py and replace:

```
api_key = "YOUR_API_KEY"
appid = "GAME_APPID"
```
with your API key and app ID, then you'll be able to run it with:

python Steam_Ban_GUI_V3.py

## 🏗 Build Instructions (Windows Executable)

To build a standalone .exe using PyInstaller, use the following command:

### for windows🪟 :

```
pyinstaller --onefile --windowed \
    --hidden-import=PIL \
    --hidden-import=PIL._tkinter_finder \
    --hidden-import=tkinter \
    --hidden-import=PIL.Image \
    --hidden-import=PIL.ImageTk \
    --add-data "background.png;." \
    --icon=BAN.ico \
    Steam_Ban_GUI_V3.py
```

### for linux 🐧:
```
pyinstaller --onefile --windowed \
    --hidden-import=PIL \
    --hidden-import=PIL._tkinter_finder \
    --hidden-import=tkinter \
    --hidden-import=PIL.Image \
    --hidden-import=PIL.ImageTk \
    --add-data "background.png:." \
    --icon=BAN.ico \
    Steam_Ban_GUI_V3.py
```

This will create a standalone .exe inside the dist/ folder.
Note: Make sure background.png and BAN.ico are located in the same directory as the script during the build process.

## 📄 License

This project is distributed under the original license from KillaBoi’s Steam-Banning-API. If you fork or distribute, please maintain credit to the original author.

## 🙋‍♂️ Disclaimer

This tool is intended for developers or administrators of games integrated with Steam's partner API. Abuse of the banning system may violate Steamworks terms.
