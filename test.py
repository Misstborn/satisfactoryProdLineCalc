import sys

from PySide2.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem, QGraphicsRectItem, QGraphicsPathItem
from PySide2.QtGui import QPen, QBrush, QColor, QPainterPath
from PySide2.QtCore import Qt, QRectF, QPointF

class Node(QGraphicsRectItem):
    def __init__(self, x, y, label="Node", width=60, height=60):
        super().__init__(-width/2, -height/2, width, height)  # Create a rectangular node
        self.setPos(x, y)
        self.setBrush(QBrush(QColor(100, 150, 250)))  # Fill color
        self.setPen(QPen(Qt.black, 2))  # Border color

        # Add a label to the node
        text = QGraphicsTextItem(label, self)
        text.setDefaultTextColor(Qt.white)
        text.setPos(-text.boundingRect().width() / 2, -text.boundingRect().height() / 2)  # Center label in node

class FlowchartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flowchart Example with PySide2")
        self.setGeometry(100, 100, 800, 600)

        # Set up the scene and view
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        # Create nodes
        node1 = Node(100, 200, "Start")
        node2 = Node(300, 200, "Process")
        node3 = Node(500, 100, "End")

        # Add nodes to the scene
        self.scene.addItem(node1)
        self.scene.addItem(node2)
        self.scene.addItem(node3)

        # Connect nodes with lines
        self.add_path_connection(node1, node2)
        self.add_path_connection(node2, node3)

    def add_path_connection(self, node1, node2):
        # Add path object
        _path = QPainterPath()
        curve_radius = (node1.pos().y() - node2.pos().y()) / 2.75  # Hard coded appearance quality number

        # Start is midpoint of the right side of node 1, end is midpoint of left side of node 2
        _start = QPointF(node1.pos().x() + node1.boundingRect().width() / 2, node1.pos().y())
        _end = QPointF(node2.pos().x() - node2.boundingRect().width() / 2, node2.pos().y())
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlowchartWindow()
    window.show()
    sys.exit(app.exec_())
