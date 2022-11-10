# Parachute Gore DXF Generator
# Copyright © 2022 Eabha Abramson
# main.py - Runs the main application for the program

from config import *
from functions import *
from gui import *

def main() -> None:
    app = QApplication(sys.argv)    # Create the application

    window = MainWindow()   # Create the window for the application
    window.setWindowTitle("Parachute Gore DXF Generator")   # Title

    window.show()   # Show window
    app.exec_() # Run app

main()  # Run the program
