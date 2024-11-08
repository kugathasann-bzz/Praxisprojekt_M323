"""Praxisprojekt Rezepte - Neeraja Kugathasan"""

from dataclasses import dataclass
from typing import List


@dataclass
class Recipe:
    recipe_id: int
    name: str
    ingredients: List[str]
    instructions: List[str]
    difficulty: int

