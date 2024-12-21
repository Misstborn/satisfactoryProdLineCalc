import sys

from PySide2.QtWidgets import (QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem,
                               QGraphicsTextItem, QGraphicsLineItem, QGraphicsRectItem, QGraphicsPathItem, QComboBox,
                               QGraphicsProxyWidget)
from PySide2.QtGui import QPen, QBrush, QColor, QPainterPath, QFont, QPainter
from PySide2.QtCore import Qt, QRectF, QPointF, QLineF
import calc
import json

# Reads recipes.json to load each recipe into a list of Items.
with open('recipes.json', 'r') as file:
    for _recipe in json.load(file):
        new_recipe = calc.Recipe(*_recipe.values())
        for item in new_recipe.items:
            calc.Item(item, new_recipe)

for item in calc.Item.all_items:
    item.order_recipes()

print(vars(calc.Recipe.all_recipes[0].get_full_tree()))
print(calc.Item.all_items[0].recipes[0].get_ingredients())


# A given Node represents one recipe, with a building, inputs, outputs, a clock speed, and the option to change the used
# recipe.
class Node(QGraphicsRectItem):
    def __init__(self, x, y, _item, width=275, height=125):
        # Initialization
        super().__init__(0, 0, width, height)  # Create a rectangular node
        self.item = _item
        self.current_recipe = self.item.recipes[0]
        # print(self.item)
        self.setPos(x, y) # Set location
        self.setBrush(QBrush(QColor(100, 150, 250)))  # Fill color
        self.setPen(QPen(Qt.black, 2))  # Border color

        self.input_labels = [] # Labels for recipe components
        self.output_labels = [] # Labels for recipe products

        self.center = QPointF(self.pos().x() + self.boundingRect().width() / 2,  # Center point of Node
                              self.pos().y() + self.boundingRect().height() / 2)
        self.local_center = QPointF(width / 2, height / 2)  # Local center point of Node for children
        self.center_right_wall = QPointF(self.pos().x() + self.boundingRect().width(), self.center.y())  # Midpoint of right wall
        self.center_left_wall = QPointF(self.pos().x(), self.center.y()) #  Midpoint of left well

        self.recipe_combo = QComboBox()  # Combo (multiple choice) box to select the used recipe.

        # For each recipe used to make the item, add to combo box
        for __recipe in self.item:
            self.recipe_combo.addItem(__recipe.name)
        self.recipe_combo.currentTextChanged.connect(self.change_recipe)  # Connect the changing of the selected recipe to the change_recipe method.
        self.change_recipe(self.current_recipe.name)  # Run change_recipe to show the labels for the initial recipe.

        self.recipe_proxy_widget = QGraphicsProxyWidget(self)  # Proxy to place combo box inside Node.
        self.recipe_proxy_widget.setWidget(self.recipe_combo)  # Assign proxy the combo box widget.
        self.recipe_proxy_widget.setPos(self.local_center.x() - (self.recipe_proxy_widget.boundingRect().width() / 2), 2)  # Set position of combo box to top center.
        self.recipe_proxy_widget.setZValue(1)  # Place combo box so it displays over other objects. (Displays the dropdown over item labels, namely.)


    # Method to create and place a label for the input or output item, with correct flow rate.
    def add_item(self, _is_input, __item, __rate):
        # Create label with specific font and color.
        item_label = QGraphicsTextItem(f'{__rate} {__item.name}/m', self)
        item_label.setDefaultTextColor(Qt.white)
        item_label.setFont(QFont('Arial', 7))

        # If item is a component.
        if _is_input:
            self.input_labels.append(item_label)  # Add to list of components.
            label_list = self.input_labels  # Set local label_list to the component list.

        # If item is a product.
        else:
            # print(f'Item: {__item.name}, {item_label.boundingRect()}')
            self.output_labels.append(item_label)  # Add to list of products.
            label_list = self.output_labels  # Set local label_list to the product list.

        # Get how far the label should be placed from the center in order to have all the labels centered around the centerline of Node.
        center_offset = ((item_label.boundingRect().height() / 2) +
                         ((len(label_list) - 1) / 2) * item_label.boundingRect().height())
        if len(label_list) % 2 == 0:
            center_offset = (item_label.boundingRect().height() + 1) * (len(label_list) / 2)

        # For each label in whichever list is being used, place it then subtract its size (along with padding) from the offset.
        for _item_label in label_list:
            x_pos = -2 if _is_input else self.boundingRect().width() - _item_label.boundingRect().width() - 1  # Set x position of label.
            _item_label.setPos(x_pos, self.local_center.y() - center_offset)
            center_offset -= _item_label.boundingRect().height() + 2

    # Method to change the currently used recipe.
    def change_recipe(self, _recipe_name):
        # Remove all labels from visibility, and then delete them.
        for label in self.input_labels + self.output_labels:
            label.scene().removeItem(label)
            del label

        # Label lists are now full of null pointers, set them to empty.
        self.input_labels = []
        self.output_labels = []

        # Find the correct Recipe object based on the recipe name.
        for recipe in self.item:
            if recipe.name == _recipe_name:
                self.current_recipe = recipe

        print(vars(self.current_recipe))
        # Populate labels.
        for __ingredient in self.current_recipe.ingredients:
            _item_object = calc.Item.all_items[calc.Item.all_items.index(__ingredient['Item'])]
            self.add_item(True, _item_object, __ingredient['Per-minute'])

        for __output in self.current_recipe.outputs:
            _item_object = calc.Item.all_items[calc.Item.all_items.index(__output['Item'])]
            self.add_item(False, _item_object, __output['Per-minute'])


