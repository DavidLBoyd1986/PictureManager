from picture_manager.cli.parser import create_parser
from picture_manager.cli.parser import parse_args
from picture_manager.cli.commands import handle_organize

def main():
    parser = create_parser()
    args = parse_args(parser)

    if args.command == 'organize':
        handle_organize(args)

if __name__ == '__main__':
    main()