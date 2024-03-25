import os

path = os.path.dirname(os.path.abspath(__file__))

paths: {str: str} = {
    "icons": path + "/resources/icons/",
    "blocks": path + "\python\data\\blocksInfo.txt",
    "blocksIcons": path + "\\resources\\blocksIcons\\"
}

if __name__ == "__main__":
    from python.presentation.MainWindow.MainWindow import execute
    execute()