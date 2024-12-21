import requests
from bs4 import BeautifulSoup
import json


def to_json(name, alternate, building, ingredients, outputs):

    # Catch there being no ingredients
    try:
        formatted_ingredients = [{"Item": item_name, "Per-minute": float(quantity.replace(',', ''))} for
                                 item_name, quantity in ingredients]
        # print(formatted_ingredients)
    except TypeError:
        formatted_ingredients = None

    # Catch there being no products
    try:
        formatted_outputs = [{"Item": item_name, "Per-minute": float(quantity.replace(',', ''))} for
                             item_name, quantity in outputs]
    except TypeError:
        formatted_outputs = None

    formatted = {"Name": name,
                 "Alternate": True if alternate == 'Alternate' else False,
                 'FICSMAS': True if alternate == 'FICSMAS' else False,
                 "Building": building,
                 "Ingredients": formatted_ingredients,
                 "Outputs": formatted_outputs}

    return formatted


# Name site and get soup
site = 'https://satisfactory.wiki.gg/wiki/Recipes'
page = requests.get(site)
soup = BeautifulSoup(page.content, 'html.parser')
outputData = []

# The table on the wiki that contains all the recipes
recipeTable = soup.find('div', {'class': 'mw-parser-output'}).find('table').find('tbody').find_all('tr')

# Position 0 contains null data, skip
for recipe in recipeTable[1:]:
    # Name of recipe (not necessarily what is produced)
    recipeName = recipe.find('td').text.removesuffix('Alternate').removesuffix('FICSMAS')
    recipeComponents = [None]  # Components used in recipe, some recipes don't use any so defaults to None
    recipeOutputs = [None]  # Outputs made by recipe, set to None for consistency
    recipeBuilding = recipe.find('div', {'class': 'recipe-building'}).find('a').get('title')

    # If the recipe title has a "badge," then it is either an alt or FICSMAS recipe.
    if badge := recipe.find('td').find('span', {'class': 'recipe-badge'}):
        special = badge.text
    else:
        special = False

    # All subtags in a recipe (name, items per minute, produced in, etc)
    for tag in recipe.find_all('td'):

        # If the tag has the 'recipe-items' class (and assign those items to itemSet)
        if itemSet := tag.find('div', {'class': 'recipe-items'}):
            itemSetNames = []

            # Try except to catch there not being any inputs/outputs
            try:
                # Temp variable to reduce function calls, finds specific text span
                isSupply = ('supplied' in itemSet.find('div', {'class': 'recipe-item'})
                            .find('span', {'class': 'item-minute'}).get('title'))
                isWithdrawn = ('withdrawn' in itemSet.find('div', {'class': 'recipe-item'})
                            .find('span', {'class': 'item-minute'}).get('title'))
            except AttributeError:
                isSupply = None

            else:
                # For each item in the set, get the name
                for item in itemSet.find_all('div', {'class': 'recipe-item'}):
                    itemSetNames.append((item.find('a').get('title'), item.find('span', {'class': 'item-minute'}).text[:-6]))

                # Put list of item names into recipeComponents/Outputs depending on which one the text specifies
                if isSupply:
                    recipeComponents = itemSetNames
                elif isWithdrawn:
                    recipeOutputs = itemSetNames

    # print(f'Name: {recipeName}, Components: {recipeComponents}, Outputs: {recipeOutputs}, Produced in: '
    #       f'{recipeBuilding}')
    print(recipeComponents)

    outputData.append(to_json(recipeName, special, recipeBuilding, recipeComponents, recipeOutputs))


# Open file to output recipe data to
with (open('recipes.json', 'w+') as jsonfile):
    json.dump(outputData, jsonfile, indent=4)
