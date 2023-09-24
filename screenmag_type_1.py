import cv2
import numpy as np
import pyautogui
import keyboard

def screen_magnifier(scale_factor=2):
    while True:
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
        magnified_frame = cv2.resize(magnified_frame, (0, 0), fx=scale_factor, fy=scale_factor)

        # Display the magnified region
        cv2.imshow('Magnifier', magnified_frame)

        # Check for the hotkey to exit (e.g., Esc key)
        if keyboard.is_pressed('Esc'):
            break

        cv2.waitKey(1)

    cv2.destroyAllWindows()
    sys.exit(app.exec_())

if __name__ == "__main__":
    screen_magnifier(scale_factor=2)
