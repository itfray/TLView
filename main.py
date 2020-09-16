import sys
from mainwindow import MainWindow
from PySide2.QtWidgets import QApplication


WIN_MIN_REL_W = 0.5     # Minimum relative value window's width
WIN_MIN_REL_H = 0.6     # Minimum relative value window's height


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    # get available values width and height
    geometry = app.desktop().availableGeometry(window)
    window.setMinimumSize(geometry.width() * WIN_MIN_REL_W,
                          geometry.height() * WIN_MIN_REL_H)
    window.show()
    sys.exit(app.exec_())