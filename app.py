# cd recipes
# .\venv\Scripts\Activate
# python app.py

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

cookbook = []
class Recipe:
    def __init__(self, title, ingredients, instructions, tags):
        self.Title = title
        self.Ingredients = ingredients
        self.Instructions = instructions
        self.Tags = tags

def add_to_cookbook(recipe):
    cookbook.append(recipe)

def remove_from_cookbook(recipe):
    cookbook.remove(recipe)

def update_cookbook(recipe, new_recipe):
    cookbook.remove(recipe)
    cookbook.append(new_recipe)

def save_cookbook():
    with open('data.txt', 'w') as file:
        file.write("Family Cookbook")
        for recipe in cookbook:
            file.write(f"\n{recipe.Title}\n{recipe.Ingredients}\n{recipe.Instructions}\n{recipe.Tags}")

def load_cookbook():
    with open('data.txt', 'r') as file:
        # lines = file.readlines()
        lines = file.readlines()[1:]
        for i in range(0, len(lines), 4):
            if i + 3 < len(lines):
                recipe = Recipe(lines[i].strip(), lines[i+1].strip(), lines[i+2].strip(), lines[i+3].strip())
                cookbook.append(recipe)

def sort_cookbook_by_name():
    cookbook.sort(key=lambda x: x.Title.upper())

def sort_cookbook_by_tags():
    # sort_cookbook_by_name()
    cookbook.sort(key=lambda x: x.Tags.upper())

@app.route('/api/get-cookbook', methods=['GET'])
def get_cookbook():
    load_cookbook()
    sort_cookbook_by_tags()
    return jsonify({"data": cookbook})









def sort_by_name():
    with open('data.txt', 'r') as file:
        lines = file.readlines()
    
    recipes = []
    for i in range(0, len(lines), 4):
        if i + 3 < len(lines):
            recipe = [lines[i].strip(), lines[i+1].strip(), lines[i+2].strip(), lines[i+3].strip()]
            recipes.append(recipe)
    
    recipes.sort(key=lambda x: x[0].upper())
    
    with open('data.txt', 'w') as file:
        for i, recipe in enumerate(recipes):
            file.write('\n'.join(recipe))
            if i < len(recipes) - 1:
                file.write('\n')


