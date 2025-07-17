import hashlib
import os
from logger import log_progress

class DuplicateFinder:
    def __init__(self, logger=None):
        self.logger = logger

    def find_duplicates(self, photos):
        hashes = {}
        duplicates = []
        for photo in photos:
            try:
                file_hash = self._hash_file(photo)
                if file_hash in hashes:
                    duplicates.append(photo)
                else:
                    hashes[file_hash] = photo
            except Exception as e:
                log_progress(self.logger, f"Error hashing {photo}: {e}")
        log_progress(self.logger, f"Found {len(duplicates)} duplicate photos.")
        return duplicates

    def delete_duplicates(self, duplicates):
        count = 0
        for photo in duplicates:
            try:
                os.remove(photo)
                count += 1
                log_progress(self.logger, f"Deleted duplicate: {photo}")
            except Exception as e:
                log_progress(self.logger, f"Error deleting {photo}: {e}")
        log_progress(self.logger, f"Deleted {count} duplicate photos.")

    def _hash_file(self, path, block_size=65536):
        hasher = hashlib.md5()
        with open(path, 'rb') as f:
            buf = f.read(block_size)
            while buf:
                hasher.update(buf)
                buf = f.read(block_size)
        return hasher.hexdigest()