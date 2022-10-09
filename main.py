# Run: C:\Users\D026557\AppData\Local\Programs\Python\Python39\python.exe main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from classes.MainWidget import MainWidget
from classes.MainWindowMenu import MainWindowMenu
from classes.Process import Process

# .:| TODO |:.
# - Adaptation of usage of rings to chains
#   + add configuration parameter to draw/hide such "markers"
#   + instead of "markers" use a tiny node-image, laying on the line
# - File Handling
#   + Delete (file) function 
#   + Picot-Positions for each figure
#   + Change handling of filenames => process such calls in a new method
#   + Name of current filename in title
#   + Add filter in file open/save dialogs (txt)
#   + Change the way how to deal with picot coordinates (separate file for new figure extension
#     of program users, too)
# - SVG Panel
#   + Paper size (xmax, ymax) / A4/A3/A2/A1/A0/individual size from User
#   + Numbers and names of figures written
#   + Individual text everywhere
#   + Graphical elements and Text created by drag&drop via icons in toolbox-bar
#   + Error with zooming with regards to papersize - not visible with huge papersize
#   + Parameter for Output of SVG, e.g.:
#     . stroke width
#     . "Name" or "Number" of a figure
#     . Number of nodes between picots/edges as text
#     . Text for Instruction per Round/Figur as written Text
# - Text Panel
#   + Zoom in Text Pane (larger font size), e.g. when using Ctrl+/Ctrl- depending on active pane
#   + Text in formatted HTML instead of plain text
#   + HTML formatting in config file (font size, font color, font family)
# - Hints for Output for Publication in e.g. Internet


class Main(QMainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        # ----- Panel und Layout ---------------------------------------------------------------- #
        self.widget = MainWidget(self)
        self.setCentralWidget(self.widget) 

        # ----- Menu and all Actions ------------------------------------------------------------ #
        self.menu = MainWindowMenu(self)
        self.setMenuBar(self.menu)
        self.setWindowTitle('TADES (Tatting Design Studio)')
        self.setGeometry(50, 50, 1500, 1000)

        # ----- "Rest" -------------------------------------------------------------------------- #
        self.process = Process(self)
        
    # ON ACTION #
    def onNew(self):
        self.widget.onNew()
    def onOpen(self):
        self.widget.onOpen()
    def onDelete(self):
        pass
    def onSave(self):
        self.widget.onSave()
    def onSaveAs(self):
        self.widget.onSaveAs()
    def onExit(self):
        self.process.onExit()
    def onRedraw(self):
        self.widget.onRedraw()
    def onZoomIn(self):
        self.widget.onZoomIn()
    def onZoomOut(self):
        self.widget.onZoomOut()
    def onGrid(self):
        self.process.onGrid()

def main():
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()