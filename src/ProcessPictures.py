from pathlib import Path
from PIL import Image
import shutil


class PictureProcessor:
    """
    Object that contains methods to process pictures for the application.
    """
    def __init__(self, session_manager):
        self.session_manager = session_manager
        self.processedImageTracker = {}
        self.imageInformation = {"image_filename": "",
                                 "image_full_directory_path": "",
                                 "destination_directory": "",
                                 "creation_date": "",
                                 "creation_year": "",
                                 "creation_month": "",
                                 "creation_day": "",
                                 "duplicate": "",
                                 "orientation": ""}

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
        image = Image.open(image_path)
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

    def process_picture(self, image_path):
        """Processes a picture given to it while navigating the indicated directory

        :param image_path: full Path object to the image
        :return: Boolean indicating if the picture was processed successfully
        """
        # Resets image information
        for key in self.imageInformation.keys():
            self.imageInformation[key] = ""

        # Gets new image information
        self.image_information["image_filename"] = self.get_filename_from_directory_path(image_path)
        self.imageInformation["image_full_directory_path"] = image_path
        self.imageInformation["destination_directory"] = self.session_manager['new_directory_object']
        self.imageInformation["duplicate"] =\
            self.is_image_duplicate_by_filename(self, self.imageInformation["image_filename"])

