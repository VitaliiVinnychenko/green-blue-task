from enum import Enum


class Category(str, Enum):
    LAPTOP = "laptop"
    PHONE = "phone"
    KITCHEN = "kitchen"
    OTHER = "other"
