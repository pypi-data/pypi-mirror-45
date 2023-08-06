# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore

from prettyqt import core


class PackageModel(core.AbstractTableModel):
    HEADER = ["Name"]
    DATA_ROLE = QtCore.Qt.UserRole
    NAME_ROLE = QtCore.Qt.UserRole + 2

    def __init__(self, packages=None, parent=None):
        super().__init__(parent=parent)
        self.items = packages

    def rowCount(self, parent=None):
        return len(self.items)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return False
        if role in [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole, self.NAME_ROLE]:
            return self.items[index.row()].description
        return None

    def flags(self, index):
        return (super().flags(index) |
                QtCore.Qt.ItemNeverHasChildren |
                QtCore.Qt.ItemIsEditable |
                QtCore.Qt.ItemIsUserCheckable)


if __name__ == "__main__":
    import pkgutil
    import importlib
    import pkginfo
    from prettyqt import widgets
    app = widgets.Application.create_default_app()
    packages = list()
    for finder, name, ispkg in pkgutil.iter_modules():
        if name.startswith('datacook_'):
            importlib.import_module(name)
            packages.append(pkginfo.Installed(name))
    widget = widgets.TableView()
    model = PackageModel(packages)
    widget.setModel(model)
    widget.show()
    app.exec_()
