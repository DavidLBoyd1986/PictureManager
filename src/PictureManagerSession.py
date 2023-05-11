import pathlib
import os
import re
from HelperFunctions import input_converter
from OSFunctions import createPictureDirectory


class PictureManagerSession:
    def __init__(self):

        # get OS type, determines valid directory paths
        os_type = os.name
        # Regex for validating directory inputs
        unix_directory_pattern = r"(?:\/[a-zA-Z0-9\.\-\_ ]+)+"
        self.unix_valid_directory = re.compile(unix_directory_pattern)
        windows_directory_pattern = r"[A-Z]:(?:\\[A-Za-z0-9-_ ']+)+"
        self.windows_valid_directory = re.compile(windows_directory_pattern)
        # Yes/No input validation
        self.input_validation_yes_no = ["Yes", "YES", "yes", 'Y', "y", "No", "NO", "no", "N", "n"]
        # Session Options and inputs stored in a dictionary
        self.session_options = {"root_directory_object": "", "recurse_directory": True, "modify_directory": False,
                                "new_directory_object": "", "delete_duplicates": False, "preserve_duplicates": True,
                                "delete_blurry": False, "preserve_blurry": True, "re-orientate_pics": True,
                                "time_organization": frozenset[True, False, False],
                                "group_by_facial_recognition": False, "os_type": os_type}
        # Every picture processed is put in this set. Used to detect duplicates
        self.picture_hashes = set()

        # Get user input for how to organize pictures
        self.initialization_questions()

        # Root directory given that will be analyzed for pictures
        print(self.session_options)

    def process_pictures(self):
        """this method will go through the directory provided, and process the pictures to be organized"""

    def initialization_questions(self):
        """This method gets the user's input for how PictureManager will organize their pictures

        returns: Dictionary with Questions (keys) mapped to Answers (Values)"""
        # Input the directory the pictures are located in
        self.input_root_directory()
        # Recursively go through sub-directories for pictures?
        self.input_recurse_directory()
        # Modify current directory?
        self.input_modify_directory()
        # If not modifying directory input new directory to move photos, and create it if it doesn't exist
        if not self.session_options["modify_directory"]:
            self.input_new_directory()
        # Delete Duplicates
        self.input_delete_duplicates()
        if self.session_options["delete_duplicates"] and self.session_options["modify_directory"]:
            # Preserve deleted duplicates in another directory for manual review?
            self.input_preserve_duplicates()
        # Delete Blurry
        self.input_delete_blurry()
        if self.session_options["delete_blurry"] and self.session_options["modify_directory"]:
            # Preserve deleted blurry photos in another directory for manual review?
            self.input_preserve_blurry()
        # Re-Orientate sideways pictures
        self.input_reorientate_pictures
        # Time Unit to organize pictures in at the highest level directory (Year/Month/Day)
        self.input_organize_by_time()

    def input_root_directory(self):
        """Method used by initialization_questions for input about the root_directory containing the pictures."""
        while True:
            try:
                root_directory_string = str(input("Input the directory the pictures are located in:\n"))

                # Test if input is a valid directory - THIS MIGHT NOT BE NEEDED SINCE ONLY VALID DIRECTORIES WILL EXIST
                if self.session_options["os_type"] == "nt":
                    if not re.match(self.windows_valid_directory, root_directory_string):
                        raise ValueError("not a valid directory")
                if self.session_options["os_type"] == "posix":
                    if not re.match(self.unix_valid_directory, root_directory_string):
                        raise ValueError("not a valid directory")

                # Test if inputted directory exists
                root_directory_object = pathlib.Path(root_directory_string)
                if not root_directory_object.exists():
                    raise ValueError("Directory doesn't exist")
            except ValueError:
                if self.session_options["os_type"] == "nt":
                    print("Directory input must be a valid string: i.e. C:\\Users\\david\\Pictures")
                elif self.session_options["os_type"] == "posix":
                    print("Directory input must be a valid string: i.e. /home/users/Pictures")
                else:
                    print("Directory invalid - OS not recognized")
            else:
                self.session_options["root_directory_object"] = root_directory_object
                break

    def input_recurse_directory(self):
        """Method used by initialization_questions for input about recursively delving the root_directory provided."""
        while True:
            try:
                recurse_directory = str(input("\nRecursively go through sub-directories for pictures?: Yes/No "
                                              "(Default: Yes)\n"))
                if recurse_directory == "":
                    break
                if recurse_directory not in self.input_validation_yes_no:
                    raise ValueError("Invalid Input")
            except ValueError:
                print("Must input Yes or No....")
            else:
                self.session_options["recurse_directory"] = input_converter(recurse_directory)
                break

    def input_modify_directory(self):
        """Method used by initialization_questions for input about modifying the root_directory provided."""
        while True:
            try:
                modify_directory = str(input("\nModify current directory?: Yes/No (Default: No)\n\n"
                                             "WARNING - Not modifying the current directory, and creating a new one to "
                                             "copy the pictures too, takes up a lot of space.\n"
                                             "Verify free space before doing this.\n"))
                if modify_directory == "":
                    break
                if modify_directory not in self.input_validation_yes_no:
                    raise ValueError("Invalid Input")
            except ValueError:
                print("Input must be: Yes or No....")
            else:
                self.session_options["modify_directory"] = input_converter(modify_directory)
                break

    def input_new_directory(self):
        """Method used by initialization_questions for input about where new directory location will be."""
        while True:
            try:
                new_directory_string = str(input("\nInput the directory to put the organized pictures in:\n"))

                # Test if input is a valid directory
                if self.session_options["os_type"] == "nt":
                    if not re.match(self.windows_valid_directory, new_directory_string):
                        raise ValueError("not a valid directory")
                if self.session_options["os_type"] == "posix":
                    if not re.match(self.unix_valid_directory, new_directory_string):
                        raise ValueError("not a valid directory")
                # Test if inputted directory exists, if not create it.
                new_directory_object = pathlib.Path(new_directory_string)
                if not new_directory_object.exists():
                    new_directory_object.mkdir(parents=True)
            except ValueError:
                if self.session_options["os_type"] == "nt":
                    print("Directory input must be a valid string: i.e. C:\\Users\\david\\Pictures")
                elif self.session_options["os_type"] == "posix":
                    print("Directory input must be a valid string: i.e. /home/users/Pictures")
                else:
                    print("Directory invalid - OS not recognized")
            else:
                self.session_options["new_directory_object"] = new_directory_object
                break

    def input_delete_duplicates(self):
        """Method used by initialization_questions for input about deleting duplicate pictures."""
        while True:
            try:
                delete_duplicates = str(input("\nDelete duplicate photos?: Yes/No (Default: No)\n"))
                if delete_duplicates == "":
                    break
                if delete_duplicates not in self.input_validation_yes_no:
                    raise ValueError("Invalid Input")
            except ValueError:
                print("Input must be: Yes or No....")
            else:
                self.session_options["delete_duplicates"] = input_converter(delete_duplicates)
                break

    def input_preserve_duplicates(self):
        """Method used by initialization_questions for input about preserving duplicate pictures marked for deletion."""
        while True:
            try:
                preserve_duplicates = str(input("\nPreserve duplicate photos marked for deletion?: Yes/No"
                                                "(Default: Yes)\n"))
                if preserve_duplicates == "":
                    break
                if preserve_duplicates not in self.input_validation_yes_no:
                    raise ValueError("Invalid Input")
            except ValueError:
                print("Input must be: Yes or No....")
            else:
                self.session_options["preserve_duplicates"] = input_converter(preserve_duplicates)
                if self.session_options["modify_directory"] and self.session_options["preserve_duplicates"]:
                        print("Duplicates will be stored here: FIX THIS")
                        #TODO Add where duplicates/blurry pics will be stored when modifying the directory
                        # Will be under /PictureManager/Sessions/Session_20211222/preserved_photos/duplicates
                break

    def input_delete_blurry(self):
        """Method used by initialization_questions for input about deleting blurry pictures."""
        while True:
            try:
                delete_blurry = str(input("\nDelete blurry photos?: Yes/No (Default: No)\n"))
                if delete_blurry == "":
                    break
                if delete_blurry not in self.input_validation_yes_no:
                    raise ValueError("Invalid Input")
            except ValueError:
                print("Input must be: Yes or No....")
            else:
                self.session_options["delete_blurry"] = input_converter(delete_blurry)
                break

    def input_preserve_blurry(self):
        """Method used by initialization_questions for input about preserving blurry pictures marked for deletion."""
        while True:
            try:
                preserve_blurry = str(input("\nPreserve blurry photos marked for deletion?: Yes/No (Default: Yes)\n"))
                if preserve_blurry == "":
                    break
                if preserve_blurry not in self.input_validation_yes_no:
                    raise ValueError("Invalid Input")
                if self.session_options["modify_directory"] and self.session_options["preserve_blurry"]:
                    print("Blurry photos will be stored here: FIX THIS")
                    #TODO Add where duplicates/blurry pics will be stored when modifying the directory
                    # Will be under /PictureManager/Sessions/Session_20211222/preserved_photos/duplicates
            except ValueError:
                print("Input must be: Yes or No....")
            else:
                self.session_options["preserve_blurry"] = input_converter(preserve_blurry)
                break

    def input_reorientate_pictures(self):
        """Method used by initialization_questions for input about re-orientating pictures saved in wrong direction."""
        while True:
            try:
                reorientate_pictures = str(input("\nReorientate pictures saved in wrong direction?: Yes/No"
                                                 "(Default: Yes)\n"))
                if reorientate_pictures == "":
                    break
                if reorientate_pictures not in self.input_validation_yes_no:
                    raise ValueError("Invalid Input")
            except ValueError:
                print("Input must be: Yes or No....")
            else:
                self.session_options["reorientate_pics"] = input_converter(reorientate_pictures)
                break

    def input_organize_by_time(self):
        """Method used by initialization_questions for input about organizing pictures by time."""
        while True:
            print ("\nPictures will be organized by time, default is to organize by year. Please select the main time "
                   "unit to organize by, and if you want sub-directories organized by smaller time units.\n"
                   "If you don't want your pictures organized by time answer No to all the following questions")
            try:
                time_organize_year_input = str(input("\nOrganize Picture by Year?: Yes/No (Default: Yes)\n"))
                if time_organize_year_input == "":
                    time_organize_year_input = True
                    break
                if time_organize_year_input not in self.input_validation_yes_no:
                    raise ValueError("Invalid Input")
            except ValueError:
                print("Input must be: Yes or No....")
            else:
                time_organize_year_input = input_converter(time_organize_year_input)
                break
        while True:
            try:
                time_organize_month_input = str(input("\nOrganize Picture by Month?: Yes/No (Default: No)\n"))
                if time_organize_month_input == "":
                    time_organize_month_input = False
                    break
                if time_organize_month_input not in self.input_validation_yes_no:
                    raise ValueError("Invalid Input")
            except ValueError:
                print("Input must be: Yes or No....")
            else:
                time_organize_month_input = input_converter(time_organize_month_input)
                break
        while True:
            try:
                time_organize_day_input = str(input("\nOrganize Picture by Day?: Yes/No (Default: No)\n"))
                if time_organize_day_input == "":
                    time_organize_day_input = False
                    break
                if time_organize_day_input not in self.input_validation_yes_no:
                    raise ValueError("Invalid Input")
            except ValueError:
                print("Input must be: Yes or No....")
            else:
                time_organize_day_input = input_converter(time_organize_day_input)
                break
        time_organization = frozenset[time_organize_year_input, time_organize_month_input, time_organize_day_input]
        self.session_options["time_organization"] = time_organization


# End input methods.
# Methods to process pictures are listed below
    # Goes through pictures
    def process_pictures(self, recursive):
        # Create directory, and any sub directories, to store pictures in for this session
        if self.session_options["os_type"] == "posix":
            self.create_directories_linux()
        if self.session_options["os_type"] == "nt":
            self.create_directories_windows()
        # Go through every picture in the directory


    # Create any directories required
    def create_directories_windows(self):
        # If new directories are to be created to store pictures, create them
        if self.session_options["modify_directory"] is False:
            # Create a new session directory to store pictures in
            createPictureDirectory(self.session_options["new_directory_object"])
            # Create sub directories to organize by time

        elif self.session_options["modify_directory"] is True:
            # Create sub directories (under working directory) to organize by time

    # Create any directories required
    def create_directories_linux(self):
        # If new directories are to be created to store pictures, create them
        if self.session_options["modify_directory"] is False:
            # Create a new session directory to store pictures in

            # Create sub directories to organize by time

        elif self.session_options["modify_directory"] is True:
            # Create sub directories (under working directory) to organize by time