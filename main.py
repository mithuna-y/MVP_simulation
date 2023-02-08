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

# # original light unimpeded by medium
# x = np.linspace(-10, 0, 100)
# y = plane_wave(frequency)(x, t0)
# plt.plot(x, y)

t = np.linspace(0, 10, 100)
n = 50

fig, ax = plt.subplots()
lines = []
for i in range(n + 1):
    line, = ax.plot([], [], color="blue")
    lines.append(line)

ax.set_xlim(-10, 10)
ax.set_ylim(-1.2, 1.2)

def init():
    for line in lines:
        line.set_data([], [])
    return lines

def update(frame):
    for i, line in enumerate(lines):
        x_start = i * 10/n
        x_end = (i+1) * 10/n
        x = np.linspace(x_start, x_end, int(100/n))
        phase = (i + 1) * 0.5 * frequency / (resonant_frequency - frequency) * 10 / n
        y = plane_wave(frequency, phase)(x, frame)
        line.set_data(x, y)

    x_start = -10
    x_end = 0
    x = np.linspace(x_start, x_end, 100)
    phase = 0
    y = plane_wave(frequency, phase)(x, frame)
    line.set_data(x, y)
    return lines


ani = FuncAnimation(fig, update, frames=100, init_func=init, blit=True)
plt.show()


#
# # slicing the medium up
# n = 100
# step = 10/n
# for i in range(n):
#     x_segment = np.linspace(i*step, (i+1)*step, 100)
#     phase = (i + 1) * 0.5 * frequency / (resonant_frequency - frequency) * 10 / n
#     y_segment = plane_wave(frequency, phase)(x_segment, t0)
#     plt.plot(x_segment, y_segment, color="blue")
# plt.xlabel('x')
# plt.ylabel('y')
#
# plt.title('Light travelling through n layers of electrons properly \n accounting for frequency dependence of shift')
#
# plt.show()







