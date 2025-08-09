import os

from constants import (
    APP_DATA_KEY,
    APPLICATION_DATA_FILE,
    APPLICATION_DATA_FOLDER,
    PROJECT_DATA_FILE,
)


def GetApplicationDataFolder() -> str:
    return os.path.join(os.environ[APP_DATA_KEY], APPLICATION_DATA_FOLDER)


def GetApplicationDataFile() -> str:
    return os.path.join(GetApplicationDataFolder(), APPLICATION_DATA_FILE)


def GetProjectDataFolder(projectDirectory: str, projectName: str) -> str:
    return os.path.normpath(os.path.join(projectDirectory, projectName))


def GetProjectDataFile(projectDirectory: str, projectName: str) -> str:
    return os.path.normpath(
        os.path.join(
            GetProjectDataFolder(projectDirectory, projectName), PROJECT_DATA_FILE
        )
    )
