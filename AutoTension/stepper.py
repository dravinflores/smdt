# Stepper program
# to operate the stepper motor for the tensioning station
# through the National Instruments device
# automatically tension to the correct tension
# and plot the progress.
#
# Modifications:
# 2022-06, Reinhard: Move high-level functionality to autotension_gui
import math

import nidaqmx
import time
import matplotlib.pyplot as plt
import numpy as np

from nidaqmx.constants import TerminalConfiguration, AcquisitionType

def V_to_g(V):
    return V * 100


class Plotter:
    def __init__(self, title, xlabel, ylabel):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.X = []
        self.Y = []
        self.time0 = time.time()
        self.i = 0

    def plot(self, Y):
        self.X.append(time.time()-self.time0)
        self.Y.append(Y)
        self.i += 1
        fig = plt.figure('Tension', figsize=(8, 4))
        fig.clf()
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.grid(True, linestyle='--')
        plt.plot(np.array(self.X), np.array(self.Y), 'r-')
        plt.tight_layout()
        plt.gcf().canvas.flush_events()
        #plt.pause(0.0001)

        #plt.show(block=False)
        plt.draw()
        plt.show(block=False)

    def clear(self):
        plt.clf()
        self.X = []
        self.Y = []
        self.i = 0

class Stepper:
    def __init__(self, ai_channel_name="Dev1/ai2", do_channel_name="Dev1/port0/line0:2", plotter=None, n_samp=200, noise_reduction=None, stride=1):
        self.read_task = nidaqmx.Task()
        self.read_task.ai_channels.add_ai_voltage_chan(ai_channel_name, terminal_config=TerminalConfiguration.RSE)
        self.read_task.start()
        self.step_task = nidaqmx.Task()
        self.step_task.do_channels.add_do_chan(do_channel_name)
        self.step_task.start()
        self.plotter = plotter
        self.n_samp = n_samp
        self.noise_reduction = noise_reduction
        self.stride = stride
        self.isPaused = False

    def __del__(self):
        self.read_task.stop()
        self.step_task.stop()

    def pause(self):
        if not self.isPaused:
            self.read_task.stop()
            self.step_task.stop()
            self.isPaused = True

    def resume(self):
        if self.isPaused:
            self.read_task.start()
            self.step_task.start()
            self.isPaused=False

    def step(self, target=320, tolerance=10):
        V = self.read_task.read(number_of_samples_per_channel=self.n_samp)
        V = self.noise_reduction(V)
        measured = V_to_g(V)
        error = target - measured
        if abs(error) > tolerance:
            if error > 0:
                for i in range(self.stride):
                    self.step_task.write(5)
                    self.step_task.write(4)
            else:
                for i in range(self.stride):
                    self.step_task.write(7)
                    self.step_task.write(6)
        return round(measured,2)

    def clear(self): self.plotter.clear()

    def step_to(self, target=320, tolerance=10, callback=None):
        done = False
        i = 0
        while not done:
            i += 1
            measured = self.step(target, tolerance)
            if self.plotter:
                self.plotter.plot(measured)
            if callback:
                callback(measured)
            if abs(target - measured) < tolerance:
                done = True
                self.hold(target, tolerance, 1, callback)
        #self.read_task.stop()
        #self.step_task.stop()

    def hold(self, target, tolerance=10, hold_time=10, callback=None):
        time0 = math.inf
        i = 0

        while (time.time() - time0) < hold_time:
            i += 1
            measured = self.step(target, tolerance)
            if self.plotter:
                self.plotter.plot(measured)
            if callback:
                callback(measured)
            if abs(target - measured) < tolerance and time0 == math.inf:
                time0 = time.time()

        #self.read_task.stop()
        #self.step_task.stop()



if __name__ == '__main__':
    with nidaqmx.Task() as read_task, nidaqmx.Task() as step_task:

        read_task.ai_channels.add_ai_voltage_chan("Dev1/ai2")
        step_task.do_channels.add_do_chan("Dev1/port0/line0:2")

        target = 1
        tolerance = 0.1

        p = Plotter("Title", "Time", "V")

        done = False
        i = 0
        while not done:
            V = read_task.read()
            error = target - V
            p.plot(i, V)
            i += 1
            if abs(error) < tolerance:
                done = True
            elif error > 0:
                step_task.write(5)
                step_task.write(4)
            else:
                step_task.write(7)
                step_task.write(6)

