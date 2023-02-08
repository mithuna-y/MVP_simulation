import matplotlib.pyplot as plt
import numpy as np

# speed of light
C = 1


# plane wave function with a given frequency and optional phase
def plane_wave(frequency, phase=0):
    w = 2 * np.pi * frequency
    def plane_wave_w_function(x, t):
        return np.cos(w * t + w/C * x + phase)
    return plane_wave_w_function


frequency = 0.05
t0 = 0
x = np.linspace(-10, 0, 100)
y = plane_wave(frequency)(x, t0)
plt.plot(x, y)

n = 100
step = 10/n
for i in range(n):
    x_segment = np.linspace(i*step, (i+1)*step, 100)
    phase = (i + 1) * 0.2
    print(f"phase is {phase}, frequency is {frequency}, and initial value is {plane_wave(frequency, phase)(0, t0)}")
    y_segment = plane_wave(frequency, phase)(x_segment, t0)
    plt.plot(x_segment, y_segment)
plt.xlabel('x')
plt.ylabel('y')

plt.title('Light travelling through n layers of electrons- kinda')

plt.show()





