import sys
from PySide.QtCore import *
from PySide.QtGui import *

from connectionWindow import ConnectionWindow
from controller import Controller 

if __name__ == '__main__':
    controller = Controller()

    # Create the Qt Application
    app = QApplication(sys.argv)

    # Create and show the form
    form = ConnectionWindow(controller)
    form.show()

    # Run the main Qt loop
    sys.exit(app.exec_())
