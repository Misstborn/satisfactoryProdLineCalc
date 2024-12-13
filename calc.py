import json

EXTRACTED_ITEMS = ('Iron Ore', 'Copper Ore', 'Caterium Ore', 'Limestone', 'Coal', 'Raw', 'Sulfur', 'Bauxite', 'Uranium'
                    , 'SAM', 'Water', 'Crude Oil', 'Nitrogen Gas', 'FICSMAS Gift', 'Mycelia', 'Beryl Nut', 'Paleberry',
                    'Bacon Agaric', 'Blue Power Slug', 'Yellow Power Slug', 'Purple Power Slug', 'Hog Remains',
                    'Hatcher Remains', 'Spitter Remains', 'Stinger Remains', 'Wood', 'Leaves')

class Recipe:
    def __init__(self, name, alt, ficsmas, building, ingredients, outputs):
        self.name = name
        self.building = building
        self.alt = alt
        self.ficsmas = ficsmas
        self.ingredients = ingredients
        self.items = [item['Item'] for item in outputs]
        self.ipm = [item['Per-minute'] for item in outputs]
        self.clockspeed = 1

    def __contains__(self, item):
        if not isinstance(item, str):
            raise TypeError("Item is not a string")

        return item in self.items

    def calc_clockspeed(self):
        pass

    def recipes_for_inputs(self):
        _ingredient_recipes = []
        for _ingredient in self.ingredients:
            if any(extracted_item in _ingredient for extracted_item in EXTRACTED_ITEMS):
                continue

            for _item in recipes:
                if _ingredient['Item'] in _item and not _item.alt:
                    _ingredient_recipes.append(_item)

        return _ingredient_recipes

#problems: Compacted Coal, Encased Uranium Cell,
recipes = []
with open('recipes.json', 'r') as file:
    for _recipe in json.load(file):
        recipes.append(Recipe(*_recipe.values()))


print(vars(recipes[28]))
print(len(recipes))
print(list(vars(i) for i in recipes[28].recipes_for_inputs()))