# Main visible window that will contain the nodes.
class MainWindow(QMainWindow):
    def __init__(self):
        # Initialization
        super().__init__()
        self.setWindowTitle("Satisfactory Production Layout Manager")
        self.setGeometry(100, 100, 800, 600)

        # Set up the scene and view
        self.scene = QGraphicsScene()
        self.flowchart = FlowchartView(self.scene, self)
        self.setCentralWidget(self.flowchart)

        # Create nodes
        node1 = Node(0, 200, calc.Item.all_items[1])
        node2 = Node(300, 200, calc.Item.all_items[1])
        node3 = Node(600, 100, calc.Item.all_items[2])

        # Add nodes to the scene
        self.scene.addItem(node1)
        self.scene.addItem(node2)
        self.scene.addItem(node3)

        # Connect nodes with lines
        self.flowchart.add_path_connection(node1.center_right_wall, node2.center_left_wall)
        self.flowchart.add_path_connection(node2.center_right_wall, node3.center_left_wall)


class FlowchartView(QGraphicsView):
    def __init__(self, __graphics_scene, __parent):
        super().__init__(__graphics_scene, __parent)
        self.scene = __graphics_scene
        self.setRenderHint(QPainter.Antialiasing)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scene.setSceneRect(-250, -250, 2000, 2000)

        # Translation variables
        self.scale_factor = 1.0
        self.max_zoom = 5.0
        self.min_zoom = 0.2
        self._is_panning = False
        self._pan_start = QPointF()


    def add_path_connection(self, _start, _end):
        """Create a line with smooth Bézier curves for corners between two points."""
        # Add path object
        _path = QPainterPath()

        # Determine which axis difference the curve radius should be based on.
        if abs(_start.y() - _end.y()) <= _end.x() - _end.x():
            curve_radius = (_start.y() - _end.y()) / 2.75  # Hard coded appearance quality number

        else:
            curve_radius = (_end.x() - _start.x()) / 2.75

        print(curve_radius)

        # Start is midpoint of the right side of node 1, end is midpoint of left side of node 2
        # Midpoint between nodes
        x_midpoint = ((_end.x() - _start.x()) / 2) + _start.x()
        # Control points offset by curve radius from midline
        control_point1 = QPointF(x_midpoint + curve_radius, _start.y())
        control_point2 = QPointF(x_midpoint - curve_radius, _end.y())
        control_point3 = QPointF(x_midpoint - curve_radius, _start.y())
        control_point4 = QPointF(x_midpoint + curve_radius, _end.y())

        # Set path location
        _path.moveTo(_start)

        # Node1 beneath node2
        if _start.y() >= _end.y():
            _path.lineTo(control_point3)
            _path.cubicTo(control_point1, control_point2, control_point4)
            _path.lineTo(_end)

        # Node1 above node2
        else:
            _path.lineTo(control_point1)
            _path.cubicTo(control_point3, control_point4, control_point2)
            _path.lineTo(_end)

        # Add the path to the scene
        path_item = QGraphicsPathItem(_path)
        path_item.setPen(QPen(Qt.black, 2))
        self.scene.addItem(path_item)

    def add_point_to_scene(self, point, color):
        # Visualize a point as a small circle
        radius = 5
        ellipse = QGraphicsEllipseItem(point.x() - radius, point.y() - radius, 2 * radius, 2 * radius)
        ellipse.setBrush(QBrush(color))
        ellipse.setPen(QPen(Qt.black))
        self.scene.addItem(ellipse)

    def wheelEvent(self, event):
        """Zoom in or out based on the mouse wheel movement."""
        zoom_in_factor = 1.1
        zoom_out_factor = 1 / zoom_in_factor

        # Determine the zoom direction
        if event.angleDelta().y() > 0:  # Scroll up
            if self.scale_factor < self.max_zoom:
                self.scale(zoom_in_factor, zoom_in_factor)
                self.scale_factor *= zoom_in_factor
        else:  # Scroll down
            if self.scale_factor > self.min_zoom:
                self.scale(zoom_out_factor, zoom_out_factor)
                self.scale_factor *= zoom_out_factor

    def mousePressEvent(self, event):
        """Start panning when the middle or left mouse button is pressed."""
        if event.button() == Qt.MiddleButton:
            self._is_panning = True
            self.viewport().setCursor(Qt.ClosedHandCursor)  # Change cursor to indicate panning.
            self._pan_start = event.pos()  # Record the starting position.

        # If other type of mousepress, super mousePressEvent
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handle panning when the mouse moves."""
        if self._is_panning:
            # Calculate the distance the mouse has moved.
            delta = self._pan_start - event.pos()
            self._pan_start = event.pos()  # Update the last position.

            # Adjust the scroll position of the view to reflect movement.
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() + delta.x()
            )
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() + delta.y()
            )

        # If not panning, super mousePressEvent
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Stop panning when the mouse button is released."""
        if event.button() == Qt.MiddleButton:
            self._is_panning = False
            self.viewport().setCursor(Qt.ArrowCursor)  # Restore the default cursor

        # If other type of mouserelease, super mouseReleaseEvent
        else:
            super().mouseReleaseEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
