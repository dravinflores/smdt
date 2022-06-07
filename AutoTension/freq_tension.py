#
# sMDT wiring station internal tension measurement
# Reads wave function from the wire at the tensioning station and then does a Fourier transform to obtain
# the frequency at which the wire is vibrating. Then convert that to wire tension.
#
import nidaqmx
import time
import pprint
from nidaqmx.constants import TerminalConfiguration, AcquisitionType
from scipy import fftpack
import numpy as np
import time

class FourierTension:
    def __init__(self,
                ai_channel_name="Dev1/ai0",
                do_channel_name="Dev1/port1/line0",
                sampling_time = 2,
                rate = 1000,
                linear_density = 38.8,
                wire_length = 1605):
        self.wvf_task = nidaqmx.Task()
        self.ctrl_task = nidaqmx.Task()
        self.wvf_task.ai_channels.add_ai_voltage_chan(ai_channel_name, min_val=-10, max_val=10, terminal_config=TerminalConfiguration.RSE)
        self.wvf_task.timing.cfg_samp_clk_timing(rate=rate, sample_mode=AcquisitionType.FINITE, samps_per_chan=sampling_time * rate)
        self.ctrl_task.do_channels.add_do_chan("Dev1/port1/line0")
        #self.wvf_task.start()
        #self.ctrl_task.start()

        self.sampling_time = sampling_time
        self.rate = rate
        self.linear_density = linear_density
        self.wire_length = wire_length

    #def __del__(self):
    #    self.wvf_task.stop()
    #    self.ctrl_task.stop()

    def get_tension(self):
        self.ctrl_task.write(False)
        time.sleep(3)
        self.ctrl_task.write(True)

        data = self.wvf_task.read(number_of_samples_per_channel=self.sampling_time * self.rate)

        X = fftpack.fft(data)

        frequency = (np.argmax(X[self.sampling_time * 10: self.sampling_time * 200]) + self.sampling_time * 10) / self.sampling_time
        tension = ((((((self.wire_length - 28) / 1000) ** 2) * (self.linear_density / 1000000)) * 4) * (frequency ** 2)) / 0.0098
        return round(tension,2), round(frequency,1)

if __name__ == "__main__":
    ft = FourierTension()
    for i in range(5):
        time.sleep(2)
        print(ft.get_tension()[0])
