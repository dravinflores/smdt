import os
import sys
import csv
import datetime
from pathlib import Path

pyside_version = None
try:
    from PySide6 import QtCore, QtWidgets, QtGui, QtUiTools
    pyside_version = 6
except ImportError:
    from PySide2 import QtCore, QtWidgets, QtGui, QtUiTools
    pyside_version = 2

debug = True


def add_directory_to_path():
    parent_directory = Path().parent.resolve()
    sys.path.append(parent_directory)


def add_directory_to_path_alt():
    sMDT_DIR = os.path.dirname(os.path.abspath(__file__))
    containing_dir = os.path.dirname(sMDT_DIR)
    sys.path.append(containing_dir)


add_directory_to_path_alt()
from sMDT import db
from sMDT.data import status


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, database):
        super().__init__()

        self.title = "Export Tubes"
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 400

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        self.export_tubes_widget = ExportTubesWidget(database)
        self.setCentralWidget(self.export_tubes_widget)


class ExportTubesWidget(QtWidgets.QWidget):
    def __init__(self, database):
        super().__init__()
        self.database = database
        self.setup_name_widget()
        self.setup_tube_list_widget()
        self.setup_edit_buttons_widget()
        self.setup_barcode_widget()
        self.setup_export_button_widget()
        self.setup_status_widget()

        self.add_widgets_to_layout()
        self.connect_signals()

        self.name = ''
        self.tube_dict = {
            "Row 1": [],
            "Row 2": [],
            "Row 3": [],
            "Row 4": [],
            "Row 5": [],
            "Row 6": [],
            "Row 7": [],
            "Row 8": [],
            "Row 9": [],
            "Row 10": []
        }

        model = self.create_item_model()
        self.tree_view.setModel(model)

    def setup_name_widget(self):
        self.name_container = QtWidgets.QWidget()
        self.name_entry = QtWidgets.QLineEdit()
        self.name_label = "Name:"
        layout = QtWidgets.QFormLayout()
        layout.addRow(self.name_label, self.name_entry)
        self.name_container.setLayout(layout)

    def setup_tube_list_widget(self):
        self.tube_list_container = QtWidgets.QGroupBox("Ready To Export")
        self.tree_view = DataView(self.database)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.tree_view)
        self.tube_list_container.setLayout(layout)

    def setup_edit_buttons_widget(self):
        self.edit_buttons_container = QtWidgets.QWidget()
        self.remove_button = QtWidgets.QPushButton("Remove")
        self.replace_button = QtWidgets.QPushButton("Replace")
        remove_tip = "Select the tube from the list above to remove."
        replace_tip = "Select the tube from the list above to replace."
        self.remove_button.setToolTip(remove_tip)
        self.replace_button.setToolTip(replace_tip)
        layout = QtWidgets.QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.remove_button)
        layout.addWidget(self.replace_button)
        layout.addStretch()
        self.edit_buttons_container.setLayout(layout)

    def setup_barcode_widget(self):
        self.barcode_container = QtWidgets.QWidget()
        self.barcode_entry = QtWidgets.QLineEdit()
        self.barcode_entry.setPlaceholderText("MSU00000")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.barcode_entry)
        self.barcode_container.setLayout(layout)

    def setup_export_button_widget(self):
        self.export_button_container = QtWidgets.QWidget()
        self.export_button = QtWidgets.QPushButton("Export Tubes")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.export_button)
        self.export_button_container.setLayout(layout)

    def setup_status_widget(self):
        self.status_container = QtWidgets.QWidget()
        self.status_window = StatusWindow()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.status_window)
        self.status_container.setLayout(layout)

    def add_widgets_to_layout(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.name_container)
        main_layout.addWidget(self.tube_list_container)
        main_layout.addWidget(self.edit_buttons_container)
        main_layout.addWidget(self.barcode_container)
        main_layout.addWidget(self.export_button_container)
        main_layout.addWidget(self.status_container)
        self.setLayout(main_layout)

    def connect_signals(self):
        self.name_entry.editingFinished.connect(self.add_name)
        # self.barcode_entry.editingFinished.connect(self.add_tube)
        self.barcode_entry.returnPressed.connect(self.add_tube)
        self.export_button.pressed.connect(self.to_csv)
        self.remove_button.pressed.connect(self.remove)
        self.replace_button.pressed.connect(self.replace)

    def add_name(self):
        if len(self.name_entry.text()):
            self.name = self.name_entry.text()

    def to_csv(self):
        if any(len(val) < 10 for val in self.tube_dict.values()):
            QtWidgets.QMessageBox.warning(
                    None,
                    'Not Enough Barcodes',
                    "Please fill the shipment with tubes")
        if not self.name:
            QtWidgets.QMessageBox.warning(
                    None,
                    'No Name',
                    "Please fill in your name")
        else:
            # So we're going to need to adjust our system so that we can
            # find where the csv file is to be placed.
            current_dir = Path().resolve()
            exported_tubes_dir = current_dir.parent / 'Exported_Tubes'

            # Now we need to add this folder if it doesn't exist.
            exported_tubes_dir.mkdir(parents=True, exist_ok=True)

            current_date = datetime.datetime.now()
            file_name = current_date.strftime("%Y_%m_%d-%H_%M_%S") + '.csv'
            csv_file = exported_tubes_dir / file_name

            if csv_file.exists():
                write_opening_line = False
            else:
                write_opening_line = False

            fieldnames = [
                "logger",
                "row",
                "barcode",
                "first_tension",
                "first_frequency",
                "first_tension_date",
                "dark_current",
                "leak_rate"
            ]

            csv_lines = []
            for (key, val) in self.tube_dict.items():
                for tube_id in val:
                    t = self.database.get_tube(tube_id)
                    logger = self.name
                    row = key[3:]
                    barcode = tube_id
                    (tension, frequency, d) = self.get_first_tension(t)
                    dc = t.dark_current.get_record('last').dark_current
                    leak = t.leak.get_record('last').leak_rate

                    opening = {
                        "logger": "Logger",
                        "row": "Row",
                        "barcode": "Barcode",
                        "first_tension": "First Tension [g]",
                        "first_frequency": "Tension Frequency [Hz]",
                        "first_tension_date": "First Tension date [yyyy:mm:dd]",
                        "dark_current": "Dark Current [nA]",
                        "leak_rate": "Leak Rate[mbar l/s]"
                    }

                    line = {
                        "logger": logger,
                        "row": row,
                        "barcode": barcode,
                        "first_tension": f"{tension:0.2f}",
                        "first_frequency": f"{frequency:0.2f}",
                        "first_tension_date": f"{d.strftime('%Y:%m:%d')}",
                        "dark_current": f"{dc:0.2f}",
                        "leak_rate": f"{leak}"
                    }
                    csv_lines.append(line)

            if not csv_file.exists():
                csv_file.touch()
                write_opening_line = True
            
            with csv_file.open('w+', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                if write_opening_line:
                    writer.writerow(opening)

                for line in csv_lines:
                    writer.writerow(line)

                self.status_window.setText("CSV has been created.")

    def add_tube(self):
        tube_id = self.barcode_entry.text()

        if debug:
            if tube_id == 'FILL':
                for i in range(10):
                    for j in range(10):
                        self.add_item_to_model(f"({i+1}, {j+1})")

            if tube_id == 'ADD FAKES':
                for i in range(659, 686):
                    self.add_item_to_model(f"MSU00{i}")
                for i in range(692, 720):
                    self.add_item_to_model(f"MSU00{i}")
                for i in range(749, 772):
                    self.add_item_to_model(f"MSU00{i}")
                for i in range(469, 488):
                    self.add_item_to_model(f"MSU00{i}")
                for i in range(508, 520):
                    self.add_item_to_model(f"MSU00{i}")

        try:
            t = self.database.get_tube(tube_id)
        except KeyError:
            print("KeyError has occurred. Tube cannot be found in the database")
        except AttributeError:
            print("AttributeError has occurred. Database cannot be read.")
        else:
            if t.status() == status.Status.PASS:
                self.add_item_to_model(tube_id)

            elif t.status() == status.Status.INCOMPLETE:
                print("Tube is incomplete.")
                QtWidgets.QMessageBox.warning(
                        None,
                        'Incomplete Tube',
                        "Tube is incomplete"
                )
            else:
                print("Tube has failed.")
                QtWidgets.QMessageBox.warning(
                        None,
                        'Failed Tube',
                        "Tube has a failure."
                )

        self.barcode_entry.clear()

    def get_first_tension(self, tube):
        list_of_records = tube.tension.get_record('all')
        first_record = None

        for record in list_of_records:
            if not record.fail():
                first_record = record

        if first_record is None:
            first_record = list_of_records[-1]

        return (record.tension, record.frequency, record.date)

    def create_item_model(self):
        model = QtGui.QStandardItemModel()
        model.invisibleRootItem()

        for (key, val) in self.tube_dict.items():
            item = QtGui.QStandardItem(key)
            item.setEditable(False)

            for elem in val:
                item.appendRow(QtGui.QStandardItem(elem))

            model.appendRow(item)

        return model

    def add_item_to_model(self, arg_item):
        """
        Whenever we add a tube to update, we just recreate the internal mode.
        """
        model = QtGui.QStandardItemModel()
        model.invisibleRootItem()

        for (key, val) in self.tube_dict.items():
            # if arg_item in self.tube_dict.values():
            if any(arg_item in val for val in self.tube_dict.values()):
                break

            if not val or len(val) < 10:
                self.tube_dict[key].append(arg_item)
                break

        model = self.create_item_model()
        self.tree_view.setModel(model)

    def remove(self):
        index = self.tree_view.selectedIndexes()[0]
        item = index.model().itemFromIndex(index).text()
        for (key, val) in self.tube_dict.items():
            if item in val:
                val.remove(item)
                print(val)
        self.tree_view.setModel(self.create_item_model())

    def replace(self):
        barcode = self.barcode_entry.text()
        index = self.tree_view.selectedIndexes()[0]
        item = index.model().itemFromIndex(index).text()

        for (key, val) in self.tube_dict.items():
            if item in val:
                val[val.index(item)] = barcode
        self.tree_view.setModel(self.create_item_model())


class DataView(QtWidgets.QTreeView):
    def __init__(self, database):
        super().__init__()
        self.database = database

        self.setStyleSheet("QTreeView::item { padding: 5px }")
        self.setFont(QtGui.QFont('times new roman', 10))
        # self.set
        self.setAlternatingRowColors(True)
        self.resizeColumnToContents(0)
        self.doubleClicked.connect(self.on_double_click)
        self.s = None

    def on_double_click(self, index):
        item = self.selectedIndexes()[0]
        captured_text = item.model().itemFromIndex(index).text()

        if captured_text[:3] != 'Row':
            self.s = StatusWindow(str(self.database.get_tube(captured_text)))
            self.s.show()


class StatusWindow(QtWidgets.QWidget):
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

        self.setFont(QtGui.QFont('Open Sans', 14))

    def setText(self, text_str):
        self.text_box.setText(text_str)


class CustomItem(QtGui.QStandardItem):
    def __init__(self, in_str):
        super().__init__(in_str)
        self.setEditable(False)


def main():
    add_directory_to_path()
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")

    database = db.db()

    window = MainWindow(database=database)
    window.show()

    if pyside_version == 2:
        sys.exit(app.exec_())
    elif pyside_version == 6:
        sys.exit(app.exec())

if __name__ == "__main__":
    main()
