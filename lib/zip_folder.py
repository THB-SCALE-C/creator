import io
import os
from typing import Any, List, TypedDict
import zipfile

class Content(TypedDict):
    filename:str
    path: str
    content: Any

def zip_folder(folder_path: str, contents:List[Content]) -> bytes:
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