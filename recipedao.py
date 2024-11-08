"""Praxisprojekt Rezepte - Neeraja Kugathasan"""

import sqlite3
import json
from recipe import Recipe

class RecipeDao:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_table(self):
        # Dropping the table if it already exists
        self.cursor.execute("DROP TABLE IF EXISTS recipe")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipe (
                recipe_id INTEGER PRIMARY KEY,
                name TEXT,
                ingredients TEXT,  
                instructions TEXT, 
                difficulty INTEGER
            )
        """)
        self.conn.commit()

    def add_item(self, recipe):
        # Insert with recipe_id explicitly
        self.cursor.execute(
            "INSERT INTO recipe (recipe_id, name, ingredients, instructions, difficulty) VALUES (?, ?, ?, ?, ?)",
            (recipe.recipe_id, recipe.name, json.dumps(recipe.ingredients), json.dumps(recipe.instructions), recipe.difficulty)
        )
        self.conn.commit()

    def get_item(self, recipe_id):
        self.cursor.execute("SELECT * FROM recipe WHERE recipe_id = ?", (recipe_id,))
        row = self.cursor.fetchone()
        if row:
            return Recipe(row[0], row[1], json.loads(row[2]), json.loads(row[3]), row[4])
        return None

    def get_all_items(self):
        self.cursor.execute("SELECT * FROM recipe")
        rows = self.cursor.fetchall()
        items = [Recipe(row[0], row[1], json.loads(row[2]), json.loads(row[3]), row[4]) for row in rows]
        return items

    def update_item(self, recipe):
        self.cursor.execute(
            "UPDATE recipe SET name = ?, ingredients = ?, instructions = ?, difficulty = ? WHERE recipe_id = ?",
            (recipe.name, json.dumps(recipe.ingredients), json.dumps(recipe.instructions), recipe.difficulty, recipe.recipe_id)
        )
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def delete_item(self, recipe_id):
        self.cursor.execute("DELETE FROM recipe WHERE recipe_id = ?", (recipe_id,))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def close(self):
        self.conn.close()
