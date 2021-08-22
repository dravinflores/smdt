###############################################################################
#   File: DatabaseViewer.py
#   Author(s): Dravin Flores, Reinhard Schwienhorst
#   Date Created: 01 June, 2021
#
#   Purpose: This program displays the database as a read-only GUI.
#
#   Known Issues:
#
#   Workarounds:
#
#   Updates:
#   2021-06-13, Reinhard Schwienhorst: Update database every 5 seconds
#   2021-06-24, Reinhard: Allow user to enter only 4 digits for tube ID
#   2021-08-22, Reinhard: Fix warnings about alignment and fonts
#
###############################################################################

pyside_version = None
try:
    from PySide6 import QtCore, QtWidgets, QtGui
    pyside_version = 6
except ImportError:
    from PySide2 import QtCore, QtWidgets, QtGui
    pyside_version = 2

from pathlib import Path
import operator
import datetime

import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from sMDT import db
from sMDT.data import status
import sys


class DataModel(QtCore.QAbstractTableModel):
    """
    This class allows for the tube data to be stored in a Qt-friendly way,
    through the view-model architecture. The model acts as the data storage,
    whereas the view displays the data to the user.
    """
    date_fmt_str = '%d %b %Y'

    # These are just baked in at the moment.
    horizontal_headers = [
        "Status", "Tube ID", "Initial Users", "Swage Date",
        "Initial Tension Date", "Initial Tension (g)",
        "Secondary Tension Date", "Secondary Tension (g)",
        "Leak Rate (mbar L/s)",
        "Dark Current (nA)"
    ]

    # These constants here are just so we can remove any None types, purely
    # for allowing the sorting of any data.
    no_value_recorded_float = 299792458.00
    no_value_recorded_date = datetime.datetime(1800, 1, 1)

    def __init__(self, data_array, database, path_str):
        super().__init__()
        self.m_data = data_array
        self.database = database
        self.path_str = path_str

        # use a timer to update the database every 5 seconds
        self.timer = QtCore.QTimer()
        # self.connect(timer, QtCore.SIGNAL("timeout()"), self.update)
        self.timer.timeout.connect(self.update)

        fifteen_seconds = 15 * 1000

        self.timer.start(fifteen_seconds)

        # remember how the data is sorted when updating the display
        self.column = 3
        self.reverse = True

    def data(self, index, role):
        val = self.m_data[index.row()][index.column()]

        # For the data we want to print to the screen.
        if role == QtCore.Qt.DisplayRole:
            # First we want to check for any unrecorded values and alert
            # the user.
            unrecorded_str = "-- NO RECORD --"

            if isinstance(val, float) and \
                    val == DataModel.no_value_recorded_float:
                return unrecorded_str

            if isinstance(val, datetime.datetime) and \
                    val == DataModel.no_value_recorded_date:
                return unrecorded_str

            if isinstance(val, datetime.datetime):
                return val.strftime(DataModel.date_fmt_str)
            elif isinstance(val, float):
                return f"{val:0.2f}"
            elif isinstance(val, status.Status):
                if val == status.Status.FAIL:
                    return "FAIL"
                elif val == status.Status.PASS:
                    return "PASS"
                else:
                    return "INCOMPLETE"
            else:
                # What else are we going to catch? Integers?
                return str(val)

        if role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter

        if role == QtCore.Qt.ForegroundRole:
            # Here we can control the text color itself.
            '''
            if isinstance(val, string):
                return QtGui.QColor('grey')
            '''

        if role == QtCore.Qt.BackgroundRole:
            # Here we can control the background color itself.
            if isinstance(val, status.Status):
                if val == status.Status.FAIL:
                    return QtGui.QColor('red')
                elif val == status.Status.PASS:
                    return QtGui.QColor('green')
                else:
                    return QtGui.QColor('orange')
            else:
                pass

    def headerData(self, column, orientation, role):
        # We want to have named columns.
        if (role, orientation) == (QtCore.Qt.DisplayRole, QtCore.Qt.Horizontal):
            return DataModel.horizontal_headers[column]

        # This is just so we can have numbered rows.
        if (role, orientation) == (QtCore.Qt.DisplayRole, QtCore.Qt.Vertical):
            return column + 1

    def sort(self, column, order):
        self.column = column
        self.reverse = True
        self.layoutAboutToBeChanged.emit()

        self.m_data = sorted(
            self.m_data,
            key=operator.itemgetter(column),
            reverse=self.reverse
        )

        if order == QtCore.Qt.DescendingOrder:
            self.m_data.reverse()
            self.reverse = False

        self.layoutChanged.emit()

    def rowCount(self, index):
        return len(self.m_data)

    def columnCount(self, index):
        return len(self.m_data[0])

    def update(self):
        self.layoutAboutToBeChanged.emit()
        self.database = get_new_database(self.path_str)
        self.m_data = db_to_display_array(self.database)

        self.m_data = sorted(
            self.m_data,
            key=operator.itemgetter(self.column),
            reverse=self.reverse
        )

        self.layoutChanged.emit()


