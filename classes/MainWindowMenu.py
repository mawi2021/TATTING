# Sorces
#   https://iconarchive.com/show/oxygen-icons-by-oxygen-icons.org.1.html
from PyQt5.QtWidgets import QMenuBar, QAction
from PyQt5.QtGui import QIcon, QKeySequence

class MainWindowMenu(QMenuBar):

    def __init__(self, parent):
        super().__init__()

        # ----- F I L E ------------------------------------------------------------------------- #
        fileMenu = self.addMenu("File")

        self.newAction = QAction(QIcon("icons/newproject2.png"), "New", self)
        self.newAction.triggered.connect(parent.onNew)
        fileMenu.addAction(self.newAction)

        self.openAction = QAction(QIcon("icons/openproject2.png"), "Open", self)
        self.openAction.triggered.connect(parent.onOpen)
        self.openAction.setShortcut(QKeySequence("Ctrl+O"))
        fileMenu.addAction(self.openAction)

        self.deleteAction = QAction(QIcon("icons/trash2.png"), "Delete", self)
        self.deleteAction.triggered.connect(parent.onDelete)
        fileMenu.addAction(self.deleteAction)

        fileMenu.addSeparator()

        self.saveAction = QAction(QIcon("icons/disc2.png"), "Save", self)
        self.saveAction.triggered.connect(parent.onSave)
        self.saveAction.setShortcut(QKeySequence("Ctrl+S"))
        fileMenu.addAction(self.saveAction)

        self.saveasAction = QAction(QIcon("icons/discas2.png"), "Save as", self)
        self.saveasAction.triggered.connect(parent.onSaveAs)
        fileMenu.addAction(self.saveasAction)

        fileMenu.addSeparator()

        self.exitAction = QAction(QIcon("icons/exit2.png"), "Exit Program", self)
        self.exitAction.triggered.connect(parent.onExit)
        fileMenu.addAction(self.exitAction)        

        # ----- E D I T ------------------------------------------------------------------------- #
        editMenu = self.addMenu("Edit")

        self.redrawAction = QAction(QIcon("icons/redraw2.png"), "Redraw", self)
        self.redrawAction.triggered.connect(parent.onRedraw)
        self.redrawAction.setShortcut(QKeySequence("Ctrl+R"))
        editMenu.addAction(self.redrawAction)

        # ----- V I E W ------------------------------------------------------------------------- #
        viewMenu = self.addMenu("View")

        self.zoomInAction = QAction(QIcon("icons/zoom_in2.png"), "Zoom In", self)
        self.zoomInAction.triggered.connect(parent.onZoomIn)
        self.zoomInAction.setShortcut(QKeySequence("Ctrl++"))
        viewMenu.addAction(self.zoomInAction)

        self.zoomOutAction = QAction(QIcon("icons/zoom_out2.png"), "Zoom Out", self)
        self.zoomOutAction.triggered.connect(parent.onZoomOut)
        self.zoomOutAction.setShortcut(QKeySequence("Ctrl+-"))
        viewMenu.addAction(self.zoomOutAction)

        self.gridAction = QAction(QIcon("icons/..."), "Toggle Gridlines", self)
        self.gridAction.triggered.connect(parent.onGrid)
        self.gridAction.setShortcut(QKeySequence("Ctrl+G"))
        viewMenu.addAction(self.gridAction)

        self.nodeCircleAction = QAction(QIcon("icons/..."), "Toggle Dots for Nodes", self)
        self.nodeCircleAction.triggered.connect(parent.onNodeCircle)
        self.nodeCircleAction.setShortcut(QKeySequence("Ctrl+N"))
        viewMenu.addAction(self.nodeCircleAction)

        self.imageFrameAction = QAction(QIcon("icons/..."), "Toggle Frame of Images", self)
        self.imageFrameAction.triggered.connect(parent.onImageFrame)
        self.imageFrameAction.setShortcut(QKeySequence("Ctrl+F"))
        viewMenu.addAction(self.imageFrameAction)
