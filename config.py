import os
import sys
import shutil
import logging
import datetime
import argparse
import subprocess
from glob import glob
from typing import List

# ================== CONSTANTS RELATED SETTINGS ===================
CLANG_PATH_KEY = "CLANG_PATH"
# =================================================================

# ================== DIRECTORIES RELATED SETTINGS =================
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.normpath(os.path.join(PROJECT_DIR, "temp"))

APP_DIR = os.path.normpath(os.path.join(PROJECT_DIR, "app"))
UIS_DIR = os.path.normpath(os.path.join(APP_DIR, "uis"))
CONVERTED_UIS_DIR = os.path.normpath(os.path.join(APP_DIR, "converted_uis"))
ENGINE_BINDING_DIR = os.path.normpath(os.path.join(APP_DIR, "Engine"))

ENGINE_DIR = os.path.normpath(os.path.join(PROJECT_DIR, "engine"))
ENGINE_BUILD_DIR = os.path.normpath(os.path.join(ENGINE_DIR, "build"))
ENGINE_INSTALL_DIR = os.path.normpath(os.path.join(PROJECT_DIR, "install"))

AUTOGEN_DIR = os.path.normpath(os.path.join(PROJECT_DIR, "autogen"))
AUTOGEN_TEMPLATE_DIR = os.path.normpath(os.path.join(AUTOGEN_DIR, "templates"))
# =================================================================

# ================== CONSTANTS RELATED SETTINGS ===================
LOGGER_NAME = "CONFIG"
SCRIPT_EXTENSION = ".exe" if sys.platform == "win32" else ""
# =================================================================

# ================== LOGGER RELATED SETTINGS ======================
logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "[%(levelname)-5s] - [%(name)-7s] - %(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
# ================================================================


# ================== VENV RELATED SETTINGS ========================
def get_venv_dir(folder: str) -> str:
    return os.path.normpath(os.path.join(folder, "venv"))


def get_script_dir(folder: str) -> str:
    return os.path.normpath(os.path.join(get_venv_dir(folder), "Scripts"))


def get_python_exe_path(folder: str) -> str:
    return os.path.normpath(
        os.path.join(get_script_dir(folder), "python" + SCRIPT_EXTENSION)
    )


def get_pytest_exe_path(folder: str) -> str:
    return os.path.normpath(
        os.path.join(get_script_dir(folder), "pytest" + SCRIPT_EXTENSION)
    )


def get_requirements_file_path(folder: str) -> str:
    return os.path.normpath(os.path.join(folder, "requirements.txt"))


# ================================================================

# ================== EXECUTABLES RELATED SETTINGS ================
PYQT6_TOOL_EXE_PATH = os.path.normpath(
    os.path.join(
        get_script_dir(APP_DIR),
        "pyqt6-tools" + SCRIPT_EXTENSION,
    )
)

PYUIC6_EXE_PATH = os.path.normpath(
    os.path.join(
        get_script_dir(APP_DIR),
        "pyuic6" + SCRIPT_EXTENSION,
    )
)

APPLICATION_PYTHON_EXE_PATH = os.path.normpath(
    os.path.join(
        get_script_dir(APP_DIR),
        "python" + SCRIPT_EXTENSION,
    )
)
# ================================================================


def get_last_modified_timestamp(file_name: str) -> datetime.datetime:
    """
    Cross-platform method to get the last modified timestamp of a file.
    """
    if sys.platform == "win32":
        return datetime.datetime.fromtimestamp(os.path.getmtime(file_name))
    else:
        return datetime.datetime.fromtimestamp(os.path.getmtime(file_name))


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


