# Run: C:\Users\D026557\AppData\Local\Programs\Python\Python39\python.exe main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from classes.MainWidget import MainWidget
from classes.MainWindowMenu import MainWindowMenu
from classes.Process import Process

# .:| TODO |:.
# - File Handling
#   + Delete (file) function 
#   + Change handling of filenames => process such calls in a new method
#   + Add filter in file open/save dialogs (txt)
# - SVG Panel
#   + Graphical elements and Text created by drag&drop via icons in toolbox-bar
#   + Parameter for Output of SVG: Number of nodes between picots/edges as text
#   + "reversed" chain
#   + Split code _add (MainWidget) into several methods
# - Text Panel
#   + Zoom in Text Pane (larger font size), e.g. when using Ctrl+/Ctrl- depending on active pane
#   + Text in formatted HTML instead of plain text
#   + HTML formatting in config file (font size, font color, font family)
#   + When clicking on text, show element colored or bold in drawing
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
        self.setGeometry(50, 50, 1250, 1250)

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
    def onGrid(self):
        self.process.onGrid()
    def onNodeCircle(self):
        self.process.onNodeCircle()
    def onImageFrame(self):
        self.process.onImageFrame()
    def onPaperSizeA4(self):
        self.process.onPaperSize('A4')
    def onPaperSizeA3(self):
        self.process.onPaperSize('A3')
    def onPaperSizeA2(self):
        self.process.onPaperSize('A2')
    def onPaperSizeA1(self):
        self.process.onPaperSize('A1')
    def onPaperSizeA0(self):
        self.process.onPaperSize('A0')

def main():
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()