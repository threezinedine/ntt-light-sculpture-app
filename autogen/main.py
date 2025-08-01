from utils.args import Args
from utils.template import AutoGenTemplate
from parser.paser import Parser


def main():
    args = Args()

    Parser.ConfigClang(args.clang)
    parser = Parser(args.input_files[0])

    template = AutoGenTemplate(args.jinja_template)

    result = template.render({})

    with open(args.output_file, "w") as f:
        f.write(result)


if __name__ == "__main__":
    main()
