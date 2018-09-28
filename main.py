from PyQt5.QtWidgets import QApplication
import sys
from DA_backend import Backend
from DA_GuiMainWin import Main

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    
    # Initialises object that handles all backend processing
    backend = Backend()
    
    # Builds main interface, and passes in the backend.
    main = Main(app, backend)
    
    sys.exit(app.exec_())