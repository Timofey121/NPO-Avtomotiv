import sqlite3
import sys

import psutil
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
)


class MonitorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initDB()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.is_recording = False

    def initUI(self):
        self.setWindowTitle("System Monitor")

        self.cpu_label = QLabel("CPU: 0%")
        self.memory_label = QLabel("Memory: 0%")
        self.disk_label = QLabel("Disk: 0%")

        self.start_button = QPushButton("Start Recording")
        self.stop_button = QPushButton("Stop Recording (Disabled)")
        self.history_button = QPushButton("Show History")
        self.stop_button.setEnabled(False)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Timestamp", "CPU", "Memory", "Disk"])

        layout = QVBoxLayout()
        data_layout = QHBoxLayout()
        data_layout.addWidget(self.cpu_label)
        data_layout.addWidget(self.memory_label)
        data_layout.addWidget(self.disk_label)
        layout.addLayout(data_layout)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.history_button)
        layout.addLayout(button_layout)
        layout.addWidget(self.history_table)
        self.setLayout(layout)

        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)
        self.history_button.clicked.connect(self.show_history)

    def initDB(self):
        self.conn = sqlite3.connect('system_monitor.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                                timestamp TEXT,
                                cpu_usage REAL,
                                memory_usage REAL,
                                disk_usage REAL)''')

    def update_data(self):
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        self.cpu_label.setText(f"CPU: {cpu_percent}%")
        self.memory_label.setText(f"Memory: {memory_percent}%")
        self.disk_label.setText(f"Disk: {disk_usage}%")

        if self.is_recording:
            timestamp = QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')
            self.cursor.execute("INSERT INTO data VALUES (?, ?, ?, ?)",
                                (timestamp, cpu_percent, memory_percent, disk_usage))
            self.conn.commit()

    def start_recording(self):
        self.is_recording = True
        self.timer.start(1000)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_recording(self):
        self.is_recording = False
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def show_history(self):
        # Очистить таблицу
        self.history_table.clearContents()

        self.cursor.execute("SELECT * FROM data")
        results = self.cursor.fetchall()

        self.history_table.setRowCount(len(results))
        for row_index, row_data in enumerate(results):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.history_table.setItem(row_index, col_index, item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MonitorApp()
    ex.show()
    sys.exit(app.exec_())
