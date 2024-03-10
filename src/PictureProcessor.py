from pathlib import Path
import shutil
import PIL.Image

# TODO Find way to iterate through files only once. This could be done while processing files through iteration
#  instead of making lists to be processed later.
# TODO Hash the file based on it's contents to detect duplicate photos with different names
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
                # Copy the file to the new directory
                shutil.copyfile(pic, copy_location)
            else:
                continue

    def _organize_pic_by_time(self, pic_in_pil, pic_name):
        """
        This method takes the pic open in PIL and the pic_name.
        Extracts the time from the pic, and creates the directories based on time the pic was taken.
        Returns the directory location to copy the pic to.

        :param pic_in_pil: pic open in PIL
        :param pic_name: filename of pic
        :return: location to copy picture to
        """
        pic_taken_date = pic_in_pil.getexif()[306]
        year_taken = pic_taken_date.split(':')[0]
        month_taken = pic_taken_date.split(':')[1]

        if not Path(self._copyPicDirectoryPath.__str__() + '\\' + str(year_taken)).exists():
            (self._copyPicDirectoryPath / str(year_taken)).mkdir()
        if not Path(self._copyPicDirectoryPath.__str__() + '\\' + str(year_taken) + '\\' +
                    str(month_taken)).exists():
            (self._copyPicDirectoryPath / str(year_taken) / str(month_taken)).mkdir()
        copy_location = self._copyPicDirectoryPath / str(year_taken) / str(month_taken) / pic_name

        return copy_location
