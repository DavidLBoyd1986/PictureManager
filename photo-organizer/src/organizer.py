import os
from utils.file_utils import get_photos
from duplicate_finder import DuplicateFinder
from blur_detector import BlurDetector
from logger import log_progress

class PhotoOrganizer:
    def __init__(self, options):
        self.options = options
        self.logger = options.logger

    def organize(self):
        photos = self._scan_photos()
        log_progress(self.logger, f"Found {len(photos)} photos.")
        if self.options.delete_duplicates:
            dup_finder = DuplicateFinder(self.logger)
            duplicates = dup_finder.find_duplicates(photos)
            dup_finder.delete_duplicates(duplicates)
        if self.options.delete_blurry:
            blur_detector = BlurDetector(self.logger)
            blur_detector.delete_blurry_photos(photos)
        self._organize_by_time(photos)
        log_progress(self.logger, "Organization complete.")

    def _scan_photos(self):
        return get_photos(self.options.directory, self.options.recursive)

    def _organize_by_time(self, photos):
        import shutil
        from PIL import Image
        from PIL.ExifTags import TAGS
        from datetime import datetime

        def get_date_taken(path):
            try:
                image = Image.open(path)
                exif = image._getexif()
                if exif:
                    for tag, value in exif.items():
                        decoded = TAGS.get(tag, tag)
                        if decoded == "DateTimeOriginal":
                            return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
            except Exception:
                pass
            return None

        for photo in photos:
            date_taken = get_date_taken(photo)
            if not date_taken:
                continue
            parts = [str(date_taken.year)]
            if self.options.levels > 1:
                parts.append(f"{date_taken.month:02d}")
            if self.options.levels > 2:
                parts.append(f"{date_taken.day:02d}")
            dest_dir = os.path.join(self.options.directory, *parts)
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, os.path.basename(photo))
            if os.path.abspath(photo) != os.path.abspath(dest_path):
                shutil.move(photo, dest_path)
                log_progress(self.logger, f"Moved {photo} -> {dest_path}")