from flask import Flask, render_template, request, redirect, url_for
from recipe import Recipe
from recipedao import RecipeDao

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

recipedao = RecipeDao('recipes.db')
recipedao.create_table()

def generate_testdata():
    if len(recipedao.get_all_items()) == 0:
        recipedao.add_item(Recipe(1, "Spaghetti Bolognese", ["Spaghetti", "Rinderhackfleisch", "Tomatensauce", "Zwiebeln", "Knoblauch"], ["Nudeln kochen", "Fleisch anbraten", "Sauce hinzufügen"], 2))
        recipedao.add_item(Recipe(2, "Caesar Salad", ["Römersalat", "Hähnchenbrust", "Caesar Dressing", "Parmesan", "Croutons"], ["Salat waschen", "Hähnchen anbraten", "Dressing hinzugeben"], 4))
        recipedao.add_item(Recipe(3, "Tomatensuppe", ["Tomaten", "Zwiebeln", "Knoblauch", "Brühe", "Basilikum"], ["Zwiebeln und Knoblauch anbraten", "Tomaten hinzufügen", "Mit Brühe aufkochen"], 3))
        recipedao.add_item(Recipe(4, "Pancakes", ["Mehl", "Milch", "Eier", "Backpulver", "Zucker"], ["Zutaten vermischen", "Teig in Pfanne geben", "Beidseitig braten"], 2))
        recipedao.add_item(Recipe(5, "Avocado Toast", ["Avocado", "Brot", "Salz", "Pfeffer", "Zitronensaft"], ["Brot toasten", "Avocado zerdrücken", "Auf Brot verteilen"], 1))

generate_testdata()

@app.route('/')
def index():
    recipes = recipedao.get_all_items()
    return render_template('index.html', recipes=recipes)

@app.route('/<int:recipe_id>')
def get_recipe(recipe_id):
    recipe = recipedao.get_item(recipe_id)
    return render_template('recipe.html', recipe=recipe)

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        get_form_field = lambda field: request.form.get(field, '').strip()

        name = get_form_field('name')
        ingredients = list(filter(lambda x: x, get_form_field('ingredients').split(',')))
        instructions = list(filter(lambda x: x, get_form_field('instructions').split(',')))
        difficulty = get_form_field('difficulty')

        if name and ingredients and instructions and difficulty.isdigit():
            difficulty = int(difficulty)

            all_recipes = recipedao.get_all_items()
            new_id = max([r.recipe_id for r in all_recipes], default=-1) + 1

            new_recipe = Recipe(
                recipe_id=new_id,
                name=name,
                ingredients=ingredients,
                instructions=instructions,
                difficulty=difficulty
            )

            recipedao.add_item(new_recipe)
            return redirect(url_for('index'))
        else:
            return render_template('add_recipe.html', error="Bitte füllen Sie alle Felder aus und stellen Sie sicher, dass die Schwierigkeit eine Zahl ist.")

    return render_template('add_recipe.html')

@app.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    recipe = recipedao.get_item(recipe_id)

    if not recipe:
        return redirect(url_for('index'))

    if request.method == 'POST':

        get_form_field = lambda field: request.form.get(field, '').strip()

        name = get_form_field('name')
        ingredients = list(filter(lambda x: x, get_form_field('ingredients').split(',')))
        instructions = list(filter(lambda x: x, get_form_field('instructions').split(',')))
        difficulty = get_form_field('difficulty')

        if name and ingredients and instructions and difficulty.isdigit():
            difficulty = int(difficulty)

            recipe.name = name
            recipe.ingredients = ingredients
            recipe.instructions = instructions
            recipe.difficulty = difficulty

            recipedao.update_item(recipe)
            return redirect(url_for('get_recipe', recipe_id=recipe.recipe_id))
        else:
            return render_template('edit_recipe.html', recipe=recipe, error="Bitte füllen Sie alle Felder aus und stellen Sie sicher, dass die Schwierigkeit eine Zahl ist.")

    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    recipe = recipedao.get_item(recipe_id)
    if not recipe:
        return redirect(url_for('index'))
    else:
        recipedao.delete_item(recipe_id)
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
