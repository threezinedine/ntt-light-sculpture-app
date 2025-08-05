import os


def readContent(file: str, startLine: int, startColumn: int, length: int) -> str:
    if not os.path.exists(file):
        raise FileNotFoundError(f"File {file} not found")

    with open(file, "r") as f:
        lines = f.readlines()

        content = "\n".join(lines[startLine - 1 :])

        content = content[startColumn - 1 : startColumn + length - 1]

        return content
