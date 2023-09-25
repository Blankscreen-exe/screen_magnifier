# Screen Magnifier

An app for magnifying a portion of the screen. Useful for when you want to enlarge a portion of the screen while presentating a lot code and text.

> This repo is a part of the blog article that I have written. Checkout the blog [here](url).

# Technologies

- `opencv-python`==4.8.0.74
- `Pillow`==10.0.0
- `PyQt5`==5.15.9

# Installation & Usage

1. Use a virtual environment of your choice and install dependencies inside it fro m`requirements.txt`.

```bash
pip3 install -r requirements.txt
```

2. Run the script

```bash
python3 ./screenmag_pyqt5.py
```

3. In order to run the experimental `PyAutoGUI` version, you will need to install its dependency using the following command.

```bash
pip3 install pyautogui
```

# Preview
![App preview](docs/images/preview.png)
