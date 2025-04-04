import os
import shutil

class FileManager:
    @staticmethod
    def create_folder(path):
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def copy_file(src, dst):
        shutil.copyfile(src, dst)

    @staticmethod
    def validate_image_path(path):
        return os.path.isfile(path) and path.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))