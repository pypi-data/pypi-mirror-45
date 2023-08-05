# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import pathlib
import sys

from prettyqt import widgets


class ImageViewer(widgets.Widget):

    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.title = title
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        path = pathlib.Path("decisiontree.png")
        self.image = widgets.Label.image_from_path(path, parent=self)
        self.show()


if __name__ == "__main__":
    app = widgets.Application(sys.argv)
    ex = ImageViewer()
    sys.exit(app.exec_())
