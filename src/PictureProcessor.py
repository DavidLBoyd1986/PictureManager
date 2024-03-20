import hashlib
from pathlib import Path
import shutil
import PIL.Image

# TODO Find way to iterate through files only once. This could be done while processing files through iteration
#  instead of making lists to be processed later.
# TODO Create separate method for processing files in place without copying them
# TODO - Have a separate method process each individual picture.
#  Might be necessary later when more functionality is added


class PictureProcessor:
    """
    Object that contains methods to process pictures for the application.
    """
    def __init__(self, session_options):
        self.session_options = session_options
        
        self._processedImageTracker = {}
        self._hashedImageTracker = {}

        # Do I have to turn it into a Path since it's already a WindowsPath
        self._rootDirectoryPath = Path(session_options['root_directory_object'])
        self._copyPicDirectoryPath = Path(session_options['new_directory_object'])
        self._picList = self._compile_pic_list()

        # TODO: Process video files as well
        # Get list of all video files
        self.videoList = list(self._rootDirectoryPath.glob('*.MP4'))
        self.videoList.extend(self._rootDirectoryPath.glob('*.MOV'))

        self._process_pictures()

    def _compile_pic_list(self):
        """
        Compiles a pic list that will be processed.
        Need to find a way to not precompile list, but to process images on the fly.
        :param self: self
        :return: compiled picture list
        """

        # Get list of all image files
        self._picList = list(self._rootDirectoryPath.glob('**/*.jpg'))
        self._picList.extend(list(self._rootDirectoryPath.glob('**/*.png')))
        self._picList.extend(list(self._rootDirectoryPath.glob('**/*.gif')))
        self._picList.extend(list(self._rootDirectoryPath.glob('**/*.HEIC')))

        return self._picList

    def _process_pictures(self):
        """Processes all the pictures in indicated directory
        """
        for pic in self._picList:
            # Hash pic, and check if it is a duplicate
            pic_hash = self._hash_pic(pic.__str__())
            if pic_hash not in self._hashedImageTracker:
                self._hashedImageTracker[pic_hash] = True
            else:
                continue

            # This grabs the pic filename from the whole directory path
            pic_name = pic.__str__().split('\\')[-1]

            # verify pic hasn't been processed - isn't a duplicate - then copy it
            if pic_name not in self._processedImageTracker:
                # Add file to hashtable for quick check if another file is a duplicate
                self._processedImageTracker[pic_name] = True
                # Open the pic with PIL to extract metadata
                pic_in_pil = PIL.Image.open(pic)
                # Get location to copy file to based on time, creates directories if necessary
                copy_location = self._organize_pic_by_time(pic_in_pil, pic_name)
                if copy_location.__str__().__contains__('no_date'):
                    print(pic_name)
                # Copy the file to the new directory
                shutil.copyfile(pic, copy_location)
            else:
                continue

    def _hash_pic(self, pic_file, algorithm='sha256'):
        """
        Calculate the hash digest of the pic file

        :param pic_file: full filepath to the pic_file
        :param algorithm: default set, can be changed if desired
        :return: hash of the pic_file"""
        hasher = hashlib.new(algorithm)
        with open(pic_file, 'rb') as f:  # 'rb' reads it in as binary
            while chunk := f.read(4096):  # ':=' walrus operator - assigns variables inside expressions
                hasher.update(chunk)
        return hasher.hexdigest()

    def _organize_pic_by_time(self, pic_in_pil, pic_name):
        """
        This method takes the pic open in PIL and the pic_name.
        Extracts the time from the pic, and creates the directories based on time the pic was taken.
        Returns the directory location to copy the pic to.

        :param pic_in_pil: pic open in PIL
        :param pic_name: filename of pic
        :return: location to copy picture to
        """
        # Test is exif data exists, then if the timestamp [306] exists, if either don't exist store image in '_no_date'
        exif_data = pic_in_pil.getexif()
        if exif_data is not None:
            pic_taken_date = exif_data.get(306)
            if pic_taken_date is not None:
                year_taken = pic_taken_date.split(':')[0]
                month_taken = pic_taken_date.split(':')[1]

                if not Path(self._copyPicDirectoryPath.__str__() + '\\' + str(year_taken)).exists():
                    (self._copyPicDirectoryPath / str(year_taken)).mkdir()
                if not Path(self._copyPicDirectoryPath.__str__() + '\\' + str(year_taken) + '\\' +
                            str(month_taken)).exists():
                    (self._copyPicDirectoryPath / str(year_taken) / str(month_taken)).mkdir()
                copy_location = self._copyPicDirectoryPath / str(year_taken) / str(month_taken) / pic_name

                return copy_location

        print(exif_data)
        if not Path(self._copyPicDirectoryPath.__str__() + '\\' + "no_date").exists():
            (self._copyPicDirectoryPath / "no_date").mkdir()
        return self._copyPicDirectoryPath / "no_date" / pic_name
