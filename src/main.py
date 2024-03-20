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
    # session_manager = SessionManager()

    # skipping user input everytime during development. Will pull this from SessionManager for actual code.
    # todo Create test data that can be supplied to SessionManager during testing

    # Simple Integration Tests
    session_options_simple = {'root_directory_object': WindowsPath("D:\\Picture_Manager_Test\\simple_test_directory"),
                              'recurse_directory': True, 'modify_directory': False,
                              'new_directory_object': WindowsPath("D:\\Picture_Manager_Test\\simple_copy_directory"),
                              'delete_duplicates': False, 'preserve_duplicates': True, 'delete_blurry': False,
                              'preserve_blurry': True, 're-orientate_pics': True,
                              'time_organization': frozenset[True, False, False], 'group_by_facial_recognition': False,
                              'os_type': 'nt'}

    PictureProcessor(session_options_simple)

    # Medium Integration Tests
    session_options_medium = {'root_directory_object': WindowsPath("D:\\Picture_Manager_Test\\medium_test_directory"),
                              'recurse_directory': True, 'modify_directory': False,
                              'new_directory_object': WindowsPath("D:\\Picture_Manager_Test\\medium_copy_directory"),
                              'delete_duplicates': False, 'preserve_duplicates': True, 'delete_blurry': False,
                              'preserve_blurry': True, 're-orientate_pics': True,
                              'time_organization': frozenset[True, False, False], 'group_by_facial_recognition': False,
                              'os_type': 'nt'}

    PictureProcessor(session_options_medium)

    # Simple Integration Tests
    session_options_large= {'root_directory_object': WindowsPath("D:\\Picture_Manager_Test\\large_test_directory"),
                              'recurse_directory': True, 'modify_directory': False,
                              'new_directory_object': WindowsPath("D:\\Picture_Manager_Test\\large_copy_directory"),
                              'delete_duplicates': False, 'preserve_duplicates': True, 'delete_blurry': False,
                              'preserve_blurry': True, 're-orientate_pics': True,
                              'time_organization': frozenset[True, False, False], 'group_by_facial_recognition': False,
                              'os_type': 'nt'}

    # PictureProcessor(session_options_large)

    # Large Integration Tests
