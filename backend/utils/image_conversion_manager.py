import os
from typing import List

from pdf2image import convert_from_path
from PIL import Image


class ImageConversionManager:
    def __init__(self, file_paths: List[str]):
        self.file_paths = file_paths
        self.converted_file_paths: List[str] = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.converted_file_paths:
            for converted_file_path in self.converted_file_paths:
                if os.path.isfile(converted_file_path):
                    os.unlink(converted_file_path)  # Delete the file

    def convert_to_jpgs(self):
        if all(file_path.endswith(".pdf") for file_path in self.file_paths):
            return self._convert_pdfs_to_jpgs(self.file_paths)
        elif all(file_path.endswith(".png") for file_path in self.file_paths):
            return self._convert_pngs_to_jpgs(self.file_paths)
        else:
            print("All files must be of the same type (either all .pdf or all .png)")
            return []

    def _convert_pdfs_to_jpgs(self, file_paths: List[str]):
        jpg_file_paths = []
        for file_path in file_paths:
            if file_path.endswith(".pdf"):
                images = convert_from_path(file_path)
                base_filename = os.path.basename(file_path).replace(".pdf", "")
                output_folder = os.path.dirname(file_path)
                for i, image in enumerate(images):
                    jpg_filename = f"{base_filename}_page_{i + 1}.jpg"
                    jpg_file_path = os.path.join(output_folder, jpg_filename)

                    # Resize the image
                    # image.thumbnail((1024, 1024))

                    image.save(jpg_file_path, "JPEG")
                    jpg_file_paths.append(jpg_file_path)
        return jpg_file_paths

    def _convert_pngs_to_jpgs(self, file_paths: List[str]):
        jpg_file_paths = []
        for file_path in file_paths:
            if file_path.endswith(".png"):
                image = Image.open(file_path)
                rgb_im = image.convert("RGB")

                # Resize the image
                rgb_im.thumbnail((1024, 1024))

                base_filename = os.path.basename(file_path).replace(".png", ".jpg")
                output_folder = os.path.dirname(file_path)
                jpg_file_path = os.path.join(output_folder, base_filename)
                rgb_im.save(jpg_file_path, "JPEG")
                rgb_im.close()
                jpg_file_paths.append(jpg_file_path)
        return jpg_file_paths
