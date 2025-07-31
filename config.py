import os
import sys
import logging
import argparse
import subprocess


def main():
    # ================== DIRECTORIES RELATED SETTINGS =================
    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

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
        "[%(levelname)-5s] %(asctime)s - %(filename)15s:%(lineno)-4d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    # ================================================================

    # check if current platform is windows or linux
    pyqt5_tool_exe_path = os.path.normpath(
        os.path.join(
            SCRIPT_DIR,
            "pyqt5-tools" + SCRIPT_EXTENSION,
        )
    )

    pyuic5_exe_path = os.path.normpath(
        os.path.join(
            SCRIPT_DIR,
            "pyuic5" + SCRIPT_EXTENSION,
        )
    )

    python_exe_path = os.path.normpath(
        os.path.join(
            SCRIPT_DIR,
            "python" + SCRIPT_EXTENSION,
        )
    )

    parser = argparse.ArgumentParser(
        description="The configuration helper for the current project"
    )

    parser.add_argument("action", choices=["designer", "run", "convert"])

    args = parser.parse_args()

    if args.action == "designer":
        logger.info("Opening the designer...")
        try:
            subprocess.run(
                f"{pyqt5_tool_exe_path} designer".split(" "),
                cwd=APP_DIR,
            )
        except Exception as e:
            logger.error(f"Error while opening the designer: {e}")
            exit(1)
    elif args.action == "run":
        logger.info("Running the application...")
        try:
            application_path = os.path.normpath(os.path.join(APP_DIR, "application.py"))
            subprocess.run(
                f"{python_exe_path} {application_path}".split(" "),
                cwd=APP_DIR,
            )
        except Exception as e:
            logger.error(
                f'Error while running the "{os.path.relpath(application_path, APP_DIR)}": {e}'
            )
            exit(1)
    elif args.action == "convert":
        logger.info("Converting the ui files...")

        if not os.path.exists(CONVERTED_UIS_DIR):
            logger.info(
                f'The "{os.path.relpath(CONVERTED_UIS_DIR, APP_DIR)}" directory does not exist, creating it...'
            )
            try:
                os.makedirs(CONVERTED_UIS_DIR)
                logger.info(
                    f'The "{os.path.relpath(CONVERTED_UIS_DIR, APP_DIR)}" directory has been created.'
                )
            except Exception as e:
                logger.error(
                    f'Error while creating the converted "{os.path.relpath(CONVERTED_UIS_DIR, APP_DIR)}" directory: {e}'
                )
                exit(1)

        init_py_path = os.path.normpath(os.path.join(CONVERTED_UIS_DIR, "__init__.py"))
        if not os.path.exists(init_py_path):
            logger.info(
                f'The "{os.path.relpath(init_py_path, APP_DIR)}" file does not exist, creating it...'
            )
            try:
                with open(init_py_path, "w") as f:
                    f.write("")
                logger.info(
                    f'The "{os.path.relpath(init_py_path, APP_DIR)}" file has been created.'
                )
            except Exception as e:
                logger.error(
                    f'Error while creating the "{os.path.relpath(init_py_path, APP_DIR)}" file: {e}'
                )
                exit(1)

        logger.info("Setup for converting is done. Starting the conversion...")

        # list all ui files inside the ui folder
        ui_files = [
            os.path.normpath(os.path.join(UIS_DIR, file))
            for file in os.listdir(UIS_DIR)
            if file.endswith(".ui")
        ]
        for ui_file in ui_files:
            try:
                logger.debug(f'Converting "{os.path.relpath(ui_file, APP_DIR)}"...')
                converted_ui_path = os.path.normpath(
                    os.path.join(
                        CONVERTED_UIS_DIR,
                        os.path.basename(ui_file).replace(".ui", ".py"),
                    )
                )
                subprocess.run(
                    f"{pyuic5_exe_path} {ui_file} -o {converted_ui_path}",
                    cwd=PROJECT_DIR,
                    shell=True,
                    check=True,
                )
                logger.debug(
                    f'The "{os.path.relpath(ui_file, APP_DIR)}" has been converted.'
                )
            except Exception as e:
                logger.error(
                    f'Error while converting "{os.path.relpath(ui_file, APP_DIR)}": {e}'
                )

        logger.info("The conversion is done.")


if __name__ == "__main__":
    main()
