import os

# ================================ CONSTANTS =======================================
MAX_NUMBER_OF_RECENT_PROJECTS = 5
CURRENT_PROJECT_FOLDER = os.path.dirname(__file__)
ASSETS_FOLDER = os.path.join(CURRENT_PROJECT_FOLDER, "assets")
TEST_IMAGE_FOLDER = os.path.join(ASSETS_FOLDER, "images", "tests")

VIEW_TAB_NAME = "OpenGL View"
IMAGE_CONTEXT_OPEN_OPTION = "Open"
IMAGE_CONTEXT_DELETE_OPTION = "Delete"
# ==================================================================================

# ================================ PARAMETERS ======================================
DEFAULT_THRESHOLD = 128
# ==================================================================================

# ================================ ENVIRONMENT VARIABLES ===========================
APP_DATA_KEY = "APPDATA"
# ==================================================================================

# ================================ APPLICATION DATA ================================
APPLICATION_DATA_FOLDER = "LightSculpture"
APPLICATION_DATA_FILE = "application.json"
# ==================================================================================

# ================================ PROJECT DATA ================================
PROJECT_DATA_FILE = "project.json"
# ==================================================================================

# ================================ TEST CONSTANTS ==================================
TEST_USER_FOLDER = "C:/Users/jason"
TEST_APP_DATA_FOLDER = os.path.join(TEST_USER_FOLDER, "appdata")
TEST_NON_EXISTED_PROJECT_FOLDER = os.path.join(
    TEST_USER_FOLDER, "projects", "non_existed_project"
)
TEST_NEW_PROJECT_PATH = "C:/Users/jason/Projects"
TEST_NEW_PROJECT_NAME = "Test Project"
TEST_NEW_PROJECT_NAME_2 = "Testing"
TEST_NEW_PROJECT_NAME_3 = "Testing 2"
TEST_NEW_PROJECT_NAME_4 = "Testing 3"
TEST_NEW_PROJECT_NAME_5 = "Testing 4"
TEST_NEW_PROJECT_NAME_6 = "Testing 5"
TEST_NEW_PROJECT_NAME_7 = "Testing 6"
TEST_NEW_PROJECT_NAME_8 = "Testing 7"
TEST_NEW_PROJECT_NAME_9 = "Testing 8"
TEST_NEW_PROJECT_NAME_10 = "Testing 9"
TEST_PROJECT_FILE_ERROR_FOLDER = "C:/Users/jason/Errors"
TEST_PROJECT_FILE_ERROR_PROJECT_NAME = "Error Project"

TEST_PNG_IMAGE_PATH = os.path.join(TEST_IMAGE_FOLDER, "test-png.png")
TEST_PNG_IMAGE_PATH_2 = os.path.join(TEST_IMAGE_FOLDER, "test-png-2.png")
# ==================================================================================

# ================================ EVENTS ==========================================
APPLICATION_LOADED_EVENT_NAME = "application_loaded"
OPEN_NON_EXISTED_PROJECT_DIR_EVENT_NAME = "open_non_existed_project_dir"
APPLICATION_UPDATED_EVENT_NAME = "application_updated"
CHANGE_PROJECT_EVENT_NAME = "change_project"
RECENT_PROJECTS_EVENT_NAME = "recent_projects"
MODIFY_IMAGES_LIST_EVENT_NAME = "load_image"

OPEN_IMAGE_TAB_EVENT_NAME = "open_image_tab"
# ==================================================================================
