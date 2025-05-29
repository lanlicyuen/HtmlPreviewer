import sys
import os
import json
import locale
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTextEdit, QPushButton, QFileDialog, QMenuBar,
                             QSplitter, QMessageBox)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QDateTime, Qt, QFileInfo, QLocale
from PyQt6.QtGui import QAction

# 语言检测与多语言字典
def get_language():
    lang = QLocale.system().name()
    if lang.startswith('zh'):
        return 'zh'
    else:
        return 'en'

LANG = get_language()

TEXTS = {
    'title': {'zh': 'HTML预览器', 'en': 'HTML Previewer'},
    'placeholder': {'zh': '在此粘贴HTML代码...', 'en': 'Paste your HTML code here...'},
    'save_code': {'zh': '保存代码', 'en': 'Save Code'},
    'save_preview': {'zh': '保存预览文件', 'en': 'Save Preview'},
    'save_as': {'zh': '另存文件', 'en': 'Save As...'},
    'menu_file': {'zh': '文件', 'en': 'File'},
    'menu_open': {'zh': '打开文件', 'en': 'Open File'},
    'menu_settings': {'zh': '设定', 'en': 'Settings'},
    'menu_set_path': {'zh': '设置保存路径', 'en': 'Set Save Path'},
    'menu_about': {'zh': '关于我', 'en': 'About'},
    'about_title': {'zh': '关于本工具', 'en': 'About This Tool'},
    'about_info': {
        'zh': '个人爱好开发，随便使用，电脑炸了自负！\n\n小工具由  Lanlic Yuen (1Plab CE)  V 1.0\n有问题可联系：lanlic@hotmail.com\n未必回，但未必不看。',
        'en': 'Personal hobby project, use at your own risk!\n\nTool by Lanlic Yuen (1Plab CE)  V 1.0\nContact: lanlic@hotmail.com\nNo guarantee for reply, but I may read it.'
    },
    'success_save': {'zh': '保存成功', 'en': 'Saved Successfully'},
    'fail_save': {'zh': '保存失败', 'en': 'Save Failed'},
    'open_fail': {'zh': '打开文件失败', 'en': 'Failed to Open File'},
    'drag_fail': {'zh': '拖拽打开文件失败', 'en': 'Failed to Open File by Dragging'},
    'select_path': {'zh': '选择保存路径', 'en': 'Select Save Path'},
    'save_path_set': {'zh': '保存路径已设置为: ', 'en': 'Save path set to: '},
}

SETTINGS_FILE = 'settings.json'

class HtmlPreviewApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_lang = LANG  # 新增：当前语言
        self.setWindowTitle(TEXTS['title'][self.current_lang])
        self.setGeometry(100, 100, 1200, 800)
        self.save_path = "C:/Temp"
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path, exist_ok=True)
        self.load_settings()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(5, 5, 5, 5)
        self.html_input = QTextEdit()
        self.html_input.setPlaceholderText(TEXTS['placeholder'][self.current_lang])
        self.html_input.textChanged.connect(self.update_preview)
        self.html_input.setAcceptDrops(False)
        left_layout.addWidget(self.html_input)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(5, 5, 5, 5)
        self.preview = QWebEngineView()
        right_layout.addWidget(self.preview)
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 5, 0, 0)
        self.save_code_btn = QPushButton(TEXTS['save_code'][self.current_lang])
        self.save_code_btn.clicked.connect(self.save_code)
        button_layout.addWidget(self.save_code_btn)
        self.save_preview_btn = QPushButton(TEXTS['save_preview'][self.current_lang])
        self.save_preview_btn.clicked.connect(self.save_preview)
        button_layout.addWidget(self.save_preview_btn)
        self.save_as_btn = QPushButton(TEXTS['save_as'][self.current_lang])
        self.save_as_btn.clicked.connect(self.save_preview_as)
        button_layout.addWidget(self.save_as_btn)
        right_layout.addLayout(button_layout)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 700])
        self.create_menu_bar()
        self.setAcceptDrops(True)

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.save_path = data.get('save_path', self.save_path)
            except Exception as e:
                print(f"读取设定失败: {e}")

    def save_settings(self):
        try:
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump({'save_path': self.save_path}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存设定失败: {e}")

    def refresh_ui_language(self):
        self.setWindowTitle(TEXTS['title'][self.current_lang])
        self.html_input.setPlaceholderText(TEXTS['placeholder'][self.current_lang])
        self.save_code_btn.setText(TEXTS['save_code'][self.current_lang])
        self.save_preview_btn.setText(TEXTS['save_preview'][self.current_lang])
        self.save_as_btn.setText(TEXTS['save_as'][self.current_lang])
        self.menuBar().clear()
        self.create_menu_bar()

    def create_menu_bar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu(TEXTS['menu_file'][self.current_lang])
        open_file_action = QAction(TEXTS['menu_open'][self.current_lang], self)
        open_file_action.triggered.connect(self.open_html_file)
        file_menu.addAction(open_file_action)
        settings_menu = menubar.addMenu(TEXTS['menu_settings'][self.current_lang])
        set_save_path_action = QAction(TEXTS['menu_set_path'][self.current_lang], self)
        set_save_path_action.triggered.connect(self.set_save_path)
        settings_menu.addAction(set_save_path_action)
        # 新增语言切换
        lang_menu = settings_menu.addMenu('语言 / Language')
        lang_zh_action = QAction('中文', self)
        lang_en_action = QAction('English', self)
        lang_zh_action.triggered.connect(lambda: self.set_language('zh'))
        lang_en_action.triggered.connect(lambda: self.set_language('en'))
        lang_menu.addAction(lang_zh_action)
        lang_menu.addAction(lang_en_action)
        about_menu = menubar.addMenu(TEXTS['menu_about'][self.current_lang])
        about_action = QAction(TEXTS['about_title'][self.current_lang], self)
        about_action.triggered.connect(self.show_about_dialog)
        about_menu.addAction(about_action)

    def set_language(self, lang):
        self.current_lang = lang
        self.refresh_ui_language()

    def update_preview(self):
        html_content = self.html_input.toPlainText()
        self.preview.setHtml(html_content)

    def get_timestamp_filename(self, extension):
        now = QDateTime.currentDateTime()
        timestamp = now.toString("yyyyMMdd_HHmmss")
        return f"{timestamp}.{extension}"

    def save_code(self):
        filename = self.get_timestamp_filename("html")
        filepath = os.path.join(self.save_path, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(self.html_input.toPlainText())
            QMessageBox.information(self, TEXTS['success_save'][self.current_lang], f"HTML {TEXTS['save_code'][self.current_lang]}: {filepath}")
        except Exception as e:
            QMessageBox.warning(self, TEXTS['fail_save'][self.current_lang], f"{TEXTS['save_code'][self.current_lang]}: {e}")

    def open_html_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, TEXTS['menu_open'][self.current_lang], self.save_path, "HTML Files (*.html *.htm);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    html = f.read()
                self.html_input.setPlainText(html)
            except Exception as e:
                QMessageBox.warning(self, TEXTS['open_fail'][self.current_lang], f"{TEXTS['open_fail'][self.current_lang]}: {e}")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith(('.html', '.htm')):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.html', '.htm')):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        html = f.read()
                    self.html_input.setPlainText(html)
                except Exception as e:
                    QMessageBox.warning(self, TEXTS['drag_fail'][self.current_lang], f"{TEXTS['drag_fail'][self.current_lang]}: {e}")

    def save_preview(self):
        filename = self.get_timestamp_filename("pdf")
        filepath = os.path.join(self.save_path, filename)
        filepath = os.path.abspath(filepath)
        try:
            self.preview.page().printToPdf(filepath)
            QMessageBox.information(self, TEXTS['success_save'][self.current_lang], f"{TEXTS['save_preview'][self.current_lang]}: {filepath}")
        except Exception as e:
            QMessageBox.warning(self, TEXTS['fail_save'][self.current_lang], f"{TEXTS['save_preview'][self.current_lang]}: {e}")

    def save_preview_as(self):
        filename = self.get_timestamp_filename("pdf")
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            TEXTS['save_as'][self.current_lang],
            os.path.join(self.save_path, filename),
            "PDF Files (*.pdf);;All Files (*)"
        )
        if filepath:
            filepath = os.path.abspath(filepath)
            try:
                self.preview.page().printToPdf(filepath)
                QMessageBox.information(self, TEXTS['success_save'][self.current_lang], f"{TEXTS['save_preview'][self.current_lang]}: {filepath}")
            except Exception as e:
                QMessageBox.warning(self, TEXTS['fail_save'][self.current_lang], f"{TEXTS['save_preview'][self.current_lang]}: {e}")

    def set_save_path(self):
        new_path = QFileDialog.getExistingDirectory(
            self,
            TEXTS['select_path'][self.current_lang],
            self.save_path
        )
        if new_path:
            self.save_path = new_path
            self.save_settings()
            QMessageBox.information(self, TEXTS['success_save'][self.current_lang], f"{TEXTS['save_path_set'][self.current_lang]}{self.save_path}")

    def show_about_dialog(self):
        QMessageBox.information(self, TEXTS['about_title'][self.current_lang], TEXTS['about_info'][self.current_lang])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HtmlPreviewApp()
    window.show()
    sys.exit(app.exec())