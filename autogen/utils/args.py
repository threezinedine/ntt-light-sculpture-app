import os
import argparse
from typing import List


class Args:
    """
    This class is used for parsing the input arguments for the autogen project

    Example:

    `Command line`:
    ```bash
    $ python main.py input.h template.jinja
    ```

    `Python code`:
    ```python
    from args import Args

    args = Args() # error will be raised if the input file or jinja template file does not exist
    print(args.input_file) # input.h
    print(args.jinja_template) # template.jinja
    ```
    """

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Auto generate the python interface code from the .h source code",
        )

        parser.add_argument(
            "-i",
            "--input_files",
            nargs="+",
            required=True,
            help="The .h file to be analyzed, multiple files are supported",
        )

        parser.add_argument(
            "-j",
            "--jinja_template",
            required=True,
            help="The jinja template file to be used for generating the python interface code",
        )

        parser.add_argument(
            "-o",
            "--output_file",
            required=True,
            help="The output file name for the generated python interface code",
        )

        parser.add_argument(
            "-c",
            "--clang",
            help="The absolute path to the libclang.dll file",
            required=True,
        )

        self._args = parser.parse_args()

        # ================== VALIDATION ==============================
        if not isinstance(self.input_files, list):
            self.input_files = [self.input_files]

        for input_file in self.input_files:
            self._validate_input_file(input_file)

        if not os.path.exists(self.jinja_template):
            raise FileNotFoundError(
                f"The jinja template file {self.jinja_template} does not exist"
            )
        if not self.jinja_template.endswith(".jinja"):
            raise ValueError(
                f"The jinja template file {self.jinja_template} is not a valid jinja template file"
            )

        if not os.path.exists(self.clang):
            raise FileNotFoundError(f"The clang file {self.clang} does not exist")

        # ============================================================

    def _validate_input_file(self, input_file: str) -> None:
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"The input file {input_file} does not exist")

        if not input_file.endswith(".h"):
            raise ValueError(f"The input file {input_file} is not a valid .h file")

    @property
    def input_files(self) -> List[str]:
        """
        The .h file which will be analyzed by the autogen, this should be a valid .h file
        The macro is also supported, e.g. `#include "input.h"`
        """
        return self._args.input_files

    @property
    def jinja_template(self) -> str:
        """
        The jinja template file which will be used for generating the python interface code
        The jinja template file should be a valid jinja template file
        """
        return self._args.jinja_template

    @property
    def output_file(self) -> str:
        """
        The output file name for the generated python interface code, if not provided
        the output file name will be the same as the input file name with the suffix .py
        """
        return self._args.output_file

    @property
    def clang(self) -> str:
        """
        The absolute path to the libclang.dll file
        """
        return self._args.clang