class DataView(QtWidgets.QTableView):
    """
    This class displays a model to the user.
    """

    def __init__(self):
        super().__init__()

        # This is for controlling the number of windows we have

        self.w = None
        self.window_list = []

        self.setAlternatingRowColors(True)

        self.doubleClicked.connect(self.on_double_click)

    def on_double_click(self, index):
        clicked_on_barcode = False
        clicked_on_names = False

        if index.column() == 1:
            clicked_on_barcode = True
        elif index.column() == 2:
            clicked_on_names = True

        if clicked_on_barcode:
            tube_id = self.convert_to_barcode(index.data())
            data_str = str(self.model().database.get_tube(tube_id))
        elif clicked_on_names:
            # We need to get the digits for the barcode
            digits = self.model().index(index.row(), 1).data()
            tube_id = self.convert_to_barcode(digits)
            tube = self.model().database.get_tube(tube_id)

            swage_user_list = []
            tension_user_list = []
            leak_user_list = []
            dark_current_user_list = []

            # We need to do some special things for the users.
            for record in tube.swage.get_record('all'):
                swage_user_list.append(record.user)
            for record in tube.tension.get_record('all'):
                tension_user_list.append(record.user)
            for record in tube.leak.get_record('all'):
                leak_user_list.append(record.user)
            for record in tube.dark_current.get_record('all'):
                dark_current_user_list.append(record.user)

            # We only want unique users.
            swage_user_list = list(set(swage_user_list))
            tension_user_list = list(set(tension_user_list))
            leak_user_list = list(set(leak_user_list))
            dark_current_user_list = list(set(dark_current_user_list))
            data_str = "List of users:\n"

            data_str += "\tSwage Users:\n"
            for name in swage_user_list:
                if name is not None:
                    data_str += '\t\t' + name + '\n'

            data_str += "\tTension Users:\n"
            for name in tension_user_list:
                if name is not None:
                    data_str += '\t\t' + name + '\n'

            data_str += "\tLeak Users:\n"
            for name in leak_user_list:
                if name is not None:
                    data_str += '\t\t' + name + '\n'

            data_str += "\tDark Current Users:\n"
            for name in dark_current_user_list:
                if name is not None:
                    data_str += '\t\t' + name + '\n'
        else:
            return

        self.show_new_window(data_str)

    def convert_to_barcode(self, tube_id):
        id_str = str(tube_id)
        ret_str = ''

        if len(id_str) == 1:
            ret_str = "MSU0000" + id_str
        elif len(id_str) == 2:
            ret_str = "MSU000" + id_str
        elif len(id_str) == 3:
            ret_str = "MSU00" + id_str
        elif len(id_str) == 4:
            ret_str = "MSU0" + id_str
        elif len(id_str) == 5:
            ret_str = "MSU" + id_str

        return ret_str

    def show_new_window(self, data_str):
        # print(self.window_list)
        w = TubeDataWindow(data_str)
        self.clean_windows_list()
        self.window_list.append(w)
        self.window_list[-1].show()

    def clean_windows_list(self):
        new_window_set = set()
        for window in self.window_list:
            if window.isVisible():
                new_window_set.add(window)
            else:
                window.close()
        self.window_list = list(new_window_set)


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

        self.setFont(QtGui.QFont('Arial', 14))

    def setText(self, text_str):
        self.text_box.setText(text_str)


