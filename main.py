import sys, os
import subprocess
    
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QStackedWidget

try:
    from src.registration import RegistrationPage
    from src.mainpage import MainPage
except ImportError:
    print(f"You're now in {os.getcwd()}")
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Packages installed successfully. Continuing...")
    try:
        from src.registration import RegistrationPage
        from src.mainpage import MainPage
    except ImportError:
        print("Failed to import required modules even after installing packages. Exiting.")
        sys.exit(1)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedSize(1300, 700)
        self.setWindowTitle('AI Article Generator')
        self.stacked_widget = QStackedWidget()
        self.is_login: bool = self.check_in_login()

        self.set_ui()
        
    def set_ui(self) -> None:
        
        if not self.is_login:
            self.reg_page = RegistrationPage(self)
            self.is_login = self.check_in_login()
        else:
            self.main_page = MainPage(self)


    def check_in_login(self) -> bool:
        try:
            with open('data/in_login.txt') as file:
                content: str = file.read()
                if not content.isdigit():
                    print("Why are you changed in_login.txt?")
                    sys.exit()
                
                return bool(int(content))
        except FileNotFoundError:
            print("Why you touched to data folder?")
            print(f"You're now in {os.getcwd()}")
            print('Run again we are fixed all of them for you')
            with open('data/in_login.txt', 'w') as file:
                file.write('0')
            sys.exit()
        except Exception as e:
            print(f'We encoured with {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())