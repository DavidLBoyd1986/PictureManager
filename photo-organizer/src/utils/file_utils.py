import os

def get_photos(directory, recursive=True, extensions=None):
    if extensions is None:
        extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
    photos = []
    for root, _, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1].lower() in extensions:
                photos.append(os.path.join(root, file))
        if not recursive:
            break
    return photos