def system_health_check() -> None:
    try:
        subprocess.run(
            f"cmake --version".split(" "),
            cwd=ENGINE_DIR,
            shell=True,
            check=True,
        )
        logger.info("CMake is installed and ready to use.")
    except Exception as e:
        logger.error(f"Error with your CMake, the project cannot be run: {e}")
        exit(1)

    try:
        subprocess.run(
            f"python --version".split(" "),
            cwd=ENGINE_DIR,
            shell=True,
            check=True,
        )
        logger.info("Python is installed and ready to use.")
    except Exception as e:
        logger.error(f"Error with your Python, the project cannot be run: {e}")
        exit(1)

    try:
        subprocess.run(
            f"git --version".split(" "),
            cwd=ENGINE_DIR,
            shell=True,
            check=True,
        )
        logger.info("Git is installed and ready to use.")
    except Exception as e:
        logger.error(f"Error with your Git, the project cannot be run: {e}")
        exit(1)

    try:
        subprocess.run(
            f"clang --version".split(" "),
            cwd=ENGINE_DIR,
            shell=True,
            check=True,
        )
    except Exception as e:
        logger.error(f"Error with your Clang, the project cannot be run: {e}")
        exit(1)


def create_virtual_environment(folder: str) -> None:
    venv_dir = get_venv_dir(folder)
    python_exe_path = get_python_exe_path(folder)

    if not os.path.exists(venv_dir):
        logger.info(
            f'Virtual environment for the "{os.path.relpath(folder, PROJECT_DIR)}" does not exist, creating it...'
        )

        try:
            logger.info(
                f'Creating the virtual environment in "{os.path.relpath(folder, PROJECT_DIR)}"...'
            )
            subprocess.run(
                f"python -m venv {os.path.relpath(venv_dir, folder)}".split(" "),
                cwd=folder,
                check=True,
            )
            logger.info(
                f'The virtual environment in "{os.path.relpath(folder, PROJECT_DIR)}" has been created.'
            )

            requirements_file = get_requirements_file_path(folder)
            if os.path.exists(requirements_file):
                logger.info(f"Start downloading the dependencies...")
                subprocess.run(
                    f"{python_exe_path} -m pip install -r requirements.txt".split(" "),
                    cwd=folder,
                    check=True,
                )
                logger.info(f"The dependencies have been downloaded successfully.")
            else:
                logger.warning(
                    f'The "{os.path.relpath(requirements_file, folder)}" file does not exist, skipping the dependencies download.'
                )
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
                f"{PYUIC6_EXE_PATH} {ui_file} -o {converted_ui_path}",
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
            f"{PYQT6_TOOL_EXE_PATH} designer".split(" "),
            cwd=APP_DIR,
        )
    except Exception as e:
        logger.error(f"Error while opening the designer: {e}")
        exit(1)


def run_application() -> None:
    logger.info("Running the application ...")
    try:
        application_path = os.path.normpath(os.path.join(APP_DIR, "application.py"))  # type: ignore
        subprocess.run(
            f"{APPLICATION_PYTHON_EXE_PATH} {application_path}".split(" "),
            cwd=APP_DIR,
            check=True,
        )
        logger.info(f"The application has been closed.")
    except Exception as e:
        logger.error(
            f'Error while running the "{os.path.relpath(application_path, APP_DIR)}": {e}'  # type: ignore
        )
        exit(1)


def update_requirements(folder: str) -> None:
    python_exe_path = get_python_exe_path(folder)
    requirements_file = get_requirements_file_path(folder)

    try:
        logger.info(
            f'Updating the requirements to the file "{os.path.relpath(requirements_file, PROJECT_DIR)}"...'
        )
        subprocess.run(
            f"{python_exe_path} -m pip freeze > {requirements_file}".split(" "),
            shell=True,
            cwd=folder,
            check=True,
        )
        logger.info(
            f'The requirements file "{os.path.relpath(requirements_file, PROJECT_DIR)}" has been updated successfully.'
        )
    except Exception as e:
        logger.error(
            f'Error while updating the "{os.path.relpath(requirements_file, PROJECT_DIR)}" file: {e}'
        )
        exit(1)


def clone_vendor_libraries() -> None:
    logger.info("Cloning the vendor libraries...")

    try:
        subprocess.run(
            f"git submodule update --init --recursive".split(" "),
            cwd=ENGINE_DIR,
            shell=True,
            check=True,
        )
    except Exception as e:
        logger.error(f"Error while cloning the vendor libraries: {e}")
        exit(1)


def get_build_type(release: bool = False) -> str:
    return "Release" if release else "Debug"


