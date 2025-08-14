import os

from constants import (
    APP_DATA_KEY,
    APPLICATION_DATA_FILE,
    APPLICATION_DATA_FOLDER,
    PROJECT_DATA_FILE,
    TEST_NEW_PROJECT_PATH,
)


def GetApplicationDataFolder() -> str:
    return os.path.join(os.environ[APP_DATA_KEY], APPLICATION_DATA_FOLDER)


def GetApplicationDataFile() -> str:
    return os.path.join(GetApplicationDataFolder(), APPLICATION_DATA_FILE)


def GetProjectDataFolder(projectDirectory: str, projectName: str) -> str:
    return os.path.normpath(os.path.join(projectDirectory, projectName))


def GetTestProjectDataFolder(projectName: str) -> str:
    return os.path.join(TEST_NEW_PROJECT_PATH, projectName)


def GetProjectDataFile(projectDirectory: str, projectName: str) -> str:
    return os.path.normpath(
        os.path.join(
            GetProjectDataFolder(projectDirectory, projectName), PROJECT_DATA_FILE
        )
    )


def GetProjectNameFromFilePath(projectFilePath: str) -> str:
    return os.path.split(os.path.dirname(projectFilePath))[-1]


def GetImageFileNameFromFilePath(imageFilePath: str) -> str:
    return os.path.split(imageFilePath)[-1]


def GetWindowTitle(projectName: str | None = None, isModified: bool = False) -> str:
    if projectName is None or projectName == "":
        return "Light Sculpture Studio"

    return f"Light Sculpture Studio - {projectName}{'*' if isModified else ''}"


def GetImageFolder(projectDirectory: str) -> str:
    return os.path.normpath(os.path.join(projectDirectory, "images"))


def GetImageFilePath(projectDirectory: str, imageName: str) -> str:
    return os.path.normpath(os.path.join(GetImageFolder(projectDirectory), imageName))


def GetImageNameBasedOnExistedImageNames(
    imageName: str,
    existedImageNames: list[str],
) -> str:
    finalName = imageName

    while finalName in existedImageNames:
        finalName = f"{imageName} (Copied)"

    return finalName
