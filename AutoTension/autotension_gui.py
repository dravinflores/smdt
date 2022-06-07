#
# Updated tensioner program to work with the motorized tension setup
# Paul Johnecheck
# April 2022
#
#
# Modifications:
# 2022-06, Reinhard: separate 400 and 320 tensioning, new target for 320 is 325
#
import sys
import os
import datetime

pyside_version = None
try:
    from PySide6 import QtCore, QtWidgets, QtGui
    from PySide6.QtWidgets import QMessageBox
    pyside_version = 6
except ImportError:
    from PySide2 import QtCore, QtWidgets, QtGui
    from PySide2.QtWidgets import QMessageBox
    pyside_version = 2

from stepper import Stepper, Plotter
from freq_tension import FourierTension

DROPBOX_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(DROPBOX_DIR)

from sMDT import db, tube
from sMDT.data.tension import Tension, TensionRecord


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.plot_title = "Tension v. Time"
        self.plot_x_label = "Time (s)"
        self.plot_y_label = "Tension (g)"

        self.db = db.db()

        self.setWindowTitle("AutoTension")

        layout1 = QtWidgets.QHBoxLayout()

        layout2 = QtWidgets.QVBoxLayout()
        layout3 = QtWidgets.QVBoxLayout()

        layout1.addLayout(layout2)
        layout1.addLayout(layout3)

        self.user_edit = QtWidgets.QLineEdit()
        self.ID_edit = QtWidgets.QLineEdit()
        self.ID_edit.returnPressed.connect(self.retension)
        self.ext_tension = QtWidgets.QLineEdit()
        self.ext_tension.setReadOnly(True)
        self.ext_tension.setText("Not yet measured")
        self.ext_tension.setStyleSheet('background-color: lightgrey; color: black')
        self.int_tension = QtWidgets.QLineEdit()
        self.int_tension.setReadOnly(True)
        self.int_tension.setText("Not yet measured")
        self.int_tension.setStyleSheet('background-color: lightgrey; color: black')

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Name", self.user_edit)
        form_layout.addRow("ID", self.ID_edit)
        form_layout.addRow("External Sensor Tension", self.ext_tension)
        form_layout.addRow("Internal Frequency Magnet Tension", self.int_tension)

        layout2.addLayout(form_layout)

        layout4 = QtWidgets.QHBoxLayout()
        self.first_tension_button = QtWidgets.QPushButton()
        self.first_tension_button.setText("Over-tension only (400)")
        layout4.addWidget(self.first_tension_button)

        self.release_button = QtWidgets.QPushButton()
        self.release_button.setText("Release tension (0)")
        layout4.addWidget(self.release_button)

        self.retension_button = QtWidgets.QPushButton()
        self.retension_button.setText("Final tension only (320)")
        layout4.addWidget(self.retension_button)

        self.get_tension_button = QtWidgets.QPushButton()
        self.get_tension_button.setText("Get tension")
        layout4.addWidget(self.get_tension_button)

        layout2.addLayout(layout4)
        
        #layout5 = QtWidgets.QHBoxLayout()
        #self.tension_up_button = QtWidgets.QPushButton()
        #self.tension_up_button.setText("Increase Tension")
        #layout5.addWidget(self.tension_up_button)

        #self.tension_down_button = QtWidgets.QPushButton()
        #self.tension_down_button.setText("Decrease Tension")
        #layout5.addWidget(self.tension_down_button)

        #layout2.addLayout(layout5)

        #layout6 = QtWidgets.QHBoxLayout()
        #self.stop_button = QtWidgets.QPushButton()
        #self.stop_button.setText("Stop \"Tension\"")
        #layout6.addWidget(self.stop_button)

        #layout2.addLayout(layout6)

        #layout7 = QtWidgets.QHBoxLayout()
        #self.retension_button = QtWidgets.QPushButton()
        #self.retension_button.setText("Retension")
        #layout7.addWidget(self.retension_button)

        #layout2.addLayout(layout7)

        self.first_tension_button.setAutoDefault(True)

        self.first_tension_button.clicked.connect(self.first_tension)
        self.release_button.clicked.connect(self.release)
        self.retension_button.clicked.connect(self.retension)

        self.get_tension_button.clicked.connect(self.get_tension)

        #self.tension_up_button.clicked.connect(self.tension_up)

        #self.tension_down_button.clicked.connect(self.tension_down)

        #self.stop_button.clicked.connect(self.stop)

        #self.retension_button.clicked.connect(self.retension)

        label = QtWidgets.QLabel()
        label.setText("Status")
        layout2.addWidget(label)
        self.status = QtWidgets.QLineEdit()
        self.status.setReadOnly(True)
        self.status.setText("Not Started")
        self.status.setStyleSheet('background-color: lightgrey; color: black')
        layout2.addWidget(self.status)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)
        
        self.show()

    def update_ext_tension(self, tension):
        self.ext_tension.setText(str(tension))

    def update_int_tension(self, tension):
        self.int_tension.setText(str(tension))

    def update_status(self, status):
        self.status.setText(status)

    def avg(self, x):
        return sum(x)/len(x)

    #
    # function to over-tension (first tension) to 400, only over-tension, not both steps
    def first_tension(self):

        self.tension_device = FourierTension()
        n_samp = 1
        stepper = Stepper(
            noise_reduction=self.avg,
            stride=28,
            n_samp=n_samp,
            plotter=Plotter(self.plot_title, self.plot_x_label, self.plot_y_label))

        self.update_status("Tensioning to 400")
        stepper.resume()
        stepper.step_to(350, 10, callback=self.update_ext_tension)
        stride = 5
        stepper.step_to(400, 5, callback=self.update_ext_tension)
        stride = 28
        stepper.pause()
        self.update_status("Measuring internal tension")
        tension, frequency =  self.tension_device.get_tension()
        self.update_int_tension(tension)
        # save tension information to the database
        newTube = tube.Tube()
        newTube.set_ID(self.ID_edit.text().strip())
        newTube.tension.add_record(
            TensionRecord(
                tension=tension,
                frequency=frequency,
                date=datetime.datetime.now(),
                user=self.user_edit.text().strip()
                )
            )
        self.db.add_tube(newTube)
        # end of measuring internal tension and saving to database
        stepper.resume()
        self.update_status("Holding at 400")
        stepper.hold(400, 5, hold_time=4, callback=self.update_ext_tension)
        self.update_status("Tensioning to 0")
        stepper.step_to(0, 10, callback=self.update_ext_tension)


    #
    # function to release tension, to 0
    def release(self):
        n_samp = 1
        stepper = Stepper(
            noise_reduction=self.avg,
            stride=28,
            n_samp=n_samp,
            plotter=Plotter(self.plot_title, self.plot_x_label, self.plot_y_label))

        self.update_status("Releasing tension")
        stepper.resume()
        stepper.step_to(0, 10, callback=self.update_ext_tension)

        
    #
    # function to retension (final tension) to 320, only one tension, not first over-tensioning
    def retension(self):
        self.tension_device = FourierTension()
        n_samp = 1
        stepper = Stepper(
            noise_reduction=self.avg,
            stride=28,
            n_samp=n_samp,
            plotter=Plotter(self.plot_title, self.plot_x_label, self.plot_y_label))

        self.update_status("Tensioning to 322")
        stepper.resume()
        stepper.step_to(300, 10, callback=self.update_ext_tension)
        stride = 5
        stepper.step_to(322, 5, callback=self.update_ext_tension)
        stride = 28
        stepper.pause()
        self.update_status("Measuring internal tension")
        tension, frequency =  self.tension_device.get_tension()
        self.update_int_tension(tension)
        # save tension information to the database
        newTube = tube.Tube()
        newTube.set_ID(self.ID_edit.text().strip())
        newTube.tension.add_record(
            TensionRecord(
                tension=tension,
                frequency=frequency,
                date=datetime.datetime.now(),
                user=self.user_edit.text().strip()
                )
            )
        self.db.add_tube(newTube)
        # end of measuring internal tension and saving to database

        self.update_status("Holding at 322")
        stepper.hold(322, 5, hold_time=2, callback=self.update_ext_tension)

        self.update_status("Done")
        self.ID_edit.setFocus()

    def get_tension(self):
        self.tension_device = FourierTension()
        self.update_status("Measuring internal tension")
        tension, frequency =  self.tension_device.get_tension()
        self.update_int_tension(tension)
        # save tension information to the database
        newTube = tube.Tube()
        newTube.set_ID(self.ID_edit.text().strip())
        newTube.tension.add_record(
            TensionRecord(
                tension=tension,
                frequency=frequency,
                date=datetime.datetime.now(),
                user=self.user_edit.text().strip()
                )
            )
        self.db.add_tube(newTube)
        # end of measuring internal tension and saving to database
        self.update_status("Done. Internal tension is "+str(tension))
        self.ID_edit.setFocus()


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    w = MainWindow()
    if pyside_version == 2:
        sys.exit(app.exec_())
    elif pyside_version == 6:
        sys.exit(app.exec())
