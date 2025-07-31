import os
import sys
import logging
import argparse
import subprocess

UIS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uis")
CONVERTED_UIS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "converted_uis"
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "[%(levelname)5s] %(asctime)s - %(filename)s:%(lineno)d - %(message)s"
)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # check if current platform is windows or linux
    pyqt5_tool_exe_path = os.path.join(
        current_dir,
        "venv",
        "Scripts",
        "pyqt5-tools" + ".exe" if sys.platform == "win32" else "",
    )

    pyuic5_exe_path = os.path.join(
        current_dir,
        "venv",
        "Scripts",
        "pyuic5" + ".exe" if sys.platform == "win32" else "",
    )

    python_exe_path = os.path.join(
        current_dir,
        "venv",
        "Scripts",
        "python" + ".exe" if sys.platform == "win32" else "",
    )

    parser = argparse.ArgumentParser(
        description="The configuration helper for the current project"
    )

    parser.add_argument("action", choices=["designer", "run", "convert"])

    args = parser.parse_args()

    if args.action == "designer":
        logger.info("Opening the designer...")
        try:
            subprocess.run(f"{pyqt5_tool_exe_path} designer".split(" "))
        except Exception as e:
            logger.error(f"Error while opening the designer: {e}")
            exit(1)
    elif args.action == "run":
        logger.info("Running the application...")
        try:
            subprocess.run(f"{python_exe_path} {current_dir}/application.py".split(" "))
        except Exception as e:
            logger.error(f"Error while running the application: {e}")
            exit(1)
    elif args.action == "convert":
        logger.info("Converting the ui files...")

        if not os.path.exists(CONVERTED_UIS_DIR):
            logger.info(f"The converted ui directory does not exist, creating it...")
            try:
                os.makedirs(CONVERTED_UIS_DIR)
                logger.info(f"The converted ui directory has been created.")
            except Exception as e:
                logger.error(f"Error while creating the converted ui directory: {e}")
                exit(1)

        if not os.path.exists(os.path.join(CONVERTED_UIS_DIR, "__init__.py")):
            logger.info(f"The __init__.py file does not exist, creating it...")
            try:
                with open(os.path.join(CONVERTED_UIS_DIR, "__init__.py"), "w") as f:
                    f.write("")
                logger.info(f"The __init__.py file has been created.")
            except Exception as e:
                logger.error(f"Error while creating the __init__.py file: {e}")
                exit(1)

        logger.info("Setup for converting is done. Starting the conversion...")

        # list all ui files inside the ui folder
        ui_files = [
            os.path.join(UIS_DIR, file)
            for file in os.listdir(UIS_DIR)
            if file.endswith(".ui")
        ]
        for ui_file in ui_files:
            try:
                logger.debug(f"Converting {ui_file}...")
                subprocess.run(
                    f"{pyuic5_exe_path} {ui_file} -o {CONVERTED_UIS_DIR}/{os.path.basename(ui_file).replace('.ui', '.py')}",
                    shell=True,
                )
                logger.debug(f"The {ui_file} has been converted.")
            except Exception as e:
                logger.error(f"Error while converting {ui_file}: {e}")

        logger.info("The conversion is done.")
