# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import qtawesome as qta
from qtpy import QtCore, QtWidgets

from prettyqt import widgets


class ProgressDialog(QtWidgets.QProgressDialog):
    """Progress dialog

    wrapper for QtWidgets.QProgressDialog
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        progress_bar = widgets.ProgressBar()
        progress_bar.setRange(0, 0)
        progress_bar.setTextVisible(False)
        self.setBar(progress_bar)

        self.set_icon("mdi.timer-sand-empty")
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Window)
        self.set_titlebar_buttons()
        self.setCancelButton(None)
        self.cancel()

    def set_icon(self, icon):
        if icon:
            if isinstance(icon, str):
                icon = qta.icon(icon, color="lightgray")
            self.setWindowIcon(icon)

    def open(self, message=None):
        if not message:
            message = "Processing..."
        self.setLabelText(message)
        self.show()

    def set_titlebar_buttons(self,
                             minimize: bool = False,
                             maximize: bool = False,
                             close: bool = False):
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, minimize)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, maximize)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, close)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = ProgressDialog()
    widget.show()
    widget.exec_()
