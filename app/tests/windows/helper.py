import os
import json
from dataclasses import asdict
from typing import Generator, Any
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from constants import APP_DATA_KEY, TEST_APP_DATA_FOLDER
from utils.application import GetApplicationDataFile, GetApplicationDataFolder


class AppDataSetup:
    def SetupApplicationData(self, application: Any) -> None:
        with open(GetApplicationDataFile(), "w") as f:
            f.write(json.dumps(asdict(application)))


@pytest.fixture()
def appDataSetup(fs: FakeFilesystem) -> Generator[AppDataSetup, None, None]:
    os.environ[APP_DATA_KEY] = TEST_APP_DATA_FOLDER
    fs.create_dir(GetApplicationDataFolder())  # type: ignore

    yield AppDataSetup()
