import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QListWidget, QTextEdit, QPushButton, 
                             QLineEdit, QLabel, QMessageBox)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

class EmailClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("macOS 邮箱")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建 EmailHandler 实例
        self.email_handler = Email_Handler(
            "your_email@example.com",
            "your_password",
            "smtp.example.com",
            587,
            "imap.example.com",
            993
        )
        
        # ... (之前的 UI 设置代码)
        
        # 添加刷新按钮
        refresh_button = QPushButton("刷新")
        refresh_button.clicked.connect(self.refresh_emails)
        left_layout.addWidget(refresh_button)
        
        # 初始加载邮件
        self.refresh_emails()
    
    def refresh_emails(self):
        self.email_list.clear()
        emails = self.email_handler.receive_emails()
        for email in emails:
            self.email_list.addItem(f"{email['sender']}: {email['subject']}")
        
        if emails:
            self.email_list.setCurrentRow(0)
    
    def display_email(self, item):
        if item:
            index = self.email_list.currentRow()
            email = self.email_handler.receive_emails()[index]
            self.email_display.setText(f"发件人: {email['sender']}\n主题: {email['subject']}\n\n{email['content']}")
    
    def new_email(self):
        new_email_window = NewEmailWindow(self, self.email_handler)
        new_email_window.show()

class NewEmailWindow(QWidget):
    def __init__(self, parent=None, email_handler=None):
        super().__init__(parent)
        self.email_handler = email_handler
        self.setWindowTitle("新邮件")
        self.setGeometry(200, 200, 500, 400)
        
        # ... (之前的 UI 设置代码)
    
    def send_email(self):
        to = self.to_input.text()
        subject = self.subject_input.text()
        body = self.body_input.toPlainText()
        
        if self.email_handler.send_email(to, subject, body):
            QMessageBox.information(self, "成功", "邮件已发送")
            self.close()
        else:
            QMessageBox.warning(self, "错误", "发送邮件失败")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmailClient()
    window.show()
    sys.exit(app.exec())