@app.route('/api/read-file', methods=['GET'])
def read_file():
    try:
        with open('data.txt', 'r') as file:
            lines = file.readlines()
        
        # Group lines into chunks of 4
        grouped_lines = [lines[i:i + 4] for i in range(0, len(lines), 4)]
        
        # Remove newline characters and strip lines
        grouped_lines = [[line.strip() for line in group] for group in grouped_lines]
        
        return jsonify({"data": grouped_lines})
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/write-file', methods=['POST'])
def write_file():
    try:
        contentTitle = request.json.get('content_title')
        contentIngredients = request.json.get('content_ingredients')
        contentInstructions = request.json.get('content_instructions')
        contenttags = request.json.get('content_tags')
        print('\n')
        print(contentTitle + contentIngredients + contentInstructions + contenttags)
        with open('data.txt', 'a+') as file:
            file.write("\n" + contentTitle)
            file.write("\n" + contentIngredients)
            file.write("\n" + contentInstructions)
            file.write("\n" + contenttags)
            
        sort_by_name()
        return jsonify({"message": "Recipe Added successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/delete-file', methods=['POST'])
def delete_file():
    try:
        index = request.json.get('content')
        index = index * 4
        with open('data.txt', 'r') as file:
            lines = file.readlines()

        del lines[index:index + 4]
        if lines and lines[-1].endswith('\n'):
            lines[-1] = lines[-1].rstrip('\n')

        with open('data.txt', 'w') as file:
            file.writelines(lines)
        return jsonify({"message": "Recipe deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/update-file', methods=['POST'])
def update_file():
    try:
        index = request.json.get('index')
        index = index * 4
        contentTitle = request.json.get('content_title')
        contentIngredients = request.json.get('content_ingredients')
        contentInstructions = request.json.get('content_instructions')
        contenttags = request.json.get('content_tags')

        with open('data.txt', 'r') as file:
            lines = file.readlines()

        lines[index] = contentTitle + '\n'
        lines[index + 1] = contentIngredients + '\n'
        lines[index + 2] = contentInstructions + '\n'
        lines[index + 3] = contenttags + '\n'

        with open('data.txt', 'w') as file:
            file.writelines(lines)

        sort_by_name()
        return jsonify({"message": "Recipe updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

# Berry Filled Sweet Bread
# Yeast 2 1/4 tsp, Sugar 1 cup and 1 tbsp, Warm Water 2 cups, Salt 1 tsp, flour 5-6 cups and 2 tbsp, Frozen Berries 1-2 cups, Lemon Juice 1 tbsp, Cornstarch Slurry 1 tbsp, Cream Cheese 8oz, Whipped Cream 1/4 cup, Powdered Sugar 1-2 cup, 1 Egg
# Dough: Gently stir 2 1/4 tsp yeast, 1 tbsp sugar, and 1/4 cup of warm water in a large bowl. Cover the bowl with a dish towel and let it rise a little, approximately 10-15 minutes. Then add an additional 1/2 cup of sugar, 1 3/4 cup of warm water, and 1 tsp salt. Add in 5 cups of flour. Knead the dough while adding in up to 1 more cup of flour, just until the dough has the right consistency. Place the dough in a lightly greased bowl somewhere warm. Cover with a dish towel and let rise for approximately 1 hour. - Berry Compote: Put 1-2 cups of frozen berries in a pot and 1/2 cup of sugar, more or less depending on the taste, 1 tbsp lemon juice, and 1 tbsp cornstarch. For this part of the recipe, you can adjust the amount of all the ingredients to your liking. Just remember, if you decide to add more cornstarch after the compote has heated up, you must add it in a slurry. Mix the cornstarch with a little water until the cornstarch is fully combined, then pour it into the compote. - Cream Cheese Filling: Microwave the cream cheese for about 30 seconds, or until it's soft. Add 1/4 cup whipped cream, 1-2 cups powdered sugar, just add poudered sugar until you like the taste, and finally add 1 tbsp flour. Stir until fully combined. - Combine and Bake: Once your dough has risen, preheat your oven to 350�F. Take the dough and roll it out on a floured surface. mentally divide the dough into three equal parts lengthwise. Cut the two outer sections into strips, going horizontally, such that the strips are still connected to the main part of the dough. Cover the middle portion of the dough with the cream cheese filling. Make a little well in the filling, going lengthwise. Fill the well with the berry compote. Take the strips on the sides of the dough, fold them over the top, and braid. place on a baking sheet, get a bowl and crack one egg in it and beat the egg, paint the top of the loaf with the egg, sprinkle with sugar, and bake for about 30 minutes, or until golden brown. - Serve: Once the bread is ready, remove the bread from the oven and let it cool down. Serve and enjoy!
# /images/berry-filled-sweet-bread.jpg
# Berry Scones
# Flour 2 cups, Sugar 1/3 cup, Baking Powder 2 tsp, Salt 1/2 tsp, Butter 1/2 cup, Frozen Berries, 1 Lemon Zest, Heavy Cream 3/4 cup, 1 egg
# Combine sugar and lemon zest together and smoosh it between your fingers until it feels like wet sand. Combine dry ingredients in bowl including lemon sugar. - In another bowl combine heavy cream and egg. - Cut cold butter into 1 cm cubes. Add butter to dry ingredients and squish butter cubes into the mixture the way you would for biscuits or a rough pie dough. Add frozen fruit to dry mixture and mix. Add wet mixture to dry until fully combined. - Roll into a circular shape, approx. 1/2 an inch tall and freeze. - Cut into triangles, brush with heavy cream and sprinkle with sugar and bake at 350 for about 20 min or until golden brown. After they cool, dust with powdered sugar.
# none
# Creamy Potato Soup
# Butter 1/2 cup, 1/2 Onion, flour 1/2 cup, Water or Broth 2-3 cups, milk 1 cup, pepper 1/2 tsp, garlic powder 1/2 tsp, thyme 1 tsp, salt 1 tsp, 1 bag frozen peas and carrots, 2 cubed potatoes, 2 chicken breasts
# Cube and boil potatoes till fork tender but not super soft or when you mix it, you will have mashed potatoes in your soup. Set them aside. - Boil the chicken, shred it, set it aside. - Cut up your onion and cook it with the butter in a pot until onion is thoroughly cooked. Add flour and mix continually (your making a roux, don't let it burn). Add small amounts of milk at a time and mix so it stays thick, do the same for water / broth. Add all your seasonings into the pot and mix. Add frozen veggies and cook until they aren't frozen anymore. Add potatoes and chicken and heat up. Once it's all warm it's finished.
# none
# Egg roll in a bowl
# 1 pound lean ground beef, 1 tbsp olive oil, 1/2 tsp salt, 1/4 tsp pepper, 1/2 onion finely diced, 1 carrot julienned or coarsely grated, 3 cloves of minced garlic, 3 cups cabbage thinly sliced, 1 tsp ground ginger, 1/4 cup low sodium soy sauce, 2 tsp sesame oil, 1/2 tsp sugar, 1 tbsp chopped green onion optional, 1/4 tsp sesame seeds optional
# Set a large skillet over medium/high heat and add oil. Once hot, add ground beef and brown until no longer pink, about 5 minutes, breaking up the meat with a spatula as it's cooked. Season with salt and pepper. - Add onion and carrots and saute until onion is tender, 5-7 minutes, stirring occasionally. Add the garlic and cook another 30 seconds, stirring constantly. - Finally add the cabbage, ginger, soy sauce, sesame oil, and sugar. Continue sauteeing for 5-7 minutes, stirring occasionally, or until cabbage is tender.
# /images/egg-roll-in-a-bowl.jpg
# Fried Rice
# Day Old Rice, Soy Sauce, Brown Sugar, Sesame Oil, Frozen Veggies, Chicken, Eggs, Garlic Powder, Ginger, Salt, Pepper
# Cook your eggs with salt pepper and garlic powder and set it aside. Cook your chicken with whatever seasonings you want into bite sized cubes and set it aside. - Add rice to pan with oil and cook on high heat breaking apart the rice. After rice is broken apart add soy sauce, sesame oil, brown sugar, garlic powder, ginger, pepper, and salt all to taste. Then ass veggies and cook until veggies are done stirring occasionally. Then add eggs and chicken back into it and cook just until eggs and chicken are warmed up
# none
# Taco Soup
# Beef, Bell Pepers 1-2, Onion 1, Oil / Butter 1 tbsp, Diced Garlic 1 tbsp optional, Beef Broth or Water, Tomato Chunks 1-2 cans, Black Beans 1-2 cans, Corn 1 can, Chicken Bullion 2-4 tbsp, Cumin 2-4 tbsp, Garlic Powder 1-2 tbsp, Red Pepper Flakes 1 tsp, Black Pepper 1-2 tsp, Salt to taste, Cilantro optional, Sour Cream optional, Tortilla Chips optional, Fresh Diced Tomatos optional, Diced Avocato optional
# Cook the ground beef without seasonings and set aside. Dice the onions and bell peppers. Put the onions, bell peppers, and diced garlic in a pot with some oil or butter and saute until soft. Add all the canned food to the pot, and then add your beef broth until it is the right thickness. Add all the seasonings. Make sure to taste as you go; add more or less of whatever you like. Cook until boiling; add the beef you set aside to the pot, and then it's ready to sever. Optionally, you can add cilantro, sour cream, tortilla chips, Fresh Diced Tomatos, and Diced Avocato as toppings.
# /images/taco-soup.jpg