import os
import platform
import webbrowser

def open_file(filename):
    if platform.system() == 'Darwin':       # macOS
        webbrowser.open_new('file://' + os.path.realpath('sociedades.pdf'))
    elif platform.system() == 'Windows':    # Windows
        try:
            os.startfile(filename)
        except:
            webbrowser.open_new('file://' + os.path.realpath('sociedades.pdf'))
    else:                                   # linux variants
        webbrowser.open_new('file://' + os.path.realpath('sociedades.pdf'))