###############################################################################
#   File: SwagerStationGUI.py
#   Author(s): Dravin Flores
#   Date Created: 29 June, 2021
#
#   Purpose: The new procedure for swaging tubes means that a tube is tensioned
#       before it can be swaged. The current program cannot handle this, and 
#       so a new program was created specifically for this reason.
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################

pyside_version = None
try:
    from PySide6 import QtCore, QtWidgets, QtGui
    pyside_version = 6
except ImportError:
    from PySide2 import QtCore, QtWidgets, QtGui
    pyside_version = 2

from datetime import date
from pathlib import Path

import os
import sys

is_in_dropbox_directory = False

# sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# We need to check if the file is being ran from dropbox or if it is being
# ran locally.
if is_in_dropbox_directory:
    DROPBOX_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(DROPBOX_DIR)
else:
    # This way uses the pathlib library. 
    # p = Path(__file__).resolve().parent
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(p)

# This is for debugging purposes
MSU_CODE = 'TEST'
TEST_LEN = 53535353353553

from sMDT import db, tube
from sMDT.data import swage, status

# Subclass the QWidget to be the central widget, create the layout for all the
# little subwidgets, and then set the central widget's layout.
class SwageWidget(QtWidgets.QWidget):
    def __init__(self, db):
        super().__init__()
        self.database = db
        self.setWindowTitle("Swage Station GUI")
        layout = QtWidgets.QVBoxLayout()

        # Here is for the combo-box selector.
        self.clean_code_combo = QtWidgets.QComboBox()

        cc = [
            "0: Not Cleaned",
            "1: Cleaning described in comment",
            "2: Wiped with Ethanol",
            "3: Only Vacuumed",
            "4: Vacuumed and Wiped with Ethanol",
            "5: Vacuumed with Nitrogen"
        ]

        self.clean_code_combo.addItems([
            cc[0], cc[1], cc[2], cc[3], cc[4], cc[5]
        ])
        
        # Here is for all the data entries.
        self.swage_entry = QtWidgets.QWidget()
        self.swage_entry_layout = QtWidgets.QFormLayout()

        # Here are all the text entries.
        # self.name_entry = QtWidgets.QLineEdit()
        self.name_entry = CustomLineEdit()
        self.barcode_entry = QtWidgets.QLineEdit()
        self.raw_length_entry = QtWidgets.QLineEdit()
        self.swage_length_entry = QtWidgets.QLineEdit()

        # Here we are adding in the rows with the names for the columns.
        self.swage_entry_layout.addRow("Name:", self.name_entry)
        self.swage_entry_layout.addRow("Tube ID:", self.barcode_entry)
        self.swage_entry_layout.addRow("Raw Length:", self.raw_length_entry)
        self.swage_entry_layout.addRow("Swage Length:", self.swage_length_entry)
        self.swage_entry_layout.addRow("Clean Code:", self.clean_code_combo)
        self.swage_entry.setLayout(self.swage_entry_layout)

        # Here is for the enter button.
        self.enter_button = QtWidgets.QPushButton("Create Entry")
        self.text_box = TubeDataWindow()

        layout.addWidget(self.swage_entry)
        layout.addWidget(self.enter_button)
        layout.addWidget(self.text_box)
        self.setLayout(layout)

        # self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

    def autofill_lengths(self, tube_id):
        # Debugging Purposes
        if tube_id == MSU_CODE:
            return (TEST_LEN, TEST_LEN)

        try:
            t = self.database.get_tube(tube_id)
        except KeyError:
            return (None, None)
        else:
            r = t.swage.get_record('last')
            return (r.raw_length, r.swage_length)


    def change_text_boxes_for_lengths(self, tube_id):
        (raw_len, swage_len) = self.autofill_lengths(tube_id)

        if raw_len is None and swage_len is None:
            return
        
    @QtCore.Slot()
    def print_changed_text(self, text):
        print(text)

    def write_to_database(self, barcode, name, clean_code, raw_len, swage_len):
        t = tube.Tube()
        t.set_ID(barcode)

        if raw_len is not None:
            raw_len = float(raw_len)

        if swage_len is not None:
            swage_len = float(swage_len)

        rec = swage.SwageRecord(
            raw_length=raw_len, 
            swage_length=swage_len, 
            clean_code=clean_code, 
            user=name
        )

        t.swage.add_record(rec)
        self.database.add_tube(t)


class CustomLineEdit(QtWidgets.QLineEdit):
    def __init__(self):
        super().__init__()
        self.recorded_text = None

    def event(self, event):
        if event.type() == QtCore.QEvent.KeyPress and \
                event.key() == QtCore.Qt.Key_Tab:
            self.tabPressed(self.text())
            return QtWidgets.QLineEdit.event(self, event)
        else:
            return QtWidgets.QLineEdit.event(self, event)

    def tabPressed(self, text):
        self.recorded_text = text
        # print(self.recorded_text)


# This is a copy.
class TubeDataWindow(QtWidgets.QWidget):
    """
    This class creates a widget which can display text to the screen.
    """
    def __init__(self, data_str=None):
        super().__init__()

        layout = QtWidgets.QVBoxLayout()

        self.text_box = QtWidgets.QLabel()

        if data_str is not None:
            self.text_box.setText(data_str)

        self.scrollable_window = QtWidgets.QScrollArea()
        self.scrollable_window.setWidget(self.text_box)
        self.scrollable_window.setWidgetResizable(True)

        layout.addWidget(self.scrollable_window)
        self.setLayout(layout)

    def setText(self, text_str):
        self.text_box.setText(text_str)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.database = db

        self.title = "Swage Station GUI"
        self.left = 0
        self.top = 0
        self.width = 400
        self.height = 300

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        self.swage_widget = SwageWidget(db)
        self.setCentralWidget(self.swage_widget)


def run():
    database = db.db()
    app = QtWidgets.QApplication(sys.argv)

    app.setStyle("fusion")

    window = MainWindow(database)
    window.show()

    if pyside_version == 2:
        sys.exit(app.exec_())
    elif pyside_version == 6:
        sys.exit(app.exec())

if __name__ == '__main__':
    run()
