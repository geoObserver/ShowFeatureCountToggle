# -*- coding: utf-8 -*-
# new
from qgis.PyQt.QtWidgets import QAction, QToolBar
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsLayerTreeGroup, QgsLayerTreeLayer
import os

class ShowFeatureCountToggle:
    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.toolbar = None
        self.plugin_dir = os.path.dirname(__file__)
        self.feature_counts_visible = False

    def initGui(self):
        # Toolbar suchen oder erstellen
        tb_name = "#geoObserverTools"
        for tb in self.iface.mainWindow().findChildren(QToolBar):
            if tb.objectName() == tb_name:
                self.toolbar = tb
                break
        if not self.toolbar:
            self.toolbar = QToolBar(tb_name, self.iface.mainWindow())
            self.toolbar.setObjectName(tb_name)
            #self.iface.addToolBar(self.toolbar)
            self.toolbar = self.iface.addToolBar("#geoObserver Tools")

        # Aktion erzeugen
        #icon_path = os.path.join(self.plugin_dir, "icon.svg")
        icon_path = os.path.join(self.plugin_dir, "logo.png")
        self.action = QAction(QIcon(icon_path), "Objektanzahlen ein/ausblenden", self.iface.mainWindow())
        self.action.setCheckable(True)
        self.action.triggered.connect(self.toggle_counts)

        # In Toolbar einfügen
        self.toolbar.addAction(self.action)

    def unload(self):
        if self.action and self.toolbar:
            self.toolbar.removeAction(self.action)
        if self.action:
            self.iface.removePluginMenu("Show Feature Count Toggle", self.action)

    def toggle_counts(self):
        root = self.iface.layerTreeView().layerTreeModel().rootGroup()
        self.feature_counts_visible = not self.feature_counts_visible
        self._set_counts_on_all(root, self.feature_counts_visible)
        self.action.setChecked(self.feature_counts_visible)

    def _set_counts_on_all(self, group, show):
        for child in group.children():
            if isinstance(child, QgsLayerTreeLayer):
                layer = child.layer()
                if layer and layer.type() == layer.VectorLayer:
                    child.setCustomProperty("showFeatureCount", show)
            elif isinstance(child, QgsLayerTreeGroup):
                self._set_counts_on_all(child, show)
