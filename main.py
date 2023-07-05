import sys
from PyQt5.QtWidgets import QApplication

from pages.login import LoginPage

def main():
    app = QApplication(sys.argv)
    ex = LoginPage()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()