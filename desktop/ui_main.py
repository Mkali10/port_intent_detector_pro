# desktop/ui_main.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
)
from PyQt6.QtCore import QTimer
from backend.monitor import scan_connections
from backend.intent_map import get_intent
from backend.utils import is_suspicious
from desktop.plot_widget import PlotWidget
from desktop.notifications import notify_suspicious

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Port Intent Detector PRO - Desktop")
        self.resize(900, 600)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout()
        self.central.setLayout(self.layout)

        # Alert label
        self.alert_label = QLabel("")
        self.layout.addWidget(self.alert_label)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["PID", "Process", "Local", "Remote", "Protocol", "Intent", "Suspicious"])
        self.layout.addWidget(self.table)

        # Chart
        self.chart = PlotWidget()
        self.layout.addWidget(self.chart)

        self.seen_connections = set()
        self.chart_data = {}

        # Timer to update every 2 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_connections)
        self.timer.start(2000)

    def update_connections(self):
        connections = scan_connections()
        for c in connections:
            key = (c.pid, c.laddr, c.raddr, c.proto)
            if key not in self.seen_connections:
                self.seen_connections.add(key)
                intent = c.intent()
                suspicious = c.is_suspicious()

                # Add to table
                row_pos = self.table.rowCount()
                self.table.insertRow(0)
                self.table.setItem(0, 0, QTableWidgetItem(str(c.pid)))
                self.table.setItem(0, 1, QTableWidgetItem(c.name))
                self.table.setItem(0, 2, QTableWidgetItem(f"{c.laddr[0]}:{c.laddr[1]}"))
                self.table.setItem(0, 3, QTableWidgetItem(f"{c.raddr[0]}:{c.raddr[1]}"))
                self.table.setItem(0, 4, QTableWidgetItem(c.proto.upper()))
                self.table.setItem(0, 5, QTableWidgetItem(intent))
                self.table.setItem(0, 6, QTableWidgetItem("Yes" if suspicious else "No"))

                # Update alert label
                if suspicious:
                    self.alert_label.setText("⚠️ Suspicious connection detected!")
                    notify_suspicious(f"{c.name} connecting to {c.raddr[0]}:{c.raddr[1]}")

                # Update chart
                self.chart_data[intent] = self.chart_data.get(intent, 0) + 1
        self.chart.update_chart(self.chart_data)
