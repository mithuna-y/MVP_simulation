from functools import partial
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from scipy.integrate import quad

# speed of light
c = 10


# Define the parameters of the wave packet
sigma = 1
k_0 = 1
frequency = 1
angular_frequency = 2 * np.pi * frequency
x_0 = -c * 5

# material properties
material_constant = 5
resonant_angular_frequency = 0.1 * 2 * np.pi
number_of_slices = 10

# time
t = np.linspace(0, 10, 100)


# dot moving at speed c


# Define the wave packet
def wave_packet(x, t):
    return (2 * np.pi * sigma ** 2) ** (-1 / 4) * np.exp(
        -((x - x_0 - c * t) ** 2) / (4 * sigma ** 2 * t ** 2 + 0.01) + 1j * (k_0 * (x - c * t) - angular_frequency * t))


def wave_packet_fourier(x, t):
    global x_range
    L = x_range
    n = 50
    t0 = 5
    fc = lambda x: wave_packet(x, t0) * np.cos(index * np.pi * x / L)
    fs = lambda x: wave_packet(x, t0) * np.sin(index * np.pi * x / L)

    sum = quad(partial(wave_packet, t=t0), -L, L)[0] * (1.0 / L)

    for index in range(1, n + 1):
        an = quad(fc, -L, L)[0] * (1.0 / L)
        bn = quad(fs, -L, L)[0] * (1.0 / L)
        sum += an * np.cos(index * np.pi * x / L - (c * index * np.pi / L) * t) + bn * np.sin(
            index * np.pi * x / L - (c * index * np.pi / L) * t)

    return sum


def initial_wave_packet(x):
    t0 = 5
    return wave_packet(x, t0)


# find the fourier components of a function(x)
def cos_fourier_component(function, index):
    global x_range
    L = x_range

    def fc(x):
        return function(x) * np.cos(index * np.pi * x / L)

    return quad(fc, -L, L)[0] * (1.0 / L)


def sin_fourier_component(function, index):
    global x_range
    L = x_range

    def fs(x):
        return function(x) * np.sin(index * np.pi * x / L)

    return quad(fs, -L, L)[0] * (1.0 / L)

def fourier_wave_packet(x, t, number_of_slices, slice_number):
    global x_range
    L = x_range
    n = 50
    sum = 0
    slice_width = (x_range / 2) / number_of_slices
    for index in range(1, n + 1):
        an = cos_fourier_component(initial_wave_packet, index)
        bn = sin_fourier_component(initial_wave_packet, index)
        angular_frequency = c * index * np.pi / L
        phase = material_constant * (slice_number+1) * angular_frequency / (
                resonant_angular_frequency ** 2 - angular_frequency ** 2 + 0.012) * slice_width / c
        sum += an * np.cos(index * np.pi * x / L - (c * index * np.pi / L) * t + phase) + bn * np.sin(
            index * np.pi * x / L - (c * index * np.pi / L) * t)
    return sum




fig, ax = plt.subplots()
lines = []
for i in range(number_of_slices + 1):
    line, = ax.plot([], [], color="blue")
    lines.append(line)

x_range = 100
ax.set_xlim(0, x_range)
ax.set_ylim(-1.0, 1.0)



def init():
    for line in lines:
        line.set_data([], [])
    return lines


def update(frame):
    # wave in the slices of material
    slice_width = (x_range / 2) / number_of_slices
    for slice_number, line in enumerate(lines):
        if slice_number == number_of_slices:
            x_start = 0
            x_end = int(x_range / 2)
            x = np.linspace(x_start, x_end, 100)
            y = wave_packet_fourier(x, frame)
            line.set_data(x, y)
        else:
            x_start = (x_range / 2) + slice_number * slice_width
            x_end = (x_range / 2) + (slice_number + 1) * slice_width
            x = np.linspace(x_start, x_end, 20)
            y = fourier_wave_packet(x, frame, number_of_slices, slice_number)
            line.set_data(x, y)

    return lines


ani = FuncAnimation(fig, update, frames=100, init_func=init, blit=True)
plt.show()
