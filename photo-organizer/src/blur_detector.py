from PIL import Image, ImageFilter
import os
from logger import log_progress

class BlurDetector:
    def __init__(self, logger=None, threshold=100):
        self.logger = logger
        self.threshold = threshold

    def is_blurry(self, image_path):
        try:
            image = Image.open(image_path).convert("L")
            laplacian = image.filter(ImageFilter.FIND_EDGES)
            variance = laplacian.getextrema()[1] - laplacian.getextrema()[0]
            return variance < self.threshold
        except Exception as e:
            log_progress(self.logger, f"Error analyzing {image_path}: {e}")
            return False

    def delete_blurry_photos(self, photos):
        count = 0
        for photo in photos:
            if self.is_blurry(photo):
                try:
                    os.remove(photo)
                    count += 1
                    log_progress(self.logger, f"Deleted blurry photo: {photo}")
                except Exception as e:
                    log_progress(self.logger, f"Error deleting {photo}: {e}")
        log_progress(self.logger, f"Deleted {count} blurry photos.")