# from PIL import Image
# import pdf2image


# class ImageConversionManager:
#     def __init__(self, output_folder):
#         self.output_folder = output_folder

#     def convert_to_jpg(self, file_path):
#         if file_path.endswith(".pdf"):
#             return self._convert_pdf_to_jpg(file_path)
#         elif file_path.endswith(".png"):
#             return self._convert_png_to_jpg(file_path)
#         # Add more conditions for other file types if needed

#     def _convert_pdf_to_jpg(self, file_path):
#         images = pdf2image.convert_from_path(file_path)
#         for i, image in enumerate(images):
#             image.save(file_path.replace(".pdf", "") + str(i) + ".jpg", "JPEG")
#         return file_path.replace(".pdf", "") + "0.jpg"

#     def _convert_png_to_jpg(self, file_path):
#         with Image.open(file_path) as img:
#             rgb_im = img.convert("RGB")
#             rgb_im.save(file_path.replace(".png", ".jpg"), "JPEG")
#         return file_path.replace(".png", ".jpg")


import os
import tempfile
from PIL import Image
from pdf2image import convert_from_path


class ImageConversionManager:
    def __init__(self, file_path: str, output_folder: str):
        self.file_path = file_path
        self.output_folder = output_folder

    def __enter__(self):
        self.output_folder = tempfile.mkdtemp()  # Create a temporary directory
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.output_folder and os.path.isdir(self.output_folder):
            for filename in os.listdir(self.output_folder):
                file_path = os.path.join(self.output_folder, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)  # Delete the file
            os.rmdir(self.output_folder)  # Delete the directory

    def convert_to_jpg(self, file_path):
        if file_path.endswith(".pdf"):
            return self._convert_pdf_to_jpg(file_path)
        elif file_path.endswith(".png"):
            return self._convert_png_to_jpg(file_path)
        # Add more conditions for other file types if needed

    def _convert_pdf_to_jpg(self, file_path):
        images = convert_from_path(file_path)
        jpg_files = []
        for i, image in enumerate(images):
            jpg_filename = f"output_page_{i}.jpg"
            jpg_file_path = os.path.join(self.output_folder, jpg_filename)
            image.save(jpg_file_path, "JPEG")
            jpg_files.append(jpg_file_path)
        return jpg_files

    def _convert_png_to_jpg(self, file_path):
        rgb_im = Image.open(file_path).convert("RGB")
        jpg_filename = os.path.basename(file_path).replace(".png", ".jpg")
        jpg_file_path = os.path.join(self.output_folder, jpg_filename)
        rgb_im.save(jpg_file_path, "JPEG")
        rgb_im.close()
        return jpg_file_path
