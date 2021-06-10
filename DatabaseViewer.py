###############################################################################
#   File: DatabaseViewer.py
#   Author(s): Dravin Flores
#   Date Created: 01 June, 2021
#
#   Purpose: This program displays the database as a read-only GUI.
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################

from typing import final
from PySide6 import QtCore, QtWidgets, QtGui
import operator
import datetime
import threading

from sMDT import db, tube
from sMDT.data import status
import sys


def sort_by_most_recent_date(data_array):
    '''
    We want to, by default, sort the tubes by the most recent date. So any
    where we have a passed in data array, we will want to sort it.
    '''

    # If the underlying data structure has changed, then we will need to 
    # adjust the lambda. Clearly this would be a key error.
    if type(data_array[0][6]) != type(DBTableModel.no_value_recorded_date):
        raise KeyError
    else:
        return sorted(data_array, key=lambda data : data[6], reverse=True)


class DBTableModel(QtCore.QAbstractTableModel):
    """
    This class controls how the tube data will be modeled in Qt. This is the 
    class that has 'access' to the data. Any Qt class that shows data will do
    so according to this class.
    """

    date_fmt_str = '%d %b %Y'

    standard_horizontal_headers = [
        "Status", "Tube ID", "Swage User", "Tension User", "Leak User",
        "Dark Current User", "Swage Date", 
        # "Initial Tension Date", 
        # "Initial Tension (g)", 
        "Recent Tension Date", 
        "Recent Tension (g)", "Leak Rate (mbar L/s)", "Dark Current (nA)"
    ]

    # These constants here are just so we can remove any None types, purely
    # for allowing the sorting of any data.
    no_value_recorded_float = 299792458.00
    no_value_recorded_date = datetime.datetime(1800, 1, 1)

    def __init__(self, data_array):
        super().__init__()
        # self.m_data = data_array
        self.m_data = sort_by_most_recent_date(data_array)

    def data(self, index, role):
        val = self.m_data[index.row()][index.column()]

        if role == QtCore.Qt.DisplayRole:
            # Rather than passing in strings, let's go ahead and just convert
            # here. We'll also catch the ability to get constants.
            if isinstance(val, float) and \
                    val == DBTableModel.no_value_recorded_float:
                return ""

            if isinstance(val, datetime.datetime) and \
                    val == DBTableModel.no_value_recorded_date:
                return ""

            if isinstance(val, datetime.datetime):
                return val.strftime(DBTableModel.date_fmt_str)
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
            return QtCore.Qt.AlignHCenter + QtCore.Qt.AlignVCenter

        if role == QtCore.Qt.ForegroundRole:
            # Here we can control the text color itself.
            '''
            if isinstance(val, float):
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
            return DBTableModel.standard_horizontal_headers[column]

        # This is just so we can have numbered rows.
        if (role, orientation) == (QtCore.Qt.DisplayRole, QtCore.Qt.Vertical):
            return column + 1

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        self.m_data = sorted(self.m_data, key=operator.itemgetter(column))

        if order == QtCore.Qt.DescendingOrder:
            self.m_data.reverse()

        self.layoutChanged.emit()

    def rowCount(self, index):
        return len(self.m_data)

    def columnCount(self, index):
        return len(self.m_data[0])

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled \
            | QtCore.Qt.ItemIsEditable \
            | QtCore.Qt.ItemIsSelectable

    def refresh(self, new_data):
        self.layoutAboutToBeChanged.emit()
        self.m_data = sort_by_most_recent_date(new_data)
        self.layoutChanged.emit()


class DBTableView(QtWidgets.QTableView):
    """
    This class controls how the tube data will be viewed, in which case the 
    table view is chosen so that the data can be arranged in a spreadsheet-like
    manner.
    """
    def __init__(self):
        super().__init__()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timeout)
        self.timer.setInterval(
            QtGui.QGuiApplication.styleHints().mouseDoubleClickInterval()
        )
        self.timer.setSingleShot(True)
        self.setAlternatingRowColors(True)
        # self.setGridStyle(QtCore.Qt.PenStyle.NoPen)
        self.setShowGrid(False)
        self.setCornerButtonEnabled(True)
        # self.setCornerButtonEnabled(True)
        self.resizeRowsToContents()
        self.setWordWrap(True)


    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        self.open_single_tube_data()

    def timeout(self):
        self.custom_clicked.emit(self.index)

    @QtCore.Slot()
    def open_single_tube_data(self):
        print("Hello")


class DBTubeDataFloatingWindow(QtWidgets.QWidget):
    """
    This class allows for any tube barcode to be double clicked, which will
    spawn a floating window which has all the data.
    """
    def __init__(self, tube):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        self.setWindowTitle(f"Data for {tube.get_ID()}")
        self.data = QtWidgets.QLabel(str(tube))
        layout.addWidget(self.data)
        self.setLayout(layout)


class DBTabBar(QtWidgets.QTabWidget):
    """
    This class allows for the ability to switch between the table of tubes 
    window and the search window. 
    """
    def __init__(self, data, db):
        super().__init__()

        # Creating the widgets that will be associated with the tabs.
        self.table_view = self.setup_table_view_tab_ui()
        self.search_view = self.setup_search_view_tab_ui()

        self.addTab(self.table_view, "Database")
        self.addTab(self.search_view, "Search")

        self.table_view.setSortingEnabled(True)

        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.horizontalHeader() \
            .setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.table_view.resizeColumnsToContents()
        self.table_view.setModel(DBTableModel(data))

        self.database = db

    def setup_table_view_tab_ui(self):
        # table_view_tab = QtWidgets.QTableView()
        table_view_tab = DBTableView()
        layout = QtWidgets.QVBoxLayout()

        table_view_tab.setLayout(layout)
        return table_view_tab

    def setup_search_view_tab_ui(self):
        # We need to actually create a few layouts, like the top_layout,
        # right_side_layout, left_side_layout, and the bottom_layout.

        search_view_tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        search_view_tab.typable_box_widget = QtWidgets.QLineEdit()
        search_view_tab.typable_box_widget.setMaxLength(15)

        prompt = "Type in tube ID and press enter"

        search_view_tab.typable_box_widget.setPlaceholderText(prompt)
        search_view_tab.typable_box_widget.returnPressed.connect(
            self.typed_text
        )

        search_view_tab.data_spot = QtWidgets.QLabel()

        layout.addWidget(search_view_tab.typable_box_widget)
        layout.addWidget(search_view_tab.data_spot)

        layout.insertSpacing(0, 15)
        layout.addStretch()

        search_view_tab.setLayout(layout)
        return search_view_tab

    def typed_text(self):
        tube_id = self.search_view.typable_box_widget.text()
        self.search_view.data_spot.setText(
            # self.search_view.typable_box_widget.text()
            str(self.database.get_tube(tube_id))
        )

    def setup_graph_view_tab_ui(self):
        graph_view_tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        graph_view_tab.setLayout(layout)
        return graph_view_tab

    def call_for_refresh(self):
        self.database = get_current_database()

        # Testing purposes only
        '''
        self.db_manager = db.db_manager(testing=True)
        a_new_tube = tube.Tube()
        a_new_tube.m_tube_id = ''
        self.database.add_tube(a_new_tube)
        self.db_manager.update()
        '''

        data = db_to_display_array(self.database)
        self.table_view.setModel(DBTableModel(data))

        # self.database.delete_tube('')


class ViewDBMainWindow(QtWidgets.QMainWindow):
    def __init__(self, data, db):
        super().__init__()

        self.title = "Database Viewer"
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 600

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.timer = QtCore.QTimer()
        self.timer.start(1000)

        main_layout = QtWidgets.QVBoxLayout()
        self.tab_bar = DBTabBar(data, db)
        self.setLayout(main_layout)
        self.setCentralWidget(self.tab_bar)

        toolbar = QtWidgets.QToolBar()
        self.addToolBar(toolbar)

        button_action = QtGui.QAction("Refresh", self)
        button_action.setStatusTip("Click to refresh the database")
        button_action.triggered.connect(self.refresh_data)
        toolbar.addAction(button_action)

        self.setStatusBar(QtWidgets.QStatusBar(self))

    def refresh_data(self):
        self.tab_bar.call_for_refresh()

    def toggle_window(self, window):
        if window.isVisible():
            window.hide()
        else:
            window.show()


# We're returning a tuple, corresponding to the following format:
# (date, measurement).
def get_measurement(list_of_records, type):
    date_set_without_times = set()
    for record in list_of_records:
        date_set_without_times.add(record.date.date())

    if type == 'initial':
        # The oldest date is the smallest.
        date = min(date_set_without_times)
    elif type == 'final':
        date = max(date_set_without_times)
    else:
        date = DBTableModel.no_value_recorded_date

    ret_date = DBTableModel.no_value_recorded_date
    ret_measurement = DBTableModel.no_value_recorded_float

    # Now we want the data that corresponds to the first passing measurement.
    for record in list_of_records:
        if (record.date.date() == date) and (not record.fail()):
            ret_date = record.date
            ret_measurement = record.tension
            break

    return (ret_date, ret_measurement)



def db_to_display_array(db):
    ret_arr = []
    tubes = db.get_tubes()

    for tube in tubes:
        status = tube.status()
        tube_id = tube.get_ID()

        last_swage_user = ''
        last_tension_user = ''
        last_leak_user = ''
        last_current_user = ''

        try:
            last_swage_user = tube.swage.get_record('last').user
        except IndexError:
            pass

        try:
            last_tension_user = tube.tension.get_record('last').user
        except IndexError:
            pass

        try:
            last_leak_user = tube.leak.get_record('last').user
        except IndexError:
            pass

        try:
            last_current_user = tube.dark_current.get_record('last').user
        except IndexError:
            pass

        try:
            swage_date = tube.swage.get_record('last').date
        except IndexError:
            swage_date = DBTableModel.no_value_recorded_date

        try:
            (initial_tension_date, initial_tension) = \
                get_measurement(tube.tension.get_record('all'), 'initial')
        except ValueError:
            (initial_tension_date, initial_tension) = (
                    DBTableModel.no_value_recorded_date, 
                    DBTableModel.no_value_recorded_float
                )

        try:
            (final_tension_date, final_tension) = \
                get_measurement(tube.tension.get_record('all'), 'final')
        except ValueError:
            (final_tension_date, final_tension) = (
                    DBTableModel.no_value_recorded_date, 
                    DBTableModel.no_value_recorded_float
                )

        try:
            leak_rate = tube.leak.get_record().leak_rate
        except IndexError:
            leak_rate = DBTableModel.no_value_recorded_float

        try:
            dark_current = tube.dark_current.get_record().dark_current
        except IndexError:
            dark_current = DBTableModel.no_value_recorded_float

        try:
            raw_length = tube.swage.get_record().raw_length
        except IndexError:
            raw_length = DBTableModel.no_value_recorded_float

        try:
            swage_length = tube.swage.get_record().swage_length
        except IndexError:
            swage_length = DBTableModel.no_value_recorded_float

        if tube_id is None:
            tube_id = ""
        elif swage_date is None:
            swage_date = DBTableModel.no_value_recorded_date
        elif initial_tension_date is None:
            initial_tension_date = DBTableModel.no_value_recorded_date
        elif initial_tension is None:
            initial_tension = DBTableModel.no_value_recorded_float
        elif final_tension_date is None:
            final_tension_date = DBTableModel.no_value_recorded_date
        elif final_tension is None:
            final_tension = DBTableModel.no_value_recorded_float
        elif leak_rate is None:
            leak_rate = DBTableModel.no_value_recorded_float
        elif dark_current is None:
            dark_current = DBTableModel.no_value_recorded_float
        elif raw_length is None:
            raw_length = DBTableModel.no_value_recorded_float
        elif swage_length is None:
            swage_length = DBTableModel.no_value_recorded_float
        else:
            pass

        

        l = [
            status,
            tube_id,
            last_swage_user,
            last_tension_user,
            last_leak_user,
            last_current_user,
            swage_date,
            # initial_tension_date,
            # initial_tension,
            final_tension_date,
            final_tension,
            leak_rate,
            dark_current,
        ]
        ret_arr.append(l)

    return ret_arr


def get_data_array_alt():
    data_array = []

    n_cols = 11
    n_rows = 50

    for i in range(n_rows):
        arr = []
        for j in range(n_cols):
            arr.append(j)
        data_array.append(arr)

    return data_array


def get_current_database():
    return db.db()


if __name__ == '__main__':
    database = get_current_database()
    data_array = db_to_display_array(database)

    if not data_array:
        data_array = get_data_array_alt()

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    window = ViewDBMainWindow(data_array, database)
    window.show()
    sys.exit(app.exec())
