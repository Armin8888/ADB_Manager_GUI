import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QListWidget, QFileDialog, QTabWidget, QLineEdit, QMessageBox
)


def run_adb(cmd):
    try:
        result = subprocess.check_output(["adb"] + cmd.split(), stderr=subprocess.STDOUT)
        return result.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return e.output.decode("utf-8")


class ADBTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("مدیریت ADB (ساعت هوشمند)")
        self.setGeometry(200, 100, 700, 500)

        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # --- تب مدیریت دستگاه ---
        self.tab_devices = QWidget()
        self.tabs.addTab(self.tab_devices, "مدیریت دستگاه")

        dev_layout = QVBoxLayout()
        self.device_list = QListWidget()
        self.refresh_btn = QPushButton("🔄 رفرش دستگاه‌ها")
        self.wifi_btn = QPushButton("📡 اتصال بی‌سیم")
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("IP دستگاه (مثلا 192.168.1.5)")
        self.port_input = QLineEdit("5555")
        self.port_input.setPlaceholderText("پورت (پیش‌فرض 5555)")

        self.refresh_btn.clicked.connect(self.refresh_devices)
        self.wifi_btn.clicked.connect(self.connect_wifi)

        dev_layout.addWidget(self.device_list)
        dev_layout.addWidget(self.refresh_btn)
        dev_layout.addWidget(QLabel("اتصال بی‌سیم:"))
        dev_layout.addWidget(self.ip_input)
        dev_layout.addWidget(self.port_input)
        dev_layout.addWidget(self.wifi_btn)
        self.tab_devices.setLayout(dev_layout)

        # --- تب مدیریت برنامه‌ها ---
        self.tab_apps = QWidget()
        self.tabs.addTab(self.tab_apps, "مدیریت برنامه‌ها")

        app_layout = QVBoxLayout()
        self.app_list = QListWidget()
        self.list_apps_btn = QPushButton("📜 لیست برنامه‌ها")
        self.uninstall_btn = QPushButton("❌ حذف برنامه انتخابی")
        self.extract_btn = QPushButton("📂 استخراج APK")
        self.disable_btn = QPushButton("🚫 غیرفعال کردن")
        self.enable_btn = QPushButton("✅ فعال کردن")

        self.list_apps_btn.clicked.connect(self.list_apps)
        self.uninstall_btn.clicked.connect(self.uninstall_app)
        self.extract_btn.clicked.connect(self.extract_app)
        self.disable_btn.clicked.connect(self.disable_app)
        self.enable_btn.clicked.connect(self.enable_app)

        for w in [self.app_list, self.list_apps_btn,
                  self.uninstall_btn, self.extract_btn,
                  self.disable_btn, self.enable_btn]:
            app_layout.addWidget(w)
        self.tab_apps.setLayout(app_layout)

        # --- تب فایل‌ها ---
        self.tab_files = QWidget()
        self.tabs.addTab(self.tab_files, "فایل‌ها")

        file_layout = QVBoxLayout()
        self.push_btn = QPushButton("📤 ارسال فایل به دستگاه")
        self.pull_btn = QPushButton("📥 دریافت فایل از دستگاه")
        self.push_btn.clicked.connect(self.push_file)
        self.pull_btn.clicked.connect(self.pull_file)
        file_layout.addWidget(self.push_btn)
        file_layout.addWidget(self.pull_btn)
        self.tab_files.setLayout(file_layout)

        # --- تب ابزارها ---
        self.tab_tools = QWidget()
        self.tabs.addTab(self.tab_tools, "ابزارها")

        tool_layout = QVBoxLayout()
        self.screenshot_btn = QPushButton("📸 گرفتن اسکرین‌شات")
        self.record_btn = QPushButton("🎥 ضبط صفحه")
        self.reboot_btn = QPushButton("🔄 ری‌استارت دستگاه")
        self.clear_cache_btn = QPushButton("🧹 پاک کردن کش همه برنامه‌ها")

        self.screenshot_btn.clicked.connect(self.take_screenshot)
        self.record_btn.clicked.connect(self.record_screen)
        self.reboot_btn.clicked.connect(lambda: run_adb("reboot"))
        self.clear_cache_btn.clicked.connect(lambda: run_adb("shell pm clear-all"))

        for w in [self.screenshot_btn, self.record_btn, self.reboot_btn, self.clear_cache_btn]:
            tool_layout.addWidget(w)
        self.tab_tools.setLayout(tool_layout)

        self.setLayout(layout)

    # ---- توابع ----
    def refresh_devices(self):
        self.device_list.clear()
        out = run_adb("devices")
        for line in out.splitlines()[1:]:
            if line.strip():
                self.device_list.addItem(line)

    def connect_wifi(self):
        ip = self.ip_input.text().strip()
        port = self.port_input.text().strip()
        if not ip:
            QMessageBox.warning(self, "خطا", "لطفا IP دستگاه را وارد کنید.")
            return
        run_adb("tcpip " + port)
        out = run_adb(f"connect {ip}:{port}")
        QMessageBox.information(self, "اتصال بی‌سیم", out)
        self.refresh_devices()

    def list_apps(self):
        self.app_list.clear()
        out = run_adb("shell pm list packages")
        for line in out.splitlines():
            self.app_list.addItem(line.replace("package:", ""))

    def uninstall_app(self):
        item = self.app_list.currentItem()
        if item:
            out = run_adb(f"uninstall {item.text()}")
            QMessageBox.information(self, "حذف برنامه", out)

    def extract_app(self):
        item = self.app_list.currentItem()
        if item:
            out = run_adb(f"shell pm path {item.text()}")
            apk_path = out.split(":")[-1].strip()
            save_path, _ = QFileDialog.getSaveFileName(self, "ذخیره APK", f"{item.text()}.apk")
            if save_path:
                run_adb(f"pull {apk_path} \"{save_path}\"")

    def disable_app(self):
        item = self.app_list.currentItem()
        if item:
            run_adb(f"shell pm disable-user {item.text()}")

    def enable_app(self):
        item = self.app_list.currentItem()
        if item:
            run_adb(f"shell pm enable {item.text()}")

    def push_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "انتخاب فایل برای ارسال")
        if file:
            run_adb(f"push \"{file}\" /sdcard/")

    def pull_file(self):
        save_path, _ = QFileDialog.getSaveFileName(self, "ذخیره فایل دریافت‌شده")
        if save_path:
            run_adb(f"pull /sdcard/screenshot.png \"{save_path}\"")

    def take_screenshot(self):
        run_adb("shell screencap -p /sdcard/screenshot.png")
        self.pull_file()

    def record_screen(self):
        save_path, _ = QFileDialog.getSaveFileName(self, "ذخیره ویدیو", "screen.mp4")
        if save_path:
            run_adb("shell screenrecord /sdcard/screen.mp4 & timeout 10")
            run_adb(f"pull /sdcard/screen.mp4 \"{save_path}\"")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ADBTool()
    win.show()
    sys.exit(app.exec_())
