
import argparse
from pathlib import Path

def create_parser() -> argparse.ArgumentParser:
    """
    Creates a parser, sub-parser for the command 'organize,
        and adds arguments.
    return: The created and updated parser.
    """

    parser = argparse.ArgumentParser(
        prog="PictureManager",
        description="Picture Manager CLI")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # organize command
    organize_parser = subparsers.add_parser('organize',
                                            help='Organize pictures')
    organize_parser.add_argument('-d', '--directory', required=True, type=Path,
                                 help='directory with pictures to be processed')
    organize_parser.add_argument('-i', '--in-place', required=False,
                                 action='store_true', default=False,
                                 help='Process pictures in place, or use output-directory')
    organize_parser.add_argument('-o', '--output-directory', required=False,
                                 type=Path, help='directory to put processed pictures')
    organize_parser.add_argument('-r', '--recursive', required=False,
                                 action='store_true', default=False,
                                 help='recursively go through directory,' \
                                 ' does not follow symlinks')
    organize_parser.add_argument('--organize-by-year', required=False,
                                 action='store_true', default=False,
                                 help='organizes pictures into directories for every year')
    organize_parser.add_argument('--organize-by-month', required=False,
                                 action='store_true', default=False,
                                 help='organizes pictures into directories for every month')
    organize_parser.add_argument('--organize-by-day', required=False,
                                 action='store_true', default=False,
                                 help='organizes pictures into directories for every day')
    organize_parser.add_argument('--delete-duplicates', required=False,
                                 action='store_true', default=False,
                                 help='delete duplicate pictures (DESTRUCTIVE)')
    return parser


def parse_args(parser: argparse.ArgumentParser) -> argparse.Namespace:
    """
    Parses the arguments for the parser, validates them, and returns the args
    
    :param parser: The created parser with the arguments
    :return: The arguments as a argparse.Namespace
    :rtype: Namespace
    """

    args = parser.parse_args()
    validate_args(parser, args)
    return args


def validate_args(parser: argparse.ArgumentParser, args: argparse.Namespace):
    """
    Validates the arguments passed in, and returns parser.error if invalid.
    
    :param parser: The created ArgumentParser
    :type parser: argparse.ArgumentParser
    :param args: The args for the created parser.
    :type args: argparse.Namespace
    """

    if not args.in_place and not args.output_directory:
        parser.error("--in-place or --output-directory must be included")
    if args.in_place and args.output_directory:
        parser.error("--output-directory can't be used if --in-place is used")
    if args.organize_by_month and not args.organize_by_year:
        parser.error("Can't --organize-by-month if not including"
                     "--organize-by-year")
    if args.organize_by_day and not args.organize_by_year:
        parser.error("Can't --organize-by-day if not including"
                     "--organize-by-year")
    if args.organize_by_day and not args.organize_by_month:
        parser.error("Can't --organize-by-day if not including"
                     "--organize-by-month")
