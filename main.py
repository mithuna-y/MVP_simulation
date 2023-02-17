import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from scipy.integrate import quad

fig, ax = plt.subplots()

# time
t = np.linspace(0, 10, 100)

# space
x_range = 100
ax.set_xlim(0, x_range)
ax.set_ylim(-1.0, 1.0)

# speed of light
c = 2
b
# Define the parameters of the wave packet
sigma = 1
k_0 = 1
frequency = 1.8
x_0 = -c * 5 # initial position
L = x_range * 1 #period of the fourier series approx
angular_frequency = 2 * np.pi * frequency


# material properties
material_constant = 5
resonant_frequency = 1.5
resonant_angular_frequency = 2 * np.pi * resonant_frequency
number_of_slices = 3



# segments to plot
lines = []
for i in range(number_of_slices + 1):
    if i == number_of_slices:
        line, = ax.plot([], [], color="green")
        lines.append(line)
    else:
        line, = ax.plot([], [], color="blue")
        lines.append(line)

def init():
    for line in lines:
        line.set_data([], [])
    return lines

# Define the original wave packet
def initial_wavepacket(x):
    # this is a delta function at "t=0" so let's use the function a bit after that
    t = 5
    return (2 * np.pi * sigma ** 2) ** (-1 / 4) * np.exp(
        -((x - x_0 - c * t) ** 2) / (4 * sigma ** 2 * t ** 2 + 0.01) + 1j * (k_0 * (x - c * t) - angular_frequency * t))

# Define the wave packet that time evolves according to the Schrodinger equation
def wavepacket_vacuum(x, t):
    global x_range
    global L
    fourier_cutoff = 50
    fc = lambda x: initial_wavepacket(x) * np.cos(index * np.pi * x / L)
    fs = lambda x: initial_wavepacket(x) * np.sin(index * np.pi * x / L)

    sum = quad(initial_wavepacket, -L, L)[0] * (1.0 / L)

    for index in range(1, fourier_cutoff + 1):
        an = quad(fc, -L, L)[0] * (1.0 / L)
        bn = quad(fs, -L, L)[0] * (1.0 / L)
        sum += an * np.cos(index * np.pi * x / L - (c * index * np.pi / L) * t) + bn * np.sin(
            index * np.pi * x / L - (c * index * np.pi / L) * t)

    return sum



# find the fourier components of a function(x)
def cos_fourier_component(function, index):
    global x_range
    global L

    def fc(x):
        return function(x) * np.cos(index * np.pi * x / L)

    return quad(fc, -L, L)[0] * (1.0 / L)


def sin_fourier_component(function, index):
    global x_range
    global L

    def fs(x):
        return function(x) * np.sin(index * np.pi * x / L)

    return quad(fs, -L, L)[0] * (1.0 / L)

def wavepacket_medium(x, t, number_of_slices, slice_number):
    global x_range
    global angular_frequency
    global resonant_frequency
    global L
    n = 50
    sum = 0
    slice_width = (x_range / 2) / number_of_slices
    for index in range(1, n + 1):
        an = cos_fourier_component(initial_wavepacket, index)
        bn = sin_fourier_component(initial_wavepacket, index)
        # angular_frequency = c * index * np.pi / L
        phase = material_constant * (slice_number+1) * angular_frequency / (
                resonant_angular_frequency ** 2 - angular_frequency ** 2 + 0.012) * slice_width / c
        sum += an * np.cos(index * np.pi * x / L - (c * index * np.pi / L) * t - phase) + bn * np.sin(
            index * np.pi * x / L - (c * index * np.pi / L) * t)
    return sum


def update(frame):
    # wave in the slices of material
    slice_width = (x_range / 2) / number_of_slices
    for slice_number, line in enumerate(lines):
        if slice_number == number_of_slices:
            x_start = 0
            x_end = int(x_range)
            x = np.linspace(x_start, x_end, 200)
            y = wavepacket_vacuum(x, frame)
            line.set_data(x, y)
        else:
            x_start = (x_range / 2) + slice_number * slice_width
            x_end = (x_range / 2) + (slice_number + 1) * slice_width
            x = np.linspace(x_start, x_end, 20)
            y = wavepacket_medium(x, frame, number_of_slices, slice_number)
            line.set_data(x, y)

    return lines


ani = FuncAnimation(fig, update, frames=100, init_func=init, blit=True)
plt.show()
