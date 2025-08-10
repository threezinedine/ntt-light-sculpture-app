import os

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
TEST_PROJECT_FILE_ERROR_FOLDER = "C:/Users/jason/Errors"
TEST_PROJECT_FILE_ERROR_PROJECT_NAME = "Error Project"
# ==================================================================================

# ================================ EVENTS ==========================================
APPLICATION_LOADED_EVENT_NAME = "application_loaded"
OPEN_NON_EXISTED_PROJECT_DIR_EVENT_NAME = "open_non_existed_project_dir"
APPLICATION_UPDATED_EVENT_NAME = "application_updated"
CHANGE_PROJECT_EVENT_NAME = "change_project"
RECENT_PROJECTS_EVENT_NAME = "recent_projects"
# ==================================================================================
