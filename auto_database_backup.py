#Viết code python thực hiện việc backup file database(.sql, .sqlite3) 
# lúc 00:00 AM là 12 giờ đêm (nửa đêm) hằng ngày 
# và gửi mail thông báo việc backup thành công hoặc thất bại

from email.message import EmailMessage
import os
import smtplib
from datetime import datetime
import shutil
import time
import schedule
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.sqlite3")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')  
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')

os.makedirs(BACKUP_DIR, exist_ok=True)

def send_email(subject, content):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg.set_content(content)
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"Email đã được gửi đến {EMAIL_RECEIVER}")
    except Exception as e:
        print(f"Lỗi khi gửi email: {e}")

def backup_db():
    try:
        timestamp_for_file = datetime.now().strftime("%Y%m%d_%H%M%S")
        timestamp_display = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        db_name = os.path.basename(DB_PATH)
        backup_file = os.path.join(BACKUP_DIR, f"{db_name}_{timestamp_for_file}")
        
        shutil.copy(DB_PATH, backup_file)
        
        send_email(
            subject="Backup Database thành công",
            content=f"Backup database thành công lúc {timestamp_display}. File: {backup_file}"
        )
        print("Backup thành công.")
    except Exception as e:
        send_email(
            subject="Backup Database thất bại",
            content=f"Lỗi: {str(e)}"
        )
        
schedule.every().day.at("00:00").do(backup_db)

print("Chương trình backup đã khởi động...")

while True:
    schedule.run_pending()
    time.sleep(1)
        