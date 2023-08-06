import cv2
import numpy as np
import pyautogui
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMenu, QAction, QSystemTrayIcon
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QIcon


class ScreenMagnifier(QWidget):
    exit_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.scale_factor = 2  # Default scale factor
        self.zoom_increment = 0.2  # Zoom increment for each step
        self.setWindowFlags(self.windowFlags() | 0x08000000)
        self.setAttribute(0x01000000)
        self.setWindowOpacity(0.9)
        self.windowIsHidden = False

        # Create a label to display the magnified region
        self.label = QLabel(self)
        self.label.setFixedSize(300, 200)

        # Start a timer to update the magnifier
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_magnifier)
        self.timer.start(30)  # Update the magnifier every 30 milliseconds
        
        # Create a system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))  # Replace "icon.png" with your icon file

        # Create a context menu for the system tray icon
        self.tray_menu = QMenu(self)
        self.zoom_in_action = QAction("Zoom In", self)
        self.zoom_out_action = QAction("Zoom Out", self)
        self.exit_action = QAction("Exit", self)

        # Connect actions to their respective slots
        self.zoom_in_action.triggered.connect(self.zoom_in)
        self.zoom_out_action.triggered.connect(self.zoom_out)
        self.exit_action.triggered.connect(self.close)

        # Add actions to the context menu
        self.tray_menu.addAction(self.zoom_in_action)
        self.tray_menu.addAction(self.zoom_out_action)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.exit_action)

        # Set the context menu for the system tray icon
        self.tray_icon.setContextMenu(self.tray_menu)

        # Show the system tray icon
        self.tray_icon.show()

    def update_magnifier(self):
        # Get the mouse position
        mx, my = pyautogui.position()

        # Capture the screen
        screen = pyautogui.screenshot()

        # Convert the screenshot to a NumPy array
        frame = np.array(screen)

        # Calculate the region to magnify
        magnify_x1, magnify_y1 = max(0, mx - 200), max(0, my - 100)
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

    def zoom_in(self):
        self.scale_factor += self.zoom_increment if self.zoom_increment <= 100 else 100
        self.update()
        
    def zoom_out(self):
        self.scale_factor = max(
            1, 
            self.scale_factor - self.zoom_increment
            )
        self.update()
    
    def keyPressEvent(self, event):
        
        print("PREV === ", self.scale_factor)
        
        # Ctrl + ...
        if event.modifiers() == Qt.ControlModifier:
            # zoom in (ctrl + up)
            if event.key() == Qt.Key_Up:
                self.scale_factor += self.zoom_increment if self.scale_factor <= 5 else 0
                self.update()
                
            # zoom out (ctrl + down)
            elif event.key() == Qt.Key_Down:
                self.scale_factor = max(
                    1, 
                    self.scale_factor - self.zoom_increment
                    )
                self.update()
                
            # show magnifier (ctrl + P)
            elif event.key() == Qt.Key_P and not self.windowIsHidden:
                self.hide()
                self.windowIsHidden = True
                
            # show magnifier (ctrl + P)
            elif event.key() == Qt.Key_P and self.windowIsHidden:
                self.show()
                self.windowIsHidden = False
                
        # Alt + ...
        elif event.modifiers() == Qt.AltModifier:
            pass
        
        # hide magnifier (Esc)
        elif event.key() == Qt.Key_Escape:
            self.hide()
            
            
            # elif event.key() == Qt.ScrollPhase:
            #     self.scale_factor += self.zoom_increment
            #     self.update()
            # elif event.key() == Qt.Key_Down:
            #     self.scale_factor = max(1, self.scale_factor - self.zoom_increment)
            #     self.update()

        print("MOD === ", self.scale_factor)
        
        print("")
        
    def closeEvent(self, event):
        self.exit_signal.emit()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    magnifier = ScreenMagnifier()
    magnifier.setWindowFlags(Qt.FramelessWindowHint)
    magnifier.show()

    # Connect the exit signal to the QApplication quit method
    magnifier.exit_signal.connect(app.quit)

    sys.exit(app.exec_())

    