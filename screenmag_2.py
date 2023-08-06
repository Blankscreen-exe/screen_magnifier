import cv2
import numpy as np
import pyautogui
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import QTimer

class ScreenMagnifier(QWidget):
    def __init__(self, scale_factor=2):
        super().__init__()
        self.scale_factor = scale_factor

        # Create a label to display the magnified region
        self.label = QLabel(self)
        self.label.setFixedSize(200, 200)

        # Set the window properties
        self.setWindowFlags(self.windowFlags() | 0x08000000)  # Set window to be always on top
        self.setAttribute(0x01000000)  # Set attribute to enable transparency (Windows only)
        self.setWindowOpacity(0.7)

        # Start a timer to update the magnifier
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_magnifier)
        self.timer.start(30)  # Update the magnifier every 30 milliseconds

    def update_magnifier(self):
        # Get the mouse position
        mx, my = pyautogui.position()

        # Capture the screen
        screen = pyautogui.screenshot()

        # Convert the screenshot to a NumPy array
        frame = np.array(screen)

        # Calculate the region to magnify
        magnify_x1, magnify_y1 = max(0, mx - 100), max(0, my - 100)
        magnify_x2, magnify_y2 = min(frame.shape[1], mx + 100), min(frame.shape[0], my + 100)

        # Magnify the region
        magnified_frame = frame[magnify_y1:magnify_y2, magnify_x1:magnify_x2]
        magnified_frame = cv2.resize(magnified_frame, (0, 0), fx=self.scale_factor, fy=self.scale_factor)

        # Convert the magnified frame to QImage and display it in the label
        height, width, channel = magnified_frame.shape
        bytesPerLine = 3 * width
        qImg = QImage(magnified_frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        self.label.setPixmap(pixmap)

        # Move the window to follow the mouse cursor
        self.move(mx + 10, my + 10)

if __name__ == "__main__":
    import sys
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QImage, QPixmap

    app = QApplication(sys.argv)
    magnifier = ScreenMagnifier(scale_factor=2)
    magnifier.setWindowFlags(Qt.FramelessWindowHint)
    magnifier.show()
    sys.exit(app.exec_())
