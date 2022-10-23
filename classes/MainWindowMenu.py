# Sorces
#   https://iconarchive.com/show/oxygen-icons-by-oxygen-icons.org.1.html
from PyQt5.QtWidgets import QMenuBar, QAction, QMenu
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

        # Paper Size: A4, A3, ...
        self.paperSizeMenu = QMenu('Paper Size', self)

        self.paperSizeA4Action = QAction(QIcon("icons/..."), "A4", self)
        self.paperSizeA4Action.triggered.connect(parent.onPaperSizeA4)
        self.paperSizeMenu.addAction(self.paperSizeA4Action)

        self.paperSizeA3Action = QAction(QIcon("icons/..."), "A3", self)
        self.paperSizeA3Action.triggered.connect(parent.onPaperSizeA3)
        self.paperSizeMenu.addAction(self.paperSizeA3Action)

        self.paperSizeA2Action = QAction(QIcon("icons/..."), "A2", self)
        self.paperSizeA2Action.triggered.connect(parent.onPaperSizeA2)
        self.paperSizeMenu.addAction(self.paperSizeA2Action)

        self.paperSizeA1Action = QAction(QIcon("icons/..."), "A1", self)
        self.paperSizeA1Action.triggered.connect(parent.onPaperSizeA1)
        self.paperSizeMenu.addAction(self.paperSizeA1Action)

        self.paperSizeA0Action = QAction(QIcon("icons/..."), "A0", self)
        self.paperSizeA0Action.triggered.connect(parent.onPaperSizeA0)
        self.paperSizeMenu.addAction(self.paperSizeA0Action)

        viewMenu.addMenu(self.paperSizeMenu)