def get_build_dir(release: bool = False) -> str:
    return os.path.normpath(os.path.join(ENGINE_BUILD_DIR, get_build_type(release)))


def generator_if_not_exists(release: bool = False) -> None:
    if not os.path.exists(get_build_dir(release)):
        generate_build_system(release)


def generate_build_system(release: bool = False) -> None:
    build_dir = get_build_dir(release)
    try:
        logger.info(f"Generating the build system...")
        subprocess.run(
            f"cmake -B {build_dir} -S {ENGINE_DIR} -DCMAKE_INSTALL_PREFIX={ENGINE_INSTALL_DIR} -DCMAKE_BUILD_TYPE={get_build_type(release)}".split(
                " "
            ),
            cwd=ENGINE_DIR,
            shell=True,
            check=True,
        )
        logger.info(f"The build system has been generated successfully.")
    except Exception as e:
        logger.error(f"Error while generating the build system: {e}")
        exit(1)


def copy_pyd_files(release: bool = False) -> None:
    logger.info("Copying the pyd files...")
    build_dir = get_build_dir(release)
    pyd_files = glob(os.path.join(build_dir, get_build_type(release), "*.pyd"))
    for pyd_file in pyd_files:
        try:
            logger.debug(f"Copying the {pyd_file} file...")
            shutil.copy(pyd_file, os.path.join(APP_DIR, "Engine"))
        except Exception as e:
            logger.warning(f"Error while copying the {pyd_file} file: {e}")

    logger.info("The pyd files have been copied successfully.")


def build_engine(release: bool = False) -> None:
    build_dir = get_build_dir(release)
    try:
        logger.info("Building the engine...")
        subprocess.run(
            f"cmake --build {build_dir} --config {get_build_type(release)}".split(" "),
            cwd=ENGINE_DIR,
            shell=True,
            check=True,
        )
        copy_pyd_files(release)
        logger.info(f"The engine has been built successfully.")
    except Exception as e:
        logger.error(f"Error while building the engine: {e}")
        exit(1)


def install_engine(release: bool = False) -> None:
    build_dir = get_build_dir(release)
    try:
        logger.info("Installing the engine...")
        subprocess.run(
            f"cmake --install {build_dir}".split(" "),
            cwd=ENGINE_DIR,
            shell=True,
            check=True,
        )
    except Exception as e:
        logger.error(f"Error while installing the engine: {e}")
        exit(1)


def get_all_public_headers() -> List[str]:
    engine_include_dir = os.path.normpath(os.path.join(ENGINE_DIR, "include"))

    h_files: List[str] = []
    for file in glob(os.path.join(engine_include_dir, "engine/**/*.h"), recursive=True):
        h_files.append(file)

    logger.debug(f"Found {len(h_files)} h files.")

    return h_files


def get_h_files_as_input_args() -> str:
    return " ".join([f"{file}" for file in get_all_public_headers()])


def get_libclangdll_path() -> str:
    try:
        output = subprocess.run(
            "where clang", shell=True, check=True, capture_output=True
        )
        clang_dir = os.path.dirname(output.stdout.decode("utf-8")[:-2])
        return os.path.join(clang_dir, "libclang.dll")
    except Exception as e:
        logger.error(f"Error while getting the libclang.dll path: {e}")
        exit(1)


