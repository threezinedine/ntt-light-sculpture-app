from utils.args import Args
from utils.template import AutoGenTemplate


def main():
    args = Args()

    print(args.input_files)
    print(args.jinja_template)
    print(args.output_file)

    template = AutoGenTemplate(args.jinja_template)

    result = template.render({})

    with open(args.output_file, "w") as f:
        f.write(result)


if __name__ == "__main__":
    main()
