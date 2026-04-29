import os
import shutil
from fastapi import UploadFile
import uuid

def save_img(file: UploadFile, folder="static/images/") -> str:
    """
    Save an uploaded image to a folder and return only the filename.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)

    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"

    file_path = os.path.join(folder, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return filename   # 👈 Sirf filename return hoga