from gtts import gTTS
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

# Завантажити .env
load_dotenv()

# Дані відправника
sender_email = "ruzhe_43@ukr.net"
sender_password = os.getenv("EMAIL_PASSWORD")

# Введення даних користувача
text_file_path = input("Введіть шлях до текстового файлу: ")
if not os.path.exists(text_file_path):
    print("❌ Файл не знайдено.")
    exit()

with open(text_file_path, 'r', encoding='utf-8') as file:
    text = file.read()

mp3_filename = input("Введіть назву mp3-файлу (без .mp3): ") + ".mp3"
receiver_email = input("Введіть електронну адресу отримувача: ")

# Озвучення
tts = gTTS(text=text, lang='uk')
tts.save(mp3_filename)
print(f"✅MP3 файл '{mp3_filename}' створено.")

# Формування листа
msg = EmailMessage()
msg['Subject'] = 'Озвучений текст'
msg['From'] = sender_email
msg['To'] = receiver_email
msg.set_content(text)

with open(mp3_filename, 'rb') as f:
    msg.add_attachment(f.read(), maintype='audio', subtype='mpeg', filename=mp3_filename)

# Надсилання
with smtplib.SMTP_SSL('smtp.ukr.net', 465) as smtp:
    smtp.login(sender_email, sender_password)
    smtp.send_message(msg)

print(f"📧Лист з mp3 надіслано на {receiver_email}")

# Очистка
os.remove(mp3_filename)