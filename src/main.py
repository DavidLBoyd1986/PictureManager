from cli.parser import create_parser
from cli.commands import handle_organize

def main():

    parser = create_parser()
    args = parser.parse_args()

    if args.command == 'organize':
        handle_organize(args)

if __name__ == '__main__':
    main()
