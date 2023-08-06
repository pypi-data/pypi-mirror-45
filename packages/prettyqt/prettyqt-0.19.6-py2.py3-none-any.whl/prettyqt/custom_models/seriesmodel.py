# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore

from prettyqt import core


class SeriesModel(core.AbstractTableModel):
    HEADER = ["Name"]
    DATA_ROLE = QtCore.Qt.UserRole
    NAME_ROLE = QtCore.Qt.UserRole + 2

    def __init__(self, chart=None, parent=None):
        super().__init__(parent=parent)
        self.chart = chart
        self.len = None
        self.set_length()

    def set_length(self):
        self.len = len(set(s.name() for s in self.chart().series()))

    def rowCount(self, parent=None):
        return self.len

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return False
        if role in [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole, self.NAME_ROLE]:
            return self.chart().series()[index.row()].name()
        elif role == self.DATA_ROLE:
            return self.chart().series()[index.row()]
        elif role == QtCore.Qt.DecorationRole:
            return self.chart().series()[index.row()].color()
        elif role == QtCore.Qt.CheckStateRole:
            return self.chart().series()[index.row()].isVisible()
        return None

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        if role == QtCore.Qt.EditRole:
            series = index.data(self.DATA_ROLE)
            old_name = series.name()
            series.setName(value)
            self.modify_all_with_name(series, old_name)
            self.dataChanged.emit(index, index)
            return True
        elif role == QtCore.Qt.CheckStateRole:
            s = index.data(self.DATA_ROLE)
            self.set_vis_for_series_with_names([s.name()], not s.isVisible())
            self.dataChanged.emit(index, index)
            return True

    def flags(self, index):
        return (super().flags(index) |
                QtCore.Qt.ItemNeverHasChildren |
                QtCore.Qt.ItemIsEditable |
                QtCore.Qt.ItemIsUserCheckable)

    def remove_series(self, series):
        with self.remove_rows():
            self.chart().removeSeries(series)
            self.set_length()

    def remove_series_with_names(self, names):
        with self.remove_rows():
            for s in reversed(self.chart().series()):
                if s.name() in names:
                    self.chart().removeSeries(s)
            self.set_length()

    def set_vis_for_series_with_names(self, names, visible):
        with self.change_layout():
            for s in reversed(self.chart().series()):
                if s.name() in names:
                    s.setVisible(visible)

    def modify_all_with_name(self, series, name):
        for i, s in enumerate(self.chart().series()):
            if name == s.name():
                pen = s.pen()
                pen.setColor(series.color())
                pen.setWidthF(series.pen().widthF())
                s.setPen(pen)
                s.setName(series.name())
        self.set_length()