def run_autogen(force: bool = False) -> None:
    libclangdll_path = get_libclangdll_path()

    try:
        logger.info("Running the autogen...")
        python_exe_path = get_python_exe_path(AUTOGEN_DIR)

        # ================== CHECKING MODIFICATIONS ==================
        # only run the autogen if the engine.h is modified
        all_headers = get_all_public_headers()
        has_modified_header = False
        for header in all_headers:
            if check_a_file_is_modified(header) or force:
                has_modified_header = True
                update_stamp_file_of_a_file(header)

        if not has_modified_header:
            logger.info("No header is modified, skipping the autogen.")
            return

        # ============================================================

        engine_global_public_header = os.path.normpath(
            os.path.join(ENGINE_DIR, "include", "engine", "engine.h")
        )

        # ================== BINDING RELATED SETTINGS ==================
        logger.info("Binding cpp library to python...")
        binding_output = os.path.normpath(os.path.join(ENGINE_DIR, "binding.cpp"))
        binding_template_file = os.path.normpath(
            os.path.join(AUTOGEN_TEMPLATE_DIR, "binding.j2")
        )
        subprocess.run(
            f"{python_exe_path} main.py -i {engine_global_public_header} -j {binding_template_file} -o {binding_output} -c {libclangdll_path}".split(
                " "
            ),
            cwd=AUTOGEN_DIR,
            shell=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
            check=True,
        )
        logger.info("The binding has been run successfully.")
        # ================================================================

        # ================== PYI BINDING RELATED SETTINGS ==================
        logger.info("Generating the pyi binding...")
        pyi_output = os.path.normpath(os.path.join(ENGINE_BINDING_DIR, "__init__.pyi"))
        pyi_template_file = os.path.normpath(
            os.path.join(AUTOGEN_TEMPLATE_DIR, "pyi_binding.j2")
        )
        subprocess.run(
            f"{python_exe_path} main.py -i {engine_global_public_header} -j {pyi_template_file} -o {pyi_output} -c {libclangdll_path}".split(
                " "
            ),
            cwd=AUTOGEN_DIR,
            shell=True,
            check=True,
        )
        logger.info("The pyi binding has been generated successfully.")
        # ================================================================
        logger.info("The autogen has been run successfully.")
    except Exception as e:
        logger.error(f"Error while running the autogen: {e}")
        exit(1)


def run_autogen_test() -> None:
    try:
        os.environ[CLANG_PATH_KEY] = get_libclangdll_path()
        logger.info("Running the autogen test...")
        pytest_exe_path = get_pytest_exe_path(AUTOGEN_DIR)
        subprocess.run(
            f"{pytest_exe_path}",
            cwd=AUTOGEN_DIR,
            check=True,
            shell=True,
        )
    except Exception as e:
        logger.error(f"Error while running the autogen test: {e}")
        exit(1)


def run_engine_test(release: bool = False) -> None:
    try:
        logger.info("Running the engine test...")
        build_dir = get_build_dir(release)
        exe_path = os.path.normpath(
            os.path.join(
                build_dir, get_build_type(release), "engine-test" + SCRIPT_EXTENSION
            )
        )

        subprocess.run(f"{exe_path}", check=True, shell=True)
    except Exception as e:
        logger.error(f"Error while running the engine test: {e}")
        exit(1)


def run_test_app() -> None:
    try:
        logger.info("Running the test app...")
        pytest_exe_path = get_pytest_exe_path(APP_DIR)
        subprocess.run(
            f"{pytest_exe_path}",
            cwd=APP_DIR,
            check=True,
            shell=True,
        )
    except Exception as e:
        logger.error(f"Error while running the test app: {e}")
        exit(1)


def run_config() -> None:
    # ================== APPLICATION RELATED SETTINGS ================
    # check the existence of application folder
    if not os.path.exists(APP_DIR):
        logger.error(
            f'The "{os.path.relpath(APP_DIR, PROJECT_DIR)}" directory does not exist.'
        )
        exit(1)

    # ================== SYSTEM HEALTH CHECK =========================
    logger.info("Checking the system health...")
    system_health_check()
    logger.info("The system health check is done.")
    # ================================================================

    # ================== CREATE TEMP ENVIRONMENT =====================
    logger.info("Creating the temp environment...")
    create_folder_if_not_exists(TEMP_DIR, PROJECT_DIR)
    logger.info("The temp environment has been created.")
    # ================================================================

    # ================== CREATE VIRTUAL ENVIRONMENT ==================
    logger.info("Creating the virtual environments...")
    create_virtual_environment(APP_DIR)
    create_virtual_environment(AUTOGEN_DIR)
    logger.info("The virtual environments have been created.")
    # ================================================================

    # ================== UPDATE REQUIREMENTS ========================
    logger.info("Updating the requirements...")
    update_requirements(APP_DIR)
    update_requirements(AUTOGEN_DIR)
    logger.info("The requirements have been updated.")
    # ================================================================

    # ================== CLONE THE VENDOR LIBRARIES ==================
    logger.info("Cloning the vendor libraries...")
    clone_vendor_libraries()
    logger.info("The vendor libraries have been cloned.")
    # ================================================================

    # ================== CREATE PY ENGINE BINDING ==================
    logger.info("Creating the py engine binding...")
    create_folder_if_not_exists(ENGINE_BINDING_DIR, APP_DIR)
    logger.info("The py engine binding has been created.")
    # ================================================================


