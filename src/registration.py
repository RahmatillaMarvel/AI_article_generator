from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QCheckBox
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator, QFont
import sqlite3
from pathlib import Path
import sys
import subprocess

class RegistrationPage():
    def __init__(self, window) -> None:
        super().__init__()
        self.window = window
        self.logged = False
        self.init_ui()

    def init_ui(self) -> None:
        # Registration

        # Title
        self.title_label = QLabel("Registration", self.window)
        self.title_label.setFont(QFont("Times New Roman", 25, 99))
        self.title_label.setGeometry(400, 100, 200, 50)

        # Login label
        self.login_label = QLabel("Login: ", self.window)
        self.login_label.setFont(QFont("Times New Roman", 20))
        self.login_label.setGeometry(250, 250, 200,50)
        
        # Login input
        self.login_input = QLineEdit(self.window)
        self.login_input.setFont(QFont("Times New Roman", 20))
        self.login_input.setPlaceholderText('Make new unique login')
        self.login_input.setGeometry(400, 250, 400,40)

        # Password label
        self.password_label = QLabel("Password: ", self.window)
        self.password_label.setFont(QFont("Times New Roman", 20))
        self.password_label.setGeometry(250, 350, 200,50)
        
        # Password input
        self.password_input = QLineEdit(self.window)
        self.password_input.setFont(QFont("Times New Roman", 20))
        self.password_input.setPlaceholderText('Make strong password')
        self.password_input.setGeometry(400, 350, 400,40)

        regex_password = QRegExp("[0-9A-Za-z]+")
        validator = QRegExpValidator(regex_password)
        self.password_input.setValidator(validator)
        self.password_input.setToolTip('Password can contian any numbers or English letters')
        
        regex_login = QRegExp("[0-9A-Za-z]+")
        validator = QRegExpValidator(regex_login)
        self.login_input.setValidator(validator)
        self.password_input.setToolTip('Login can contian any numbers or English letters and a!=A')

        # Checkbox 
        self.have_account = QCheckBox('Do you have an account? Switch to login',self.window)
        self.have_account.setFont(QFont("Times New Roman", 18))
        self.have_account.setGeometry(250, 450, 550,40)

        self.login_btn = QPushButton('Login', self.window)
        self.login_btn.setFont(QFont("Times New Roman", 20))
        self.login_btn.setGeometry(300, 550, 100,50)
        self.login_btn.setEnabled(False)

        self.register_btn = QPushButton('Register', self.window)
        self.register_btn.setFont(QFont("Times New Roman", 20))
        self.register_btn.setGeometry(600, 550, 100,50)


        # Switch (login->password inputs)
        self.login_input.returnPressed.connect(self.focus_password)

        self.have_account.stateChanged.connect(self.change_mode)
        self.register_btn.clicked.connect(self.register)
        self.login_btn.clicked.connect(self.login)

    def focus_password(self) -> None:
        self.password_input.setFocus()


    def change_mode(self, state):
        if state== Qt.Checked:
            self.register_btn.setEnabled(False)
            self.login_btn.setEnabled(True)
            self.login_input.setPlaceholderText('Enter your login')
            self.password_input.setPlaceholderText('Enter your password')
            self.have_account.setText('Do\'nt you have any account yet? Switch to registration')
            self.title_label.setText('Login')
        else:
            self.register_btn.setEnabled(True)
            self.login_btn.setEnabled(False)
            self.login_input.setPlaceholderText('Make new unique login')
            self.password_input.setPlaceholderText('Make strong password')
            self.have_account.setText('Do you have an account? Switch to login')
            self.title_label.setText('Registration')

        self.login_input.setText('')
        self.password_input.setText('')


        
    def register(self):
        db_file = Path('./data/users.db')
        login = self.login_input.text()
        password = self.password_input.text()
        if len(login)<3 or len(password)<5:            
            QMessageBox.warning(self.window, "Warning", "Login should be at least 3 characters long and password should be at least 5 characters long.")
            return

        open('./data/users.db', 'x') if not db_file.exists() else "" 
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    UNIQUE(username))''')

        cursor.execute("SELECT * FROM users WHERE username=?", (login,))
        existing_user = cursor.fetchone()

        if existing_user:
            QMessageBox.warning(self.window, "Warning", "This login already exists. Please choose another one.")
            conn.close()
            return
        
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (login, password))
        QMessageBox.information(self.window, "Success", "Registration successful. Please proceed to login.")
        self.have_account.setCheckState(2)

        conn.commit()
        conn.close()
        print(f"Database created successfully at: {db_file}")

    def login(self):
        db_file = Path('./data/users.db')
        login = self.login_input.text()
        password = self.password_input.text()

        if len(login)<3 or len(password)<5:            
            QMessageBox.warning(self.window, "Warning", "Login should be at least 3 characters long and password should be at least 5 characters long.")
            return

        open('./data/users.db', 'x') if not db_file.exists() else "" 
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()


        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (login, password))
        user = cursor.fetchone()

        if not user:
            QMessageBox.warning(self.window, "Error", "Invalid login or password.")
        else:
            QMessageBox.information(self.window, "Congratulation", "You're in")
            with open('data/in_login.txt', 'w') as file:
                file.write('1')
            self.window.close()
            subprocess.check_call([sys.executable, 'main.py'])

        conn.close()