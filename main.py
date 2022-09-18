# Run: C:\Users\D026557\AppData\Local\Programs\Python\Python39\python.exe main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from classes.MainWidget import MainWidget
from classes.MainWindowMenu import MainWindowMenu
from classes.Process import Process

# TODO:
#   Picot-Positionen Koordinatenliste erstellen
#   Abfrage nach Dateiname statt statisch im Programm
#   Parameter zum Aussehen, bspw. 
#   - bei Ausgaben Farbe mitgeben
#   - bei Ausgaben Strichstärke mitgeben
#   - "Name" oder "Nummer" einer Figur mitgeben, die bei der Ausgabe in/nahe der Figur als Text ausgegeben wird
#   - Anzahl Knoten in Figur-Abschnitte als Zahl eintragen
#   Anpassung Bildgröße (xmax, ymax) entsprechend der ausgegebenen Objekte oder Eingabe der Länge/Breite durch den User
#   Kommentare im Code in Englisch
#   Grafische Oberfläche
#   Gesamtanleitung pro Runde/Figur ausgeben

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
        pass
    def onOpen(self):
        self.widget.onOpen()
    def onDelete(self):
        pass
    def onSave(self):
        self.widget.onSave()
    def onSaveAs(self):
        pass
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