class TabbedWindow(QtWidgets.QTabWidget):
    """
    This widget allows for different "context" windows to be displayed, and
    selected using a tab selector.
    """

    def __init__(self, data, database, path_str):
        super().__init__()

        self.database = database

        # Creating the widgets that will be associated with the tabs.
        self.table_view = self.setup_table_view_tab()
        self.search_view = self.setup_search_view_tab()
        self.plot_view = self.setup_plot_tab()
        self.manual_data_entry = self.setup_manual_data_entry_tab()

        self.addTab(self.table_view, "Database")
        self.addTab(self.search_view, "Search")
        self.addTab(self.plot_view, "Plot")
        self.addTab(self.manual_data_entry, "Add Data")

        self.data_model = DataModel(data, database, path_str)

        self.table_view.setSortingEnabled(True)
        self.table_view.setModel(self.data_model)

    def setup_table_view_tab(self):
        table_view_tab = DataView()
        layout = QtWidgets.QVBoxLayout()
        table_view_tab.setLayout(layout)

        table_view_tab.horizontalHeader().setStretchLastSection(True)

        stretch = QtWidgets.QHeaderView.Stretch
        table_view_tab.horizontalHeader().setSectionResizeMode(stretch)

        table_view_tab.resizeColumnsToContents()

        return table_view_tab

    def setup_search_view_tab(self):
        search_view_tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        search_view_tab.mutable_text_box = QtWidgets.QLineEdit()
        search_view_tab.mutable_text_box.setMaxLength(15)

        prompt = "Type in tube ID and press enter"

        search_view_tab.mutable_text_box.setPlaceholderText(prompt)
        search_view_tab.mutable_text_box.returnPressed.connect(self.typed_text)

        search_view_tab.data_spot = TubeDataWindow()

        layout.addWidget(search_view_tab.mutable_text_box)
        layout.addWidget(search_view_tab.data_spot)

        layout.insertSpacing(0, 15)
        layout.addStretch()

        search_view_tab.setLayout(layout)
        return search_view_tab

    def typed_text(self):
        tube_id = self.search_view.mutable_text_box.text()
        # check if it's a valid tube ID, if not try to make it into one
        try:
            self.database.get_tube(tube_id)
        except KeyError:
            tube_id = "MSU0" + tube_id

        self.search_view.data_spot.setText(
            str(self.database.get_tube(tube_id))
        )

    def setup_plot_tab(self):
        graph_view_tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        graph_view_tab.setLayout(layout)
        return graph_view_tab

    def setup_manual_data_entry_tab(self):
        manual_data_entry_tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        manual_data_entry_tab.setLayout(layout)

        # We need a text entry box for the barcode.
        self.tube_id_text_box = QtWidgets.QWidget()
        tube_id_text_box_layout = QtWidgets.QFormLayout()
        tube_id_text_box_layout.addRow("Tube ID:", QtWidgets.QLineEdit())
        self.tube_id_text_box.setLayout(tube_id_text_box_layout)

        # The way we're going to switch from entering data between the
        # stations is by a combo box.
        self.station_select_combo = QtWidgets.QComboBox()
        self.station_select_combo.addItems([
            "Swage", "Tension", "Leak", "Dark Current"
        ])
        self.station_select_combo.activated.connect(self.switch_page)

        # We want to only show one station's data entry at a time
        self.stacked_layout = QtWidgets.QStackedLayout()

        # Here is the swage station's data entry page.
        swage_data_page = QtWidgets.QWidget()
        swage_data_page_layout = QtWidgets.QFormLayout()
        swage_data_page_layout.addRow("Raw Length:", QtWidgets.QLineEdit())
        swage_data_page_layout.addRow("Swage Length:", QtWidgets.QLineEdit())
        swage_data_page.setLayout(swage_data_page_layout)
        self.stacked_layout.addWidget(swage_data_page)

        # Here is the tension station's data entry page.
        tension_data_page = QtWidgets.QWidget()
        tension_data_page_layout = QtWidgets.QFormLayout()
        tension_data_page_layout.addRow("Tension: ", QtWidgets.QLineEdit())
        tension_data_page_layout.addRow("Frequency: ", QtWidgets.QLineEdit())
        tension_data_page.setLayout(tension_data_page_layout)
        self.stacked_layout.addWidget(tension_data_page)

        # Here is the leak station's data entry page.
        leak_data_page = QtWidgets.QWidget()
        leak_data_page_layout = QtWidgets.QFormLayout()
        leak_data_page_layout.addRow("Leak Rate:", QtWidgets.QLineEdit())
        leak_data_page.setLayout(leak_data_page_layout)
        self.stacked_layout.addWidget(leak_data_page)

        # Here is the dark current's data entry page.
        dark_current_data_page = QtWidgets.QWidget()
        dark_current_data_page_layout = QtWidgets.QFormLayout()
        dark_current_data_page_layout.addRow("Current:", QtWidgets.QLineEdit())
        dark_current_data_page_layout.addRow("Voltage:", QtWidgets.QLineEdit())
        dark_current_data_page.setLayout(dark_current_data_page_layout)
        self.stacked_layout.addWidget(dark_current_data_page)

        layout.addWidget(self.tube_id_text_box)
        layout.addWidget(self.station_select_combo)
        layout.addLayout(self.stacked_layout)
        manual_data_entry_tab.setLayout(layout)

        return manual_data_entry_tab

    @QtCore.Slot()
    def switch_page(self):
        self.stacked_layout.setCurrentIndex(
            self.station_select_combo.currentIndex()
        )


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, data, database, path_str):
        super().__init__()

        self.title = "Database Viewer"
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 600

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        self.tabbed_window = TabbedWindow(data, database, path_str)
        self.setCentralWidget(self.tabbed_window)


