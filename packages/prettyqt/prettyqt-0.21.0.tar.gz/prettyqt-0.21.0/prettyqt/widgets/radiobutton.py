# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets
import qtawesome as qta


class RadioButton(QtWidgets.QRadioButton):

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def set_icon(self, icon):
        if isinstance(icon, str):
            icon = qta.icon(icon)
        if icon:
            self.setIcon(icon)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = RadioButton("This is a test")
    widget.set_icon("mdi.timer")
    widget.show()
    app.exec_()
