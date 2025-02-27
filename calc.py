import json
from copy import copy

from test import max_depth

EXTRACTED_ITEMS = ('Iron Ore', 'Copper Ore', 'Caterium Ore', 'Limestone', 'Coal', 'Raw', 'Sulfur', 'Bauxite', 'Uranium'
                    , 'SAM', 'Water', 'Crude Oil', 'Nitrogen Gas', 'FICSMAS Gift', 'Mycelia', 'Beryl Nut', 'Paleberry',
                    'Bacon Agaric', 'Blue Power Slug', 'Yellow Power Slug', 'Purple Power Slug', 'Hog Remains',
                    'Hatcher Remains', 'Spitter Remains', 'Stinger Remains', 'Wood', 'Leaves')
NODE_X_OFFSET = 50

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
        # self.node_index = 1
        # self.depth = 0

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


class RecipeTree:
    def __init__(self, item):
        self.tree = self.get_tree(item)
        self.max_depth = 0
        self.layout = []

    def get_tree(self, head_item):
        # depth of node, current index being evaluated, and unique node number
        curr_index = 0
        node_number = 1
        tree = {"Node0Children": [TreeNode(copy(head_item), 0, node_number)]}
        while len(tree) >= curr_index:
            for __node in tree[f'Node{curr_index}Children']:
                tree[f'Node{curr_index}Children'] = [TreeNode(copy(ingredient), __node.depth + 1,
                                                              node_number := node_number + 1, parent=__node)
                                                     for ingredient in __node.get_ingredients(0)]
                curr_index += 1
                self.max_depth = max(self.max_depth, __node.depth + 1)

        return tree


    def get_layout(self, node_width, node_height):
        node_size = (node_width, node_height)
        # Create list of y offsets.
        node_y_offsets = [0 for _ in range(self.max_depth)]
        curr_children = None
        curr_depth = self.max_depth
        depth_index = self.max_depth - curr_depth

        for i in range(len(self.tree)):
            if self.tree[f'Node{i}Children'][0].depth == self.max_depth:
                curr_children = self.tree.pop(f'Node{i}Children')
                self.layout.append([])
                break


        for child in curr_children:
            setattr(child, 'size', node_size)
            setattr(child, 'pos', (depth_index * (node_width + NODE_X_OFFSET), node_y_offsets[depth_index]))
            self.layout[0].append(child)

        return


class TreeNode:
    def __init__(self, item, depth, index, pos=(0,0), size=(0,0), parent=None):
        self.item = item
        self.depth = depth
        self.index = index
        self.parent = parent
        self.pos = pos
        self.size = size

    def get_ingredients(self, recipe_num):
        return self.item.recipes[recipe_num].get_ingredients()

    def get_recipes(self):
        return self.item.recipes


"""
with open('recipes.json', 'r') as file:
    for _recipe in json.load(file):
        new_recipe = Recipe(*_recipe.values())
        for __item in new_recipe.items:
            Item(__item, new_recipe)

for __item in Item.all_items:
    __item.order_recipes()"""

"""print(vars(Recipe.all_recipes[28]))
print(len(Recipe.all_recipes))
print(list(vars(i) for i in Recipe.all_recipes[28].recipes_for_inputs()))

print(vars(Item.all_items[1]))
print(len(Item.all_items))
print(list(vars(i) for i in Item.all_items[1].recipes))"""

# print(Item.all_items[0].get_full_tree())
