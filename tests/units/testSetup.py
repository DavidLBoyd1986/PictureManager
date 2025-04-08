from pathlib import Path
import shutil

# Below is the permanent test directory location that will be copied into test functions:
#   D:\Picture_Manager_Test\test_directories\unit_testing\test_setup_directories


def setup_test_organize_pic_by_time():
    """
    Setups the directories required to test _organize_pic_by_time() function


    :return:
    """

    # TODO Change directories to be a part of the project, so other users have testing when importing project
    # TODO Change pictures to be generic so they don't identify me or have my family in them
    # Specify the source and destination directories
    source_directory = r'D:\Picture_Manager_Test\test_directories\unit_testing\test_setup_directories\test_organize_pic_by_time_source_directory'
    destination_directory = r"D:\Picture_Manager_Test\test_directories\unit_testing\test_organize_pic_by_time\temp_dir"

    test_dir = r"D:\Picture_Manager_Test\test_directories\unit_testing\test_organize_pic_by_time"

    # Change this to try with exception
    if Path(destination_directory).exists():
        Path(destination_directory).rmdir()

    # Use shutil to copy files
    try:
        # Copy all files from source to destination
        shutil.copytree(source_directory, destination_directory)
        print(f"Files copied successfully from '{source_directory}' to '{destination_directory}'.")
    except Exception as e:
        print(f"Error copying files: {e}")


setup_test_organize_pic_by_time()
