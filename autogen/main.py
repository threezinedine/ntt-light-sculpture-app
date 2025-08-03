import sys
import logging
from utils.args import Args
from utils.template import AutoGenTemplate
from utils.types import TypeConverter
from parser.paser import Parser
from data import LOGGER_NAME


def main():
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[%(levelname)-5s] - [%(name)-7s] - %(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    args = Args()

    logger.info("Starting the autogen process ...")

    logger.info("Parsing the input files ...")
    Parser.ConfigClang(args.clang)
    logger.info(f"H files: {args.input_file}")
    logger.debug(f"Parsing the input file: {args.input_file} ...")
    parser = Parser(args.input_file)
    logger.debug(f"Parsed the input file: {args.input_file} ...")

    logger.info("Generating the output file ...")

    template = AutoGenTemplate(args.jinja_template, TypeConverter())

    result = parser.parse(template)

    with open(args.output_file, "w") as f:
        f.write(result)


if __name__ == "__main__":
    main()
