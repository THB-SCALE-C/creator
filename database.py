import os
from typing import Generator
from fastapi import HTTPException
from supabase import Client, create_client

if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL") or ""
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY") or ""

if not all([SUPABASE_KEY, SUPABASE_URL]):
    raise ValueError("Supabase key and value must be not none.")


def get_supabase() -> Generator[Client, None, None]:
    client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    yield client