def install_dependencies(project: str, package: str) -> None:
    folder: str = APP_DIR if project == "app" else AUTOGEN_DIR

    try:
        logger.info(f"Installing the {package} package...")
        subprocess.run(
            f"{get_python_exe_path(folder)} -m pip install {package}".split(" "),
            cwd=folder,
            check=True,
            shell=True,
        )
        logger.info(f"The {package} package has been installed successfully.")
        update_requirements(folder)
        logger.info(f"The requirements file has been updated successfully.")
    except Exception as e:
        logger.error(f"Error while installing the {package} package: {e}")
        exit(1)


def main():
    # ================== CONFIG RELATED SETTINGS =====================
    has_run_config = False

    # always run the config if the temp directory does not exist
    if not os.path.exists(TEMP_DIR):
        has_run_config = True
        run_config()
    # ================================================================

    # ================== ARGUMENTS RELATED SETTINGS ==================
    parser = argparse.ArgumentParser(
        description="The configuration helper for the current project"
    )
    parser.add_argument(
        "-r",
        "--release",
        action="store_true",
        help="Generate the build system for the release mode",
    )

    subparsers = parser.add_subparsers(dest="action", help="The action to perform")

    subparsers.add_parser("config", help="Run the configuration")
    subparsers.add_parser("designer", help="Open the designer")
    subparsers.add_parser("run", help="Run the application")

    deploy_parser = subparsers.add_parser("package", help="Install the dependencies")
    deploy_parser.add_argument(
        "project",
        choices=["autogen", "app"],
    )
    deploy_parser.add_argument(
        "package",
        help="The package to be installed",
    )

    convert_parser = subparsers.add_parser("convert", help="Convert the ui files")
    convert_parser.add_argument("type", choices=["ui", "cpp", "all"])

    engine_parser = subparsers.add_parser("engine", help="Engine related actions")
    engine_parser.add_argument(
        "engine_action", choices=["generate", "build", "install"]
    )

    test_parser = subparsers.add_parser("test", help="Test related actions")
    test_parser.add_argument(
        "test_action",
        choices=["all", "autogen", "engine", "app"],
        default="all",
    )

    autogen_parser = subparsers.add_parser("autogen", help="Autogen related actions")
    autogen_parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force the autogen to run even if no header is modified",
    )

    args = parser.parse_args()

    if args.action == "config":
        if not has_run_config:
            run_config()
    elif args.action == "designer":
        open_designer()
    elif args.action == "convert":
        if args.type == "ui":
            convert_ui_files()
        elif args.type == "cpp":
            run_autogen()
        elif args.type == "all":
            convert_ui_files()
            run_autogen()
    elif args.action == "package":
        install_dependencies(args.project, args.package)
    elif args.action == "run":
        convert_ui_files()
        run_autogen()
        generator_if_not_exists(release=args.release)
        build_engine(release=args.release)
        run_application()
    elif args.action == "test":
        build_engine(release=args.release)

        if args.test_action == "autogen":
            run_autogen_test()
        elif args.test_action == "engine":
            run_engine_test(release=args.release)
        elif args.test_action == "app":
            run_test_app()
        elif args.test_action == "all":
            run_engine_test(release=args.release)
            run_autogen_test()
            run_test_app()
    elif args.action == "engine":
        if args.engine_action == "generate":
            generate_build_system(release=args.release)
        elif args.engine_action == "build":
            generator_if_not_exists(release=args.release)
            run_autogen()
            build_engine(release=args.release)
        elif args.engine_action == "install":
            generator_if_not_exists(release=True)
            run_autogen()
            build_engine(release=True)
            install_engine(release=True)
    elif args.action == "autogen":
        run_autogen(force=args.force)
    # ================================================================


if __name__ == "__main__":
    main()
