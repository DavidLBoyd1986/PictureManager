
import argparse
from pathlib import Path

def create_parser():
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
    organize_parser.add_argument('--delete_duplicates', required=False,
                                 action='store_true', default=False,
                                 help='delete duplicate pictures (DESTRUCTIVE)')

    return parser
    