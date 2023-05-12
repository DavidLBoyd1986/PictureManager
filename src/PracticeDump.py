from pathlib import Path, WindowsPath

# Get string location of directory
picDirectoryString = "D:\Picture_Manager_Test\Simple_Test_Directory"
copyPicDirectoryString = "D:\Picture_Manager_Test\Copy_Test_Directory"

# Turn string into directory path
picDirectoryPath = Path(picDirectoryString)
copyPicDirectoryPath = Path(copyPicDirectoryString)

picList = list(picDirectoryPath.glob('**/*.jpg'))
picList.extend(list(picDirectoryPath.glob('**/*.png')))
picList.extend(list(picDirectoryPath.glob('**/*.gif')))
picList.extend(list(picDirectoryPath.glob('**/*.HEIC')))

# Keep track of processed pics to prevent copying duplicates
processedPics = {}


for image_path in picList:

    if (not issubclass(type(image_path), Path)) and (not isinstance(image_path, Path)):
        raise TypeError("The image_path submitted was not of type Path or str.")

    image_file_name = image_path.__str__().split('\\')[-1]
    print(type(image_file_name))
    print(image_file_name)
