from pathlib import Path
import shutil
import PIL.Image


class PictureProcessor:
    """
    Object that contains methods to process pictures for the application.
    """
    def __init__(self, session_options):
        # Changed to just passing session_options, can probably delete this.
        #self.session_manager = session_manager
        self.session_options = session_options

        # Do I need this here??
        self.imageInformation = {"image_filename": "",
                                 "image_full_directory_path": "",
                                 "destination_directory": "",
                                 "creation_date": "",
                                 "creation_year": "",
                                 "creation_month": "",
                                 "creation_day": "",
                                 "duplicate": "",
                                 "orientation": ""}

        self.processedImageTracker = {}
        # Do I have to turn it into a Path since it's already a WindowsPath
        self.rootDirectoryPath = Path(session_options['root_directory_object'])
        self.copyPicDirectoryPath = Path(session_options['new_directory_object'])

        # TODO Find a way to iterate through files only once. This could be done while processing files through iteration
        #  instead of making lists to be processed later.
        # Get list of all image files
        self.picList = list(self.rootDirectoryPath.glob('**/*.jpg'))
        self.picList.extend(list(self.rootDirectoryPath.glob('**/*.png')))
        self.picList.extend(list(self.rootDirectoryPath.glob('**/*.gif')))
        self.picList.extend(list(self.rootDirectoryPath.glob('**/*.HEIC')))

        # Get list of all video files
        self.videoList = list(self.rootDirectoryPath.glob('*.MP4'))
        self.videoList.extend(self.rootDirectoryPath.glob('*.MOV'))

        self.process_pictures()

    @staticmethod
    def get_filename_from_directory_path(image_path):
        """Gets full filename from directory path

        :param image_path: A Path object of the full directory path of the image_file
        :return: str object of filename
        """

        if (not issubclass(type(image_path), Path)) and (not isinstance(image_path, Path)):
            raise TypeError("The image_path submitted was not of type Path or a subclass of it.")

        return image_path.__str__().split('\\')[-1]

    def is_image_duplicate_by_filename(self, image_filename):
        """Checks if image is a duplicate, and if not it adds it to the Dictionary of images processed
        
        :param image_filename: String of just the filename of the image, should not include full directory path
        :return: Boolean that states if the file is a duplicate or not
        """
        if image_filename not in self.processedImageTracker:
            # Add file to hashtable for quick check if another file is a duplicate
            self.processedImageTracker[image_filename] = True
            return True

        # Image has been processed, return false
        return False

# TODO Hash the file based on it's contents to detect duplicate photos with different names
# TODO Create separate method for processing files in place without copying them
# TODO separate creating directories based on time into another method

    @staticmethod
    def get_image_creation_date(image_path):
        """Retrieves the creation time of the image, and returns the Year and Month
        
        :param image_path: Path object to the full directory path of the image file
        :return: String of image creation date
        """
        image = PIL.Image.open(image_path)
        # Get time data from EXIF data (metadata) using PIL library
        image_creation_date = image.getexif()[306]
        return image_creation_date

    def create_directories(self, image_path):
        """If necessary creates a directory for year and month of image creation date

        :param image_path:
        :return:
        """
        # TODO is there a way to test if directories need created in a simpler way?
        image_creation_date = self.get_image_creation_date(image_path)
        image_creation_year = image_creation_date.split(':')[0]
        image_creation_month = image_creation_date.split(':')[1]

        if not Path(self.destinationDirectory.__str__() + '\\' + str(image_creation_year)).exists():
            (self.destinationDirectory / str(image_creation_year)).mkdir()
        if not Path(self.destinationDirectory.__str__() + '\\' + str(image_creation_year) + '\\'
                    + str(image_creation_month)).exists():
            (self.destinationDirectory / str(image_creation_year) / str(image_creation_month)).mkdir()
        copy_location = self.destinationDirectory / str(image_creation_year) /\
                       str(image_creation_month) / self.get_filename_from_directory_path(image_path)
        self.copy_image(image_path, copy_location)

    @staticmethod
    def copy_image(image_path, copy_location):
        """Copies the file to the indicated destination

        :param image_path: Full directory Path object to the image
        :param copy_location: Full directory Path objec to the destination - includes filename
        :return: None
        """
        shutil.copyfile(image_path, copy_location)

    def process_pictures(self):
        """Processes a picture given to it while navigating the indicated directory

        :param image_path: full Path object to the image
        :return: Boolean indicating if the picture was processed successfully
        """
        for pic in self.picList:
            # This grabs just the filename from the whole directory path
            # TODO Hash the file based on it's contents to detect duplicate photos with different names
            pic_name = pic.__str__().split('\\')[-1]

            # verify pic hasn't been processed - isn't a duplicate - then copy it
            if pic_name not in self.processedImageTracker:
                # Add file to hashtable for quick check if another file is a duplicate
                self.processedImageTracker[pic_name] = True

                # TODO separate creating directories based on time into another method
                # Organize photos in folders by year and month
                # Get time data from EXIF data (metadata) using PIL library
                pic_open_in_pil = PIL.Image.open(pic)
                pic_taken_date = pic_open_in_pil.getexif()[306]
                year_taken = pic_taken_date.split(':')[0]
                month_taken = pic_taken_date.split(':')[1]

                if not Path(self.copyPicDirectoryPath.__str__() + '\\' + str(year_taken)).exists():
                    (self.copyPicDirectoryPath / str(year_taken)).mkdir()
                if not Path(self.copyPicDirectoryPath.__str__() + '\\' + str(year_taken) + '\\' + str(month_taken)).exists():
                    (self.copyPicDirectoryPath / str(year_taken) / str(month_taken)).mkdir()
                copy_location = self.copyPicDirectoryPath / str(year_taken) / str(month_taken) / pic_name

                # TODO Create separate method for processing files in place without copying them

                # Copy the file to the new directory
                shutil.copyfile(pic, copy_location)
            else:
                continue

        # Original Code
        # Resets image information
        # for key in self.imageInformation.keys():
        #     self.imageInformation[key] = ""
        #
        # # Gets new image information
        # self.image_information["image_filename"] = self.get_filename_from_directory_path(image_path)
        # self.imageInformation["image_full_directory_path"] = image_path
        # self.imageInformation["destination_directory"] = self.session_manager['new_directory_object']
        # self.imageInformation["duplicate"] =\
        #     self.is_image_duplicate_by_filename(self, self.imageInformation["image_filename"])

    # todo - Have a separate method process each individual picture.
    # def process_picture(self, image_path):
    #     """Processes a picture given to it while navigating the indicated directory
    #
    #     :param image_path: full Path object to the image
    #     :return: Boolean indicating if the picture was processed successfully
    #     """