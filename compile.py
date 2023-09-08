from PyQt5 import uic
import sys

# Đường dẫn đến tệp .ui
ui_file = "RSA_GUI.ui"

# Chuyển đổi tệp .ui thành mã Python
py_file = "RSA_GUI.py"
uic.compileUi(ui_file, open(py_file, 'w'))