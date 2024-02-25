from SessionManager import SessionManager
from PictureProcessor import PictureProcessor
from pathlib import Path
from pathlib import WindowsPath

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Get user input for the session
    #session_manager = SessionManager()

    # skipping user input everytime during development. Will pull this from SessionManager for actual code.
    #todo Create test data that can be supplied to SessionManager during testing
    session_options = {'root_directory_object': WindowsPath("D:\\Picture_Manager_Test\\Simple_Test_Directory"), 'recurse_directory': True,
                       'modify_directory': False, 'new_directory_object': WindowsPath("D:\\Picture_Manager_Test\\Copy_Test_Directory"),
                       'delete_duplicates': False, 'preserve_duplicates': True, 'delete_blurry': False,
                       'preserve_blurry': True, 're-orientate_pics': True,
                       'time_organization': frozenset[True, False, False], 'group_by_facial_recognition': False,
                       'os_type': 'nt'}

    PictureProcessor(session_options)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
