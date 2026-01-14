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



@contextmanager
def load_zip_as_context(zip_path: str):
    temp_dir = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)
        yield Path(temp_dir)
    finally:
        shutil.rmtree(temp_dir)


def load_zip_to_temp(zip_path: str):
    temp_dir = tempfile.mkdtemp(suffix="unit_assembler")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir)
    return Path(temp_dir)

def remove_temp(temp_dir: str|Path):
    shutil.rmtree(temp_dir)