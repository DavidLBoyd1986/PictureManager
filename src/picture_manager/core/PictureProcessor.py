import hashlib
from pathlib import Path
from datetime import datetime
import argparse
import shutil
from PIL import Image
from PIL import ImageFile

# TODO Find way to iterate through files only once. This could be done while processing files through iteration
#  instead of making lists to be processed later.
# TODO Create separate method for processing files in place without copying them
# TODO - Have a separate method process each individual picture.
#  Might be necessary later when more functionality is added


class PictureProcessor:
    """
    Object that contains methods to process pictures for the application.
    """
    def __init__(self, args: argparse.Namespace):
        self.args = args 
        self._processedImageTracker = {}

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        subdir = "organized_pictures_" + timestamp
        self._source_directory_path = Path(args.directory)
        self._output_directory_path = Path(args.output_directory) / subdir
        self._output_directory_path.mkdir()
        self._picture_list = self._compile_picture_list()

        # TODO: Process video files as well
        # Get list of all video files
        self.videoList = list(self._source_directory_path.glob('*.MP4'))
        self.videoList.extend(self._source_directory_path.glob('*.MOV'))

        self._process_pictures(args)

    def _compile_picture_list(self) -> list[Path]:
        """
        Compiles the picture list that will be processed
        :return: Compiled list of pictures to process
        """
        self._picture_list =\
            list(self._source_directory_path.glob('**/*.jpg'))
        self._picture_list.extend(
            list(self._source_directory_path.glob('**/*.png'))
        )
        self._picture_list.extend(
            list(self._source_directory_path.glob('**/*.gif'))
        )
        self._picture_list.extend(
            list(self._source_directory_path.glob('**/*.HEIC'))
        )
        return self._picture_list

    def _process_pictures(self, args: argparse.Namespace) -> None:
        """
        Processes all the pictures in the compiledpicturelist
        :param args - arguments passed in from argparse parser
        :return: None
        """
        for picture in self._picture_list:
            # Hash pic, and check if it is a duplicate
            if args.delete_duplicates:
                picture_hash = self._hash_picture(picture.__str__())
                if picture_hash not in self._processedImageTracker:
                    self._processedImageTracker[picture_hash] = True
                else:
                    continue

            # Get the picture filename from the whole directory path
            picture_name = picture.__str__().split('\\')[-1]

            # Open the picture with PIL to extract metadata
            picture_in_pil = Image.open(picture)

            if not args.organize_by_year and not args.organize_by_month and not args.organize_by_day:
                copy_location = self._output_directory_path / picture_name
            elif not args.organize_by_year and not args.organize_by_month:
                copy_location = self._output_directory_path / picture_name
            elif not args.organize_by_year:
                copy_location = self._output_directory_path / picture_name
            else:
                # Get location to copy file to based on time, creates directories if necessary
                copy_location = self._organize_pictures_by_time(picture_in_pil, picture_name, args)

            #TODO - Delete Debug statement below
            if copy_location.__str__().__contains__('no_timestamp'):
                print(picture_name)

            # Copy the file to the new directory
            shutil.copyfile(picture, copy_location)

    def _hash_picture(self, picture_file: Path, algorithm='sha256') -> str:
        """
        Calculate the hash digest of the picture file

        :param picture_file: full filepath to the picture_file
        :param algorithm: default set, can be changed if desired
        :return: hash of the picture_file"""
        hasher = hashlib.new(algorithm)
        with open(picture_file, 'rb') as f:  # 'rb' reads it in as binary
            while chunk := f.read(4096):  # ':=' walrus operator - assigns variables inside expressions
                hasher.update(chunk)
        return hasher.hexdigest()

    def _organize_pictures_by_time(self, picture_in_pil: ImageFile, picture_name: str, args: argparse.Namespace):
        """
        This method takes the ImageFile and the pic_name.
        Extracts the time from the ImageFile, and creates the directories based on time the picture was taken.
        Returns the directory location to copy the picture to.

        :param picture_in_pil - ImageFile returned by pillow
        :param picture_name - filename of picture
        :return: Directory to copy picture to
        """

        exif_data = picture_in_pil.getexif()
        print(exif_data) #TODO - Delete this debug

        if exif_data is not None: #  If exif_data is None, no metadata exists
            picture_taken_date = exif_data.get(306)
            if picture_taken_date is None: # If None, no timestamp exists
                print(picture_taken_date) #TODO - Delete this debug
                if not Path(self._output_directory_path.__str__() + '\\' + "no_timestamp").exists():
                    (self._output_directory_path / "no_timestamp").mkdir()
                return self._output_directory_path / "no_timestamp" / picture_name
        else:
            if not Path(self._output_directory_path.__str__() + '\\' + "no_metadata").exists():
                (self._output_directory_path / "no_metadata").mkdir()
            return self._output_directory_path / "no_metadata" / picture_name

        year_taken = picture_taken_date.split(':')[0]
        month_taken = picture_taken_date.split(':')[1]
        day_taken = picture_taken_date.split(':')[2].split(' ')[0]

        # If directory for time doesn't exist, create it
        if args.organize_by_year:
            if not Path(self._output_directory_path.__str__() + '\\' +
                        str(year_taken)).exists():
                (self._output_directory_path / str(year_taken)).mkdir()
            copy_location = (self._output_directory_path / str(year_taken) /
                             picture_name)
        if args.organize_by_month:
            if not Path(self._output_directory_path.__str__() + '\\' +
                        str(year_taken) + '\\' + str(month_taken)).exists():
                (self._output_directory_path / str(year_taken) /
                    str(month_taken)).mkdir()
            copy_location = (self._output_directory_path / str(year_taken) /
                str(month_taken) / picture_name)
        if args.organize_by_day:
            if not Path(self._output_directory_path.__str__() + '\\' +
                        str(year_taken) + '\\' + str(month_taken) + 
                        '\\' + str(day_taken)).exists():
                (self._output_directory_path / str(year_taken) /
                    str(month_taken) / str(day_taken)).mkdir()
            copy_location = (self._output_directory_path / str(year_taken) /
                             str(month_taken) / str(day_taken) / picture_name)
        try:
            copy_location
        except NameError:
            raise RuntimeError("The copy_location variable was never" \
                "created in _organize_pictures_by_time method")
        return copy_location