def get_tension_measurement(list_of_records, type, mode):
    date_set_without_times = set()
    for record in list_of_records:
        date_set_without_times.add(record.date.date())

    if type == 'initial':
        # The oldest date is the smallest.
        date = min(date_set_without_times)
    elif type == 'final':
        date = max(date_set_without_times)
    else:
        date = DataModel.no_value_recorded_date

    ret_date = DataModel.no_value_recorded_date
    ret_tens = DataModel.no_value_recorded_float

    if mode == 'last':
        l = []
        for record in list_of_records:
            if record.date.date() == date:
                l.append(record)

        ret_date = l[-1].date
        ret_tens = l[-1].tension

    if mode == 'first passing':
        for record in list_of_records:
            if record.date.date() == date and not record.fail():
                ret_date = record.date
                ret_measurement = record.tension
                break

    if mode == 'last passing':
        l = []
        for record in list_of_records:
            if record.date.date() == date and not record.fail():
                l.append(record)

        ret_date = l[-1].date
        ret_tens = l[-1].tension

    return (ret_date, ret_tens)


def db_to_display_array(database):
    ret_arr = []
    tubes = database.get_tubes()

    for tube in tubes:
        try:
            status = tube.status()
            tube_id = tube.get_ID()

            try:
                first_swage_user = tube.swage.get_record('first').user[:3]
            except:
                first_swage_user = '---'

            try:
                first_tension_user = tube.tension.get_record('first').user[:3]
            except:
                first_tension_user = '---'

            try:
                first_leak_user = tube.leak.get_record('first').user[:3]
            except:
                first_leak_user = '---'

            try:
                first_current_user = \
                    tube.dark_current.get_record('first').user[:3]
            except:
                first_current_user = '---'

            user_str = first_swage_user + ' | ' \
                       + first_tension_user + ' | ' \
                       + first_leak_user + ' | ' \
                       + first_current_user

            user_str = user_str.upper()

            try:
                swage_date = tube.swage.get_record('last').date
            except IndexError:
                swage_date = DataModel.no_value_recorded_date

            try:
                (initial_tension_date, initial_tension) = \
                    get_tension_measurement(
                        tube.tension.get_record('all'),
                        'initial',
                        'last'
                    )
            except ValueError:
                (initial_tension_date, initial_tension) = (
                    DataModel.no_value_recorded_date,
                    DataModel.no_value_recorded_float
                )

            try:
                (final_tension_date, final_tension) = \
                    get_tension_measurement(
                        tube.tension.get_record('all'),
                        'final',
                        'last'
                    )
            except ValueError:
                (final_tension_date, final_tension) = (
                    DataModel.no_value_recorded_date,
                    DataModel.no_value_recorded_float
                )

            try:
                leak_rate = tube.leak.get_record().leak_rate
            except IndexError:
                leak_rate = DataModel.no_value_recorded_float
            try:
                dark_current = tube.dark_current.get_record().dark_current
            except IndexError:
                dark_current = DataModel.no_value_recorded_float

            if tube_id is None:
                tube_id = 0
            elif tube_id == "":
                tube_id = 0
            else:
                try:
                    tube_id = int(tube_id[3:])
                except ValueError:
                    tube_id = 0

            if swage_date is None:
                swage_date = DataModel.no_value_recorded_date
            elif initial_tension_date is None:
                initial_tension_date = DataModel.no_value_recorded_date
            elif initial_tension is None:
                initial_tension = DataModel.no_value_recorded_float
            elif final_tension_date is None:
                final_tension_date = DataModel.no_value_recorded_date
            elif final_tension is None:
                final_tension = DataModel.no_value_recorded_float
            elif leak_rate is None:
                leak_rate = DataModel.no_value_recorded_float
            elif dark_current is None:
                dark_current = DataModel.no_value_recorded_float
            else:
                pass

            l = [
                status,
                tube_id,
                user_str,
                swage_date,
                initial_tension_date,
                initial_tension,
                final_tension_date,
                final_tension,
                leak_rate,
                dark_current,
            ]
            ret_arr.append(l)

        except AttributeError:
            # We have found that something about the tube is not right.
            # We can't display the tube.
            pass

    # sort by swage date and tube ID
    ret_arr = sorted(ret_arr, key=operator.itemgetter(3, 1), reverse=True)
    return ret_arr


def get_data_array_alt():
    data_array = []

    n_cols = 11
    n_rows = 50

    for i in range(n_rows):
        arr = []
        for j in range(n_cols):
            arr.append(i + j)
        data_array.append(arr)

    return data_array


def get_new_database(path_str=None):
    if path_str is None:
        database = db.db()
    else:
        database = db.db(path_str)
    return database


def main():
    # We want to get the file name from the command line.

    try:
        path_str = str(Path(sys.argv[1]))
    except:
        path_str = None

    database = get_new_database(path_str)
    data_array = db_to_display_array(database)

    if not data_array:
        data_array = get_data_array_alt()

    app = QtWidgets.QApplication(sys.argv)

    app.setStyle("fusion")

    window = MainWindow(data_array, database, path_str)
    window.show()

    if pyside_version == 2:
        sys.exit(app.exec_())
    elif pyside_version == 6:
        sys.exit(app.exec())


if __name__ == '__main__':
    main()
