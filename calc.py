import json

EXTRACTED_ITEMS = ('Iron Ore', 'Copper Ore', 'Caterium Ore', 'Limestone', 'Coal', 'Raw', 'Sulfur', 'Bauxite', 'Uranium'
                    , 'SAM', 'Water', 'Crude Oil', 'Nitrogen Gas', 'FICSMAS Gift', 'Mycelia', 'Beryl Nut', 'Paleberry',
                    'Bacon Agaric', 'Blue Power Slug', 'Yellow Power Slug', 'Purple Power Slug', 'Hog Remains',
                    'Hatcher Remains', 'Spitter Remains', 'Stinger Remains', 'Wood', 'Leaves')

class Recipe:
    all_recipes = []

    def __init__(self, name, alt, ficsmas, building, ingredients, outputs):
        self.name = name
        self.building = building
        self.alt = alt
        self.ficsmas = ficsmas
        self.ingredients = ingredients
        self.items = [item['Item'] for item in outputs]
        self.ipm = [item['Per-minute'] for item in outputs]
        self.clockspeed = 1
        self.is_base = True if self.ingredients is None else False

        Recipe.all_recipes.append(self)

    def __contains__(self, _item):
        if not isinstance(_item, str):
            raise TypeError("Item is not a string")

        return _item in self.items

    def calc_clockspeed(self):
        pass

    def recipes_for_inputs(self):
        if not self.is_base:
            _ingredient_recipes = []
            for _ingredient in self.ingredients:
                if any(extracted_item in _ingredient for extracted_item in EXTRACTED_ITEMS):
                    continue

                for _item in Recipe.all_recipes:
                    if _ingredient['Item'] in _item and not _item.alt:
                        _ingredient_recipes.append(_item)

            return _ingredient_recipes
        else:
            raise TypeError("Item is a base with no prior ingredients.")


class Item:

    all_items = []

    def __init__(self, name, recipe, add_to_list=True):
        self.name = name
        self.recipes = [recipe]

        if add_to_list:
            self.__add_to_list()

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
        for item in new_recipe.items:
            Item(item, new_recipe)

print(vars(Recipe.all_recipes[28]))
print(len(Recipe.all_recipes))
print(list(vars(i) for i in Recipe.all_recipes[28].recipes_for_inputs()))

print(vars(Item.all_items[1]))
print(len(Item.all_items))
print(list(vars(i) for i in Item.all_items[1].recipes))
