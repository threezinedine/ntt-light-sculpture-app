import os
import sys
import logging
import datetime
import argparse
import subprocess

# ================== DIRECTORIES RELATED SETTINGS =================
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.normpath(os.path.join(PROJECT_DIR, "temp"))

APP_DIR = os.path.normpath(os.path.join(PROJECT_DIR, "app"))
UIS_DIR = os.path.normpath(os.path.join(APP_DIR, "uis"))
CONVERTED_UIS_DIR = os.path.normpath(os.path.join(APP_DIR, "converted_uis"))
VENV_DIR = os.path.normpath(os.path.join(APP_DIR, "venv"))
SCRIPT_DIR = os.path.normpath(os.path.join(VENV_DIR, "Scripts"))
# =================================================================

# ================== CONSTANTS RELATED SETTINGS ===================
LOGGER_NAME = "config"
SCRIPT_EXTENSION = ".exe" if sys.platform == "win32" else ""
# =================================================================

# ================== LOGGER RELATED SETTINGS ======================
logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "[%(levelname)-5s] %(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
# ================================================================

# ================== EXECUTABLES RELATED SETTINGS ================
PYQT5_TOOL_EXE_PATH = os.path.normpath(
    os.path.join(
        SCRIPT_DIR,
        "pyqt5-tools" + SCRIPT_EXTENSION,
    )
)

PYUIC5_EXE_PATH = os.path.normpath(
    os.path.join(
        SCRIPT_DIR,
        "pyuic5" + SCRIPT_EXTENSION,
    )
)

APPLICATION_PYTHON_EXE_PATH = os.path.normpath(
    os.path.join(
        SCRIPT_DIR,
        "python" + SCRIPT_EXTENSION,
    )
)
# ================================================================


def get_last_modified_timestamp(file_name: str) -> datetime.datetime:
    """
    Cross-platform method to get the last modified timestamp of a file.
    """
    if sys.platform == "win32":
        return os.path.getmtime(file_name)
    else:
        return os.path.getmtime(file_name)


def get_timestamp_file_path(file_name: str) -> str:
    relative_file_name = os.path.relpath(file_name, PROJECT_DIR)
    relative_dir = os.path.dirname(relative_file_name)
    raw_file_name = os.path.split(relative_file_name)[-1]

    # creating the folder recursively
    folders = os.path.split(relative_dir)
    tempFolder = TEMP_DIR

    try:
        for folder in folders:
            tempFolder = os.path.normpath(
                os.path.join(
                    tempFolder,
                    folder,
                )
            )

            if not os.path.exists(tempFolder):
                logger.debug(
                    f'Creating the "{os.path.relpath(tempFolder, PROJECT_DIR)}" directory...'
                )
                os.makedirs(tempFolder)

    except Exception as e:
        logger.error(f'Error while creating the stamp file for "{file_name}": {e}')
        exit(1)

    return os.path.normpath(
        os.path.join(
            TEMP_DIR,
            relative_dir,
            f"{raw_file_name}.stamp",
        )
    )


def check_a_file_is_modified(file_name: str) -> bool:
    """
    Assume that the file exists. If the stamp file does not exist or the stamp file is older than
        the modified time of the file, then return True.
    """
    stamp_file = get_timestamp_file_path(file_name)
    if not os.path.exists(stamp_file):
        return True

    return get_last_modified_timestamp(file_name) > get_last_modified_timestamp(
        stamp_file
    )


def update_stamp_file_of_a_file(file_name: str) -> None:
    """
    Update the stamp file of a file.
    """
    stamp_file = get_timestamp_file_path(file_name)

    with open(stamp_file, "w") as f:
        f.write("")


def create_application_virtual_environment() -> None:
    if not os.path.exists(VENV_DIR):
        logger.info(
            "Virtual environment for the application does not exist, creating it..."
        )

        try:
            logger.info(
                f"Creating the virtual environment in {os.path.relpath(VENV_DIR, APP_DIR)}..."
            )
            subprocess.run(
                f"python -m venv {os.path.relpath(VENV_DIR, APP_DIR)}".split(" "),
                cwd=APP_DIR,
                check=True,
            )
            logger.info(
                f"The virtual environment in {os.path.relpath(VENV_DIR, APP_DIR)} has been created."
            )

            logger.info(f"Start downloading the dependencies...")
            subprocess.run(
                f"{APPLICATION_PYTHON_EXE_PATH} -m pip install -r requirements.txt".split(
                    " "
                ),
                cwd=APP_DIR,
                check=True,
            )
            logger.info(f"The dependencies have been downloaded successfully.")
        except Exception as e:
            logger.error(f"Error while creating the virtual environment: {e}")
            exit(1)
    else:
        logger.info("Virtual environment for the application already exists.")


