from typing import Any
import yaml
import os


# def load_jinja_templates_from_supabase(
#     supabase:Client,
#     bucket: str,
#     root_folder: str = "",
#     valid_ext=(".jinja", ".j2", ".html")
# ) -> dict[str, Template]:
#     templates = {}

#     def to_text(data):
#         # normalize all possible binary formats
#         if isinstance(data, (bytes, bytearray, memoryview)):
#             return bytes(data).decode("utf-8")
#         return data

#     def walk(folder: str):
#         entries = supabase.storage.from_(bucket).list(folder)
#         if not entries:
#             return

#         for e in entries:
#             name = e["name"]
#             full_path = f"{folder}/{name}" if folder else name

#             # folders in supabase list() are entries with 'metadata' = None
#             if e.get("metadata") is None:
#                 walk(full_path)
#                 continue

#             if not name.lower().endswith(valid_ext):
#                 continue

#             raw = supabase.storage.from_(bucket).download(full_path)
#             content = to_text(raw)

#             key_name = os.path.splitext(full_path)[0]
#             templates[key_name] = Template(content)

#     walk(root_folder)
#     return templates

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) 
