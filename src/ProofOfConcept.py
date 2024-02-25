from pathlib import *
import shutil
import PIL.Image

session_options = {'root_directory_object': WindowsPath('D:/Picture_Manager_Test'), 'recurse_directory': True,
                   'modify_directory': False, 'new_directory_object': WindowsPath('D:/New_Picture_Manager_Test'),
                   'delete_duplicates': False, 'preserve_duplicates': True, 'delete_blurry': False,
                   'preserve_blurry': True, 're-orientate_pics': True,
                   'time_organization': frozenset[True, False, False], 'group_by_facial_recognition': False,
                   'os_type': 'nt'}

# Get string location of directory
picDirectoryString = "D:\\Picture_Manager_Test\\Simple_Test_Directory"
copyPicDirectoryString = "D:\\Picture_Manager_Test\\Copy_Test_Directory"

# Turn string into directory path
picDirectoryPath = Path(picDirectoryString)
copyPicDirectoryPath = Path(copyPicDirectoryString)

# Keep track of processed pics to prevent copying duplicates
processedPics = {}

# Get list of sub directories, Not needed - .glob automatically recursively searches a directory tree
#subDirectories = [x for x in picDirectoryPath.iterdir() if x.is_dir()]

# TODO Find a way to iterate through files only once. This could be done while processing files through iteration
#  instead of making lists to be processed later.
# Get list of all image files
picList = list(picDirectoryPath.glob('**/*.jpg'))
picList.extend(list(picDirectoryPath.glob('**/*.png')))
picList.extend(list(picDirectoryPath.glob('**/*.gif')))
picList.extend(list(picDirectoryPath.glob('**/*.HEIC')))

# Get list of all video files
videoList = list(picDirectoryPath.glob('*.MP4'))
videoList.extend(picDirectoryPath.glob('*.MOV'))
# Will change above to only iterate through directories/pics once, processing them as it goes

for pic in picList:
    # This grabs just the filename from the whole directory path
    # TODO Hash the file based on it's contents to detect duplicate photos with different names
    picName = pic.__str__().split('\\')[-1]

    # verify pic hasn't been processed - isn't a duplicate - then copy it
    if picName not in processedPics:
        # Add file to hashtable for quick check if another file is a duplicate
        processedPics[picName] = True

        # TODO separate creating directories based on time into another method
        # Organize photos in folders by year and month
        # Get time data from EXIF data (metadata) using PIL library
        picOpenInPil = PIL.Image.open(pic)
        picTakenDate = picOpenInPil.getexif()[306]
        yearTaken = picTakenDate.split(':')[0]
        monthTaken = picTakenDate.split(':')[1]

        if not Path(copyPicDirectoryPath.__str__() + '\\' + str(yearTaken)).exists():
            (copyPicDirectoryPath / str(yearTaken)).mkdir()
        if not Path(copyPicDirectoryPath.__str__() + '\\' + str(yearTaken) + '\\' + str(monthTaken)).exists():
            (copyPicDirectoryPath / str(yearTaken) / str(monthTaken)).mkdir()
        copyLocation = copyPicDirectoryPath / str(yearTaken) / str(monthTaken) / picName

        # TODO Create separate method for processing files in place without copying them

        # Copy the file to the new directory
        shutil.copyfile(pic, copyLocation)
    else:
        continue

