import json
import dearpygui.dearpygui as dpg
dpg.create_context()


class Recipe:
    def __init__(self, item, name, building, alt, ipm, ingredients):
        self.item = item
        self.name = name
        self.building = building
        self.alt = alt
        self.ipm = ipm
        self.ingredients = ingredients
        self.clockspeed = 1

    def calc_clockspeed(self):
        pass


"""with open('recipes.json', 'r') as jsonfile:
    for recipe in json.load(jsonfile):
        print(recipe)"""


with dpg.window(tag="Recipe Calculator", width=300, height=300):
    dpg.add_text("Hello, world")
    dpg.add_button(label="Save")
    dpg.add_input_text(label="string", default_value="Quick brown fox")
    dpg.add_slider_float(label="float", default_value=0.273, max_value=1)

dpg.create_viewport(title='Custom Title', width=600, height=200)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('Recipe Calculator', True)
dpg.start_dearpygui()
dpg.destroy_context()
