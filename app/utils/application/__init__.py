import os

from constants import APP_DATA_KEY, APPLICATION_DATA_FILE, APPLICATION_DATA_FOLDER


def GetApplicationDataFolder() -> str:
    return os.path.join(os.environ[APP_DATA_KEY], APPLICATION_DATA_FOLDER)


def GetApplicationDataFile() -> str:
    return os.path.join(GetApplicationDataFolder(), APPLICATION_DATA_FILE)
