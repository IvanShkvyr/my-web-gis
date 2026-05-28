from enum import Enum


class UserRole(str, Enum):
    """Role define what a user can see and do."""
    USER = "user" # regular user
    DEMO = "demo" # public demo account
    ADMIN = "admin"

