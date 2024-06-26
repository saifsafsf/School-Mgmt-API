"""This module extracts information from our `.env` file.
"""
import os

# pydantic used for data validation: https://pydantic-docs.helpmanual.io/
from pydantic import BaseSettings


def return_full_path(filename: str = ".env") -> str:
    """Uses os to return the correct path of the `.env` file."""
    absolute_path = os.path.abspath(__file__)
    directory_name = os.path.dirname(absolute_path)
    full_path = os.path.join(directory_name, filename)
    return full_path


class Settings(BaseSettings):
    """Uses pydantic to define settings for project."""

    db_user: str
    db_pass: str
    db_host: str
    db_name: str

    class Config:
        env_file = return_full_path(".env")


# Create instance of `Settings` class
settings = Settings()