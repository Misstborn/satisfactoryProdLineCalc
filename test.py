import dearpygui.dearpygui as dpg

dpg.create_context()

# Callback to monitor changes
def connection_callback(sender, app_data):
    # Recreate default connection if it's removed
    if app_data['link_id'] == "default_connection" and app_data['deleted']:
        dpg.add_node_link("node1", "node2", parent="node_editor", id="default_connection")


# Initialize node editor with default nodes and connections
with dpg.window(label="Tutorial", width=400, height=400):
    # Add nodes and pins, e.g., Node 1, Pin A connected to Node 2, Pin B
    with dpg.node_editor(callback=connection_callback):
        with dpg.node(label='node1'):
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, label='node1', tag='node1'):
                dpg.add_text("Output Pin A")
        with dpg.node(label='node2'):
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, label='node2', tag='node2'):
                dpg.add_text("Input Pin B")

        # Create a connection
        dpg.add_node_link("node1", "node2", tag="default_connection")


# Initialize Dear PyGui
dpg.create_viewport(title='Custom Node Editor')
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
