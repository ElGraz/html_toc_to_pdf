from dataclasses import dataclass


@dataclass
class Page:
    """Data class for destination page"""
    num: int = 0
    url: str = None
    desc: str = None

