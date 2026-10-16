import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field, ValidationError

from backend.prompt.extraction_prompt import EXTRACTION_PROMPT

