from PyQt5.QtWidgets import QLabel, QTextEdit, QPushButton, QScrollArea, QTextBrowser
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QFont
from src.gamini_pro import generate_response
import markdown
from uuid import uuid4
from fpdf import FPDF

class MainPage:
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.logged = False
        self.init_ui()

    def init_ui(self):
        # Title
        self.title_label = QLabel("AI Article Generator", self.window)
        self.title_label.setFont(QFont("Times New Roman", 25, 99))
        self.title_label.setGeometry(350, 100, 500, 50)

        # Code Area
        self.code_area = QTextEdit(self.window)
        self.code_area.setPlaceholderText('Write your code')
        self.code_area.setFont(QFont("Times New Roman", 18))
        self.code_area.setGeometry(100, 200, 400, 400)

        # An Article Area
        self.article_scroll_area = QScrollArea(self.window)
        self.article_scroll_area.setGeometry(550, 200, 400, 400)
        self.article_scroll_area.setWidgetResizable(True)

        # Make an article
        self.submit_btn = QPushButton("Make an article", self.window)
        self.submit_btn.setFont(QFont("Times New Roman", 18))
        self.submit_btn.setGeometry(350, 625, 300, 50)
        self.submit_btn.clicked.connect(self.make_an_article)

        # Restore an article
        self.restore_label = QLabel("Restore an article by ID:", self.window)
        self.restore_label.setFont(QFont("Times New Roman", 18))
        self.restore_label.setGeometry(1000, 200, 250, 50)

        self.restore_area = QTextEdit(self.window)
        self.restore_area.setFont(QFont("Times New Roman", 18))
        self.restore_area.setGeometry(1000, 300, 200, 50)

        self.restore_btn = QPushButton("Restore", self.window)
        self.restore_btn.setFont(QFont("Times New Roman", 18))
        self.restore_btn.setGeometry(1000, 450, 200, 50)
        self.restore_btn.clicked.connect(self.restore_an_article)

        # Save as PDF button
        self.save_pdf_btn = QPushButton("Save as PDF file", self.window)
        self.save_pdf_btn.setFont(QFont("Times New Roman", 18))
        self.save_pdf_btn.setGeometry(750, 625, 300, 50)
        self.save_pdf_btn.clicked.connect(self.save_as_pdf)

    def make_an_article(self):
        self.article_id = uuid4()
        self.request = self.code_area.toPlainText()
        self.response = generate_response(self.request)

        self.article_scroll_area.takeWidget()

        self.article_text = QTextBrowser()
        self.article_text.setOpenExternalLinks(True)
        self.article_text.setHtml(markdown.markdown(f"Your Article ID: {self.article_id}. If you want to restore it you need to copy and write to restore an article field \n\n\n"+self.response))
        self.article_text.setFont(QFont("Times New Roman", 15))
        self.article_text.setReadOnly(True)
        self.article_scroll_area.setWidget(self.article_text)

        with open(f'data/{self.article_id}.txt', 'w') as file:
            file.write(self.response)

        with open(f'articles/{self.article_id}.md', 'w') as file:
            file.write(self.response)

    def restore_an_article(self):
        article_id = self.restore_area.toPlainText()
        try:
            with open(f'data/{article_id}.txt', 'r') as file:
                restored_article = file.read()
                self.article_scroll_area.takeWidget()
                self.article_text = QTextBrowser()
                self.article_text.setOpenExternalLinks(True)
                self.article_text.setHtml(markdown.markdown(restored_article))
                self.article_text.setFont(QFont("Times New Roman", 15))
                self.article_text.setReadOnly(True)
                self.article_scroll_area.setWidget(self.article_text)
        except FileNotFoundError:
            # Handle if the article ID is not found
            QMessageBox.warning(self.window, "Article Not Found", "The article with the given ID was not found.")

    def save_as_pdf(self):
        article_text = self.article_text.toPlainText()
        if article_text:
            try:

                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, txt=article_text)
                pdf_file_path = f"articles/{self.article_id}.pdf"
                pdf.output(pdf_file_path)
                QMessageBox.information(self.window, "PDF Saved", f"The article has been saved as PDF: {pdf_file_path}")
            except Exception as e:
                QMessageBox.warning(self.window, "Error", f"An error occurred while saving PDF: {str(e)}")
        else:
            QMessageBox.warning(self.window, "No Content", "There is no article content to save.")