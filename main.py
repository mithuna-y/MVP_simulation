import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


# speed of light
C = 1

# plane wave function with a given frequency and optional phase
def plane_wave(frequency, phase=0):
    w = 2 * np.pi * frequency
    def plane_wave_w_function(x, t):
        return np.cos(-w * t + w/C * x + phase)
    return plane_wave_w_function

# frequency of the light and resonant frequency of the material
frequency = 0.05
resonant_frequency = 0.1
t0 = 0

t = np.linspace(0, 10, 100)
n = 100

fig, ax = plt.subplots()
lines = []
for i in range(n + 2):
    if i == 1:
        line, = ax.plot([], [], color="green")
        lines.append(line)
    else:
        line, = ax.plot([], [], color="blue")
        lines.append(line)


ax.set_xlim(-10, 10)
ax.set_ylim(-1.2, 1.2)

def init():
    for line in lines:
        line.set_data([], [])
    return lines

def update(frame):
    # wave in the slices of material
    for i, line in enumerate(lines):
        if i == 0:
            x_start = -10
            x_end = 0
            x = np.linspace(x_start, x_end, 100)
            phase = 0
            y = plane_wave(frequency, phase)(x, frame)
            line.set_data(x, y)
        elif i == 1:
            x_start = 0
            x_end = 10
            x = np.linspace(x_start, x_end, 100)
            phase = 2 * np.pi
            y = plane_wave(frequency * 2.5, phase)(x, frame)
            line.set_data(x, y)
        else:
            x_start = i * 10/n
            x_end = (i+1) * 10/n
            x = np.linspace(x_start, x_end, int(100))
            phase = (i + 1) * 0.5 * frequency / (resonant_frequency - frequency) * 10 / n
            y = plane_wave(frequency, phase)(x, frame)
            line.set_data(x, y)

    return lines

ani = FuncAnimation(fig, update, frames=100, init_func=init, blit=True)
plt.show()







