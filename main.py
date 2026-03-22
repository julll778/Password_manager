from PyQt6.QtWidgets import QApplication

from basicFunction import*

def main():
    app = QApplication([])
    window = PasswordManager()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()