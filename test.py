def add_item(self, is_input, _item):
    combo_box = QComboBox()
    combo_box.setFixedWidth(100)
    print(combo_box.view().sizeHintForColumn(0))
    # W combo_box.view().setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
    # print(_item)

    max_width = 0
    items_added = 0
    for recipe in _item:
        combo_box.addItem(recipe.name)
        item_width = combo_box.view().fontMetrics().horizontalAdvance(combo_box.itemText(items_added))
        max_width = max(max_width, item_width)
        items_added += 1

    combo_box.view().setMinimumWidth(max_width)
    proxy_widget_combo = QGraphicsProxyWidget(self)
    proxy_widget_combo.setWidget(combo_box)

    if is_input:
        zval = 4
        self.input_combos.append(proxy_widget_combo)
        center_offset = ((proxy_widget_combo.boundingRect().height() / 2) +
                         ((len(self.input_combos) - 1) / 2) * proxy_widget_combo.boundingRect().height())
        if len(self.input_combos) % 2 == 0:
            center_offset = (proxy_widget_combo.boundingRect().height() + 1) * (len(self.input_combos) / 2)

        for proxy_widget in self.input_combos:
            proxy_widget.setPos(2, self.local_center.y() - center_offset)
            proxy_widget.setZValue(zval)
            center_offset -= proxy_widget.boundingRect().height() + 2
            zval -= 1