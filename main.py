from config import *
from functions import *
from gui import *

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setWindowTitle("Parachute Gore DXF Generator")

    window.show()
    app.exec_()

main()