def create_folder_if_not_exists(
    path: str,
    base_folder: str,
    is_file: bool = False,
    file_content: str = "",
) -> None:
    if not os.path.exists(path):
        try:
            logger.info(
                f'The "{os.path.relpath(path, base_folder)}" directory does not exist, creating it...'
            )
            if is_file:
                with open(path, "w") as f:
                    f.write(file_content)
                logger.info(
                    f'The "{os.path.relpath(path, base_folder)}" file has been created.'
                )
            else:
                os.makedirs(path)
                logger.info(
                    f'The "{os.path.relpath(path, base_folder)}" directory has been created.'
                )
        except Exception as e:
            logger.error(
                f'Error while creating the "{os.path.relpath(path, base_folder)}" directory: {e}'
            )
            exit(1)


def convert_ui_files() -> None:
    logger.info("Converting the ui files...")

    create_folder_if_not_exists(CONVERTED_UIS_DIR, APP_DIR)
    create_folder_if_not_exists(
        os.path.normpath(
            os.path.join(
                CONVERTED_UIS_DIR,
                "__init__.py",
            ),
        ),
        APP_DIR,
        is_file=True,
    )

    logger.info("Setup for converting is done. Starting the conversion...")

    ui_files = [
        os.path.normpath(os.path.join(UIS_DIR, file))
        for file in os.listdir(UIS_DIR)
        if file.endswith(".ui")
    ]
    for ui_file in ui_files:
        if not check_a_file_is_modified(ui_file):
            continue

        try:
            logger.debug(f'Converting "{os.path.relpath(ui_file, APP_DIR)}"...')
            converted_ui_path = os.path.normpath(
                os.path.join(
                    CONVERTED_UIS_DIR,
                    os.path.basename(ui_file).replace(".ui", ".py"),
                )
            )
            subprocess.run(
                f"{PYUIC5_EXE_PATH} {ui_file} -o {converted_ui_path}",
                cwd=PROJECT_DIR,
                shell=True,
                check=True,
            )
            logger.debug(
                f'The "{os.path.relpath(ui_file, APP_DIR)}" has been converted.'
            )
            update_stamp_file_of_a_file(ui_file)
        except Exception as e:
            logger.error(
                f'Error while converting "{os.path.relpath(ui_file, APP_DIR)}": {e}'
            )

    logger.info("The conversion is done.")


def open_designer() -> None:
    logger.info("Opening the designer...")
    try:
        subprocess.run(
            f"{PYQT5_TOOL_EXE_PATH} designer".split(" "),
            cwd=APP_DIR,
        )
    except Exception as e:
        logger.error(f"Error while opening the designer: {e}")
        exit(1)


def run_application() -> None:
    logger.info("Running the application ...")
    try:
        application_path = os.path.normpath(os.path.join(APP_DIR, "application.py"))
        subprocess.run(
            f"{APPLICATION_PYTHON_EXE_PATH} {application_path}".split(" "),
            cwd=APP_DIR,
            check=True,
        )
        logger.info(f"The application has been closed.")
    except Exception as e:
        logger.error(
            f'Error while running the "{os.path.relpath(application_path, APP_DIR)}": {e}'
        )
        exit(1)


def main():
    # ================== APPLICATION RELATED SETTINGS ================
    # check the existence of application folder
    if not os.path.exists(APP_DIR):
        logger.error(
            f'The "{os.path.relpath(APP_DIR, PROJECT_DIR)}" directory does not exist.'
        )
        exit(1)

    create_application_virtual_environment()
    create_folder_if_not_exists(TEMP_DIR, PROJECT_DIR)

    # ================== ARGUMENTS RELATED SETTINGS ==================
    parser = argparse.ArgumentParser(
        description="The configuration helper for the current project"
    )

    parser.add_argument("action", choices=["designer", "run", "convert"])

    args = parser.parse_args()

    if args.action == "designer":
        open_designer()
    elif args.action == "run":
        convert_ui_files()
        run_application()
    elif args.action == "convert":
        convert_ui_files()
    # ================================================================


if __name__ == "__main__":
    main()
