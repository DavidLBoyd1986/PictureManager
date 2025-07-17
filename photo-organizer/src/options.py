class OrganizerOptions:
    def __init__(self, directory, levels=3, delete_duplicates=False, delete_blurry=False, recursive=True, logger=None):
        self.directory = directory
        self.levels = levels
        self.delete_duplicates = delete_duplicates
        self.delete_blurry = delete_blurry
        self.recursive = recursive
        self.logger = logger