import sys
import os
import time
import threading
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar, QHBoxLayout, QFileDialog
from PyQt5.QtCore import Qt
import speedtest

class SpeedTestApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Wi-Fi Speed Test")

        # Add labels for displaying download, upload speeds, latency and signal strength
        self.download_label = QLabel("Download speed: -")
        self.upload_label = QLabel("Upload speed: -")
        self.latency_label = QLabel("Latency: -")
        self.signal_strength_label = QLabel("Signal Strength: -")

        # Add button to initiate speed test
        self.test_button = QPushButton("Run Speed Test")
        self.test_button.clicked.connect(self.run_speed_test)

        # Add progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)

        # Add button to save results
        self.save_button = QPushButton("Save Results")
        self.save_button.clicked.connect(self.save_results)

        # Add labels, progress bar, and buttons to layout
        labels_layout = QVBoxLayout()
        labels_layout.addWidget(self.download_label)
        labels_layout.addWidget(self.upload_label)
        labels_layout.addWidget(self.latency_label)
        labels_layout.addWidget(self.signal_strength_label)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.test_button)
        buttons_layout.addWidget(self.save_button)

        layout = QVBoxLayout()
        layout.addLayout(labels_layout)
        layout.addWidget(self.progress_bar)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def run_speed_test(self):
        # Disable the test button while the speed test is running
        self.test_button.setEnabled(False)

        # Run speed test in a separate thread and update labels with results
        speed_test_thread = threading.Thread(target=self.run_speed_test_thread)
        speed_test_thread.start()

    def run_speed_test_thread(self):
        st = speedtest.Speedtest()
        download_speed = st.download() / 1000000
        upload_speed = st.upload() / 1000000
        ping = st.results.ping
        signal_strength = self.measure_signal_strength()

        self.download_label.setText(f"Download speed: {download_speed:.2f} Mbps")
        self.upload_label.setText(f"Upload speed: {upload_speed:.2f} Mbps")
        self.latency_label.setText(f"Latency: {ping:.2f} ms")
        self.signal_strength_label.setText(f"Signal Strength: {signal_strength:.2f} dBm")

        # Enable the test button after the speed test is complete
        self.test_button.setEnabled(True)

    def measure_signal_strength(self):
        # Measure signal strength using the airport command
        try:
            signal_strength = float(os.popen('/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | awk -F " " \'/agrCtlRSSI/ {print $2}\'').read().strip())
        except ValueError:
            signal_strength = None
        return signal_strength
        
    def save_results(self):
        # Open a file dialog to select a file to save the results to
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Save Results", "", "Text Files (*.txt)")
        
        # Save the results to the selected file
        with open(file_path, "w") as f:
            f.write(f"Download speed: {self.download_label.text()}\n")
            f.write(f"Upload speed: {self.upload_label.text()}\n")
            f.write(f"Latency: {self.latency_label.text()}\n")
            f.write(f"Signal Strength: {self.signal_strength_label.text()}\n")
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    speed_test_app = SpeedTestApp()
    speed_test_app.show()
    sys.exit(app.exec_())
