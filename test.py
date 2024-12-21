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
        self.scene = QGraphicsScene()

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