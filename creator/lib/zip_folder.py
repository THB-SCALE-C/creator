import io
import os
from typing import Any, Sequence, TypedDict
import zipfile
import tempfile
import shutil
from pathlib import Path

from contextlib import contextmanager

class Content(TypedDict):
    filename:str
    path: str
    content: Any

def zip_folder(folder_path: str, contents:Sequence[Content]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, start=folder_path)
                zip_file.write(full_path, arcname)
        for content in contents:
            path_in_zip = os.path.join(content["path"], content["filename"])
            zip_file.writestr(path_in_zip, content["content"])
    buffer.seek(0)
    return buffer.getvalue()


def load_zip_to_temp(zip_path: str|Path, target_path:str|Path):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(target_path)
    return Path(target_path)