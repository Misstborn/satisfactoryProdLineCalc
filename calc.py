import json
from copy import copy

EXTRACTED_ITEMS = ('Iron Ore', 'Copper Ore', 'Caterium Ore', 'Limestone', 'Coal', 'Raw', 'Sulfur', 'Bauxite', 'Uranium'
                    , 'SAM', 'Water', 'Crude Oil', 'Nitrogen Gas', 'FICSMAS Gift', 'Mycelia', 'Beryl Nut', 'Paleberry',
                    'Bacon Agaric', 'Blue Power Slug', 'Yellow Power Slug', 'Purple Power Slug', 'Hog Remains',
                    'Hatcher Remains', 'Spitter Remains', 'Stinger Remains', 'Wood', 'Leaves')

# Recipe class, only used to define an object with certain attributes. New instances should not be created after the
# initial list of all recipes.
class Recipe:
    all_recipes = []

    def __init__(self, name, alt, ficsmas, building, ingredients, outputs):
        # Initialization
        self.name = name
        self.building = building
        self.alt = alt
        self.ficsmas = ficsmas
        self.ingredients = ingredients
        self.outputs = outputs
        self.items = [item['Item'] for item in outputs]
        self.ipm = [item['Per-minute'] for item in outputs]
        self.clockspeed = 1
        self.is_base = True if self.ingredients is None else False  # If item is a "base" ingredient, aka cannot be crafted
        # self.children = self.get_ingredients()

        # Add this instance to the list of all recipes
        Recipe.all_recipes.append(self)

    def __contains__(self, _item):
        # Allows to check if a given item is an output of a Recipe with in.
        if not isinstance(_item, str):
            raise TypeError("Item is not a string")

        return _item in self.items

    def calc_clockspeed(self):
        pass

    # Currently unused
    def get_ingredients(self):
        if not self.is_base:
            return [Item.all_items[Item.all_items.index(ingredient['Item'])] for ingredient in self.ingredients]
        else:
            return None

# print('here')
# Similar to recipe, new instances should not be created. Contains a list of every item along with each recipe that can
# create that item
class Item:

    all_items = []

    def __init__(self, name, recipe, add_to_list=True):
        # Initialization
        self.name = name
        self.recipes = [recipe]
        self.node_index = 1

        if add_to_list:
            self.__add_to_list()

    def get_full_tree(self):
        recipe_tree = {'Node0Children': [copy(self)]}
        current_index = 0
        node_number = 1

        while len(recipe_tree) - current_index > 0:
            for __item in recipe_tree[f'Node{current_index}Children']:
                ingredients = __item.recipes[0].get_ingredients()
                output_ingredients = []
                if ingredients is not None:
                    for ingredient in ingredients:
                        node_number += 1
                        ingredient_copy = copy(ingredient)
                        ingredient_copy.node_index = node_number
                        output_ingredients.append(ingredient_copy)

                    recipe_tree[f'Node{__item.node_index}Children'] = output_ingredients

                else:
                    recipe_tree[f'Node{__item.node_index}Children'] = []

            current_index += 1

        return recipe_tree

    def __add_to_list(self):
        """Intended for internal use only."""
        # Check if an item with the same name already exists
        for _item in Item.all_items:
            if _item.name == self.name:
                # If found, add recipe to the existing item
                _item.recipes.extend(self.recipes)
                break
        else:
            # If no matching item is found, add self to all_items
            Item.all_items.append(self)

    def order_recipes(self):

        actual_index = 0
        for _ in range(len(self.recipes)):
            __recipe = self.recipes[actual_index]
            if __recipe.alt:
                self.recipes.append(self.recipes.pop(actual_index))

            elif __recipe.building == 'Converter' and __recipe.ingredients is not None and len(__recipe.ingredients) == 2:
                self.recipes.append(self.recipes.pop(actual_index))

            elif len(__recipe.items) == 2 and __recipe.items[1] == self.name:
                self.recipes.append(self.recipes.pop(actual_index))

            elif __recipe.building == 'Packager':
                self.recipes.append(self.recipes.pop(actual_index))

            elif __recipe.is_base:
                self.recipes.insert(0, self.recipes.pop(actual_index))
                actual_index += 1

            else:
                actual_index += 1

    def append(self, recipe):
        # Add a recipe to the list.
        self.recipes.append(recipe)

    def extend(self, iterable):
        self.recipes.extend(iterable)

    def pop(self, index=-1):
        # Remove and return a recipe at the specified index.
        return self.recipes.pop(index)

    def __getitem__(self, index):
        # Access a recipe by index.
        return self.recipes[index]

    def __setitem__(self, index, value):
        # Set a recipe at a specific index.
        self.recipes[index] = value

    def __delitem__(self, index):
        # Delete a recipe at a specific index.
        del self.recipes[index]

    def __contains__(self, recipe):
        # Allows for checking if an item is made by a given recipe using in.
        for contained_recipe in self.recipes:
            if contained_recipe.name == recipe.name:
                return True

        else: return False

    def __len__(self):
        # Get the number of recipes.
        return len(self.recipes)

    def __iter__(self):
        # Iterate over the recipes.
        return iter(self.recipes)

    def __repr__(self):
        return f"Item(name={self.name}, recipes={self.recipes})"

    def __str__(self):
        return f"{self.name}"

    def __eq__(self, other):
        return self.name == other


#problems: Compacted Coal, Encased Uranium Cell,

with open('recipes.json', 'r') as file:
    for _recipe in json.load(file):
        new_recipe = Recipe(*_recipe.values())
        for __item in new_recipe.items:
            Item(__item, new_recipe)

for __item in Item.all_items:
    __item.order_recipes()

"""print(vars(Recipe.all_recipes[28]))
print(len(Recipe.all_recipes))
print(list(vars(i) for i in Recipe.all_recipes[28].recipes_for_inputs()))

print(vars(Item.all_items[1]))
print(len(Item.all_items))
print(list(vars(i) for i in Item.all_items[1].recipes))"""

print(Item.all_items[0].get_full_tree())
