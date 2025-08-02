import logging
from utils.args import Args
from utils.template import AutoGenTemplate
from parser.paser import Parser


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)s] - %(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    args = Args()

    logging.info("Starting the autogen process ...")

    logging.info("Parsing the input files ...")
    Parser.ConfigClang(args.clang)
    logging.info(f"H files: {args.input_file}")
    logging.debug(f"Parsing the input file: {args.input_file} ...")
    parser = Parser(args.input_file)
    logging.debug(f"Parsed the input file: {args.input_file} ...")

    logging.info("Generating the output file ...")

    template = AutoGenTemplate(args.jinja_template)

    result = parser.parse(template)

    with open(args.output_file, "w") as f:
        f.write(result)


if __name__ == "__main__":
    main()
