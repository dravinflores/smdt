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
#   Updates:
#   2021-06-13, Reinhard Schwienhorst: Update database every 5 seconds
#   2021-06-24, Reinhard: Allow user to enter only 4 digits for tube ID
#
###############################################################################
#
#
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

#fp = open('errors.txt', 'a')
#fp.write(os.path.abspath(os.path.dirname(__file__)))
#fp.close()
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from sMDT import db, tube
from sMDT.data import status
import sys


# The way things are programmed here is a bit odd. We're using an abstract
# table model, but might be a bit more useful to create an abstract item model,
# and then subclass the table viewer instead. That way we could just create the
# model for a tube, and then have a viewing of tubes.
# See: < https://tinyurl.com/stackoverflow-itemmodel >.
# Add it to the todo.

class DBTableModel(QtCore.QAbstractTableModel):
    date_fmt_str = '%d %b %Y'

    # These are just baked in at the moment.
    standard_horizontal_headers = [
        "Status", "Tube ID", "Swage User", "Swage Date", "Initial Tension Date",
        "Initial Tension (g)", "Secondary Tension Date", 
        "Secondary Tension (g)", "Leak Rate (mbar L/s)", "Dark Current (nA)", 
        "Raw Length (cm)", "Swage Length (cm)"
    ]

    # These constants here are just so we can remove any None types, purely
    # for allowing the sorting of any data.
    no_value_recorded_float = 299792458.00
    no_value_recorded_date = datetime.datetime(1800, 1, 1)

    def __init__(self, data_array,db):
        super().__init__()
        self.m_data = data_array
        self.database=db
        # use a timer to update the database every 5 seconds
        timer = QtCore.QTimer(self)
        self.connect(timer, QtCore.SIGNAL("timeout()"), self.update)
        timer.start(5000)
        # remember how the data is sorted when updating the display
        self.column=3
        self.reverse=True

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
            return QtCore.Qt.AlignHCenter #+ QtCore.Qt.AlignVCenter

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
        self.column=column
        self.reverse=True
        self.layoutAboutToBeChanged.emit()
        self.m_data = sorted(self.m_data, key=operator.itemgetter(column),reverse=self.reverse)
        if order == QtCore.Qt.DescendingOrder:
            self.m_data.reverse()
            self.reverse=False
        self.layoutChanged.emit()

    def rowCount(self, index):
        return len(self.m_data)

    def columnCount(self, index):
        return len(self.m_data[0])

    def update(self):
        # update data first
        db.db_manager().update()
        self.layoutAboutToBeChanged.emit()
        self.m_data = db_to_display_array(self.database.db())
        self.m_data = sorted(self.m_data, key=operator.itemgetter(self.column),reverse=self.reverse)
        self.layoutChanged.emit()
        


class DBTabBar(QtWidgets.QTabWidget):
    def __init__(self, data, db):
        super().__init__()

        # Creating the widgets that will be associated with the tabs.
        self.table_view = self.setup_table_view_tab_ui()
        self.search_view = self.setup_search_view_tab_ui()
        self.graph_view = self.setup_graph_view_tab_ui()

        self.addTab(self.table_view, "Database")
        self.addTab(self.search_view, "Search")
        self.addTab(self.graph_view, "Plot")

        self.table_view.setSortingEnabled(True)

        # This part is a bit "hacky" and weird. We just put it in the tab
        # window for no other reason than it was a place to put it. Using the
        # abstract item model could offer a better organization.
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.horizontalHeader() \
            .setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.table_view.resizeColumnsToContents()
        self.table_view.setModel(DBTableModel(data,db))

        self.database = db

    def setup_table_view_tab_ui(self):
        table_view_tab = QtWidgets.QTableView()
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
        # check if it's a valid tube ID, if not try to make it into one
        try:
            self.database.db().get_tube(tube_id)
        except KeyError:
            tube_id = "MSU0"+tube_id

        self.search_view.data_spot.setText(
            # self.search_view.typable_box_widget.text()
            str(self.database.db().get_tube(tube_id))
        )

    def setup_graph_view_tab_ui(self):
        graph_view_tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        graph_view_tab.setLayout(layout)
        return graph_view_tab


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

        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        self.tab_bar = DBTabBar(data, db)
        self.setCentralWidget(self.tab_bar)


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
    # try:
    tubes = db.get_tubes()

    for tube in tubes:
        # print(tube)

        # "Status", "Tube ID", "User(s)", "Swage Date",
        # "Initial Tension Date", "Initial Tension (g)",
        # "Secondary Tension (g)", "Leak Rate", "Dark Current (nA)",
        # "Raw Length (cm)", "Swage Length (cm)"

        status = tube.status()
        tube_id = tube.get_ID()

        user_list = []

        # We need to do some special things for the users.
        for record in tube.swage.get_record('all'):
            user_list.append(record.user)

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
            tube_id = 0
        elif tube_id=="":
            tube_id = 0
        else:
            tube_id = int(tube_id[3:])
        if swage_date is None:
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
            user_list[0] if user_list else None,
            swage_date,
            initial_tension_date,
            initial_tension,
            final_tension_date,
            final_tension,
            leak_rate,
            dark_current,
            raw_length,
            swage_length
        ]
        ret_arr.append(l)

    # except Exception as e:
    # ret_arr = []
    # print(e)

    # sort by swage date and tube ID
    ret_arr=sorted(ret_arr,key = operator.itemgetter(3,1),reverse=True)
    # finally:
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


if __name__ == '__main__':
    path_str = str(Path())
    database = db
    # print(database.db().get_tube("MSU03355"))

    data_array = db_to_display_array(database.db())

    if not data_array:
        data_array = get_data_array_alt()

    # db_manager = db.db_manager()
    # db_manager.update()

    app = QtWidgets.QApplication(sys.argv)

    # No reason for this to be here. It's just here for redundancy.
    try:
        app.setStyle("Fusion")
    except:
        pass

    window = ViewDBMainWindow(data_array, database)
    window.show()
    if pyside_version == 2:
        sys.exit(app.exec_())
    elif pyside_version == 6:
        sys.exit(app.exec())
