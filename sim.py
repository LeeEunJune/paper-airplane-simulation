import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

g = 9.81
Fg = 0.049
m = Fg / g
L = 0.307
w = 0.11
r = -0.01013 #point of application of Lift

dt = 0.01
max_steps = 10000

theta = np.radians(9)
vx = 4.97 * np.cos(theta)
vy = 4.97 * np.sin(theta)
x, y = 0.0, 0.0

x_data, y_data, theta_data = [], [], []
v_data = []
Fl_data = []

for _ in range(max_steps):
    v = np.sqrt(vx**2 + vy**2)
    if v == 0:
        break

    theta = np.arctan2(vy, vx)

    Fl = 0.00158 * v**2

    fx, fy = np.cos(theta), np.sin(theta)
    nx, ny = -fy, fx

    Flx = Fl * nx
    Fly = Fl * ny

    Fx = Flx
    Fy = Fly - Fg

    ax = Fx / m
    ay = Fy / m
    vx += ax * dt
    vy += ay * dt
    x += vx * dt
    y += vy * dt

    x_data.append(x)
    y_data.append(y)
    theta_data.append(theta)
    v_data.append(v)
    Fl_data.append(Fl)

    if x >= 5.0:
        break

fig1, ax1 = plt.subplots(figsize=(8,5))
ax1.set_xlim(0, 5.0)
ax1.set_ylim(min(y_data)-0.2, max(y_data)+0.2)
ax1.set_aspect('equal')
plane_line, = ax1.plot([], [], 'b-', lw=2)
trace_line, = ax1.plot([], [], 'r--', lw=1)

trace_x, trace_y = [], []

def init():
    plane_line.set_data([], [])
    trace_line.set_data([], [])
    return plane_line, trace_line

def animate(i):
    cx, cy = x_data[i], y_data[i]
    angle = theta_data[i]

    dx = (L / 2) * np.cos(angle)
    dy = (L / 2) * np.sin(angle)

    x1, x2 = cx - dx, cx + dx
    y1, y2 = cy - dy, cy + dy
    plane_line.set_data([x1, x2], [y1, y2])

    trace_x.append(cx)
    trace_y.append(cy)
    trace_line.set_data(trace_x, trace_y)

    return plane_line, trace_line

ani = animation.FuncAnimation(
    fig1, animate, frames=len(x_data),
    init_func=init, blit=True, interval=10,
    repeat=False
)

plt.title("Paper Plane")
plt.xlabel("X position (m)")
plt.ylabel("Y position (m)")
plt.grid(True)

fig2, (axv, axtheta, axFl) = plt.subplots(3, 1, figsize=(8, 8), sharex=True)
time = np.arange(len(v_data)) * dt

axv.plot(time, v_data, label="Speed (m/s)")
axv.set_ylabel("Speed (m/s)")
axv.grid(True)
axv.legend()

axtheta.plot(time, np.degrees(theta_data), label="Angle (deg)", color='orange')
axtheta.set_ylabel("Angle (deg)")
axtheta.grid(True)
axtheta.legend()

axFl.plot(time, Fl_data, label="Lift Force (N)", color='green')
axFl.set_xlabel("Time (s)")
axFl.set_ylabel("Lift Force (N)")
axFl.grid(True)
axFl.legend()

plt.tight_layout()

plt.show()
