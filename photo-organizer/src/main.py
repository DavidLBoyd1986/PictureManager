import argparse
from options import OrganizerOptions
from organizer import PhotoOrganizer
from logger import setup_logger

def parse_args():
    parser = argparse.ArgumentParser(description="Photo Organizer")
    parser.add_argument("directory", help="Directory to organize")
    parser.add_argument("--levels", type=int, choices=[1,2,3], default=3, help="Levels for time-based folders (1=year, 2=year/month, 3=year/month/day)")
    parser.add_argument("--delete-duplicates", action="store_true", help="Delete duplicate photos")
    parser.add_argument("--delete-blurry", action="store_true", help="Delete blurry photos")
    parser.add_argument("--recursive", action="store_true", help="Recursively scan subfolders")
    parser.add_argument("--log", default="organizer.log", help="Log file path")
    return parser.parse_args()

def main():
    args = parse_args()
    logger = setup_logger(args.log)
    options = OrganizerOptions(
        directory=args.directory,
        levels=args.levels,
        delete_duplicates=args.delete_duplicates,
        delete_blurry=args.delete_blurry,
        recursive=args.recursive,
        logger=logger
    )
    organizer = PhotoOrganizer(options)
    organizer.organize()

if __name__ == "__main__":
    main()