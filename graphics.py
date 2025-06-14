import tkinter as tk
import math
import colorsys

# Settings
WIDTH, HEIGHT = 600, 600
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
NUM_SHAPES = 100
ARMS = 12
SPEED = 0.03
MOUSE_RADIUS = 80
REPULSION_FORCE = 5
RETURN_SPEED = 0.1

root = tk.Tk()
root.title("Elastic Kaleidoscope")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='black')
canvas.pack()

# Track mouse position
mouse_x, mouse_y = CENTER_X, CENTER_Y

def update_mouse(event):
    global mouse_x, mouse_y
    mouse_x, mouse_y = event.x, event.y

canvas.bind('<Motion>', update_mouse)

# Initialize shapes with position and original spiral target
shapes = []
for i in range(NUM_SHAPES):
    radius = i * 3 + 20
    angle = i * 0.3
    size = 4 + i % 3
    hue = (i / NUM_SHAPES) % 1.0
    shapes.append({
        'radius': radius,
        'angle': angle,
        'size': size,
        'hue': hue,
        'x': CENTER_X + radius * math.cos(angle),
        'y': CENTER_Y + radius * math.sin(angle)
    })

def hsl_to_rgb(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'

def animate():
    canvas.delete("all")
    for shape in shapes:
        shape['angle'] += SPEED
        shape['hue'] = (shape['hue'] + 0.002) % 1.0
        radius = shape['radius']
        angle = shape['angle']
        size = shape['size']
        hue = shape['hue']
        color = hsl_to_rgb(hue, 1, 0.5)

        # Target base position in spiral
        target_x = CENTER_X + radius * math.cos(angle)
        target_y = CENTER_Y + radius * math.sin(angle)

        # Distance from mouse
        dx = shape['x'] - mouse_x
        dy = shape['y'] - mouse_y
        dist = math.hypot(dx, dy)

        # Repel if mouse is near
        if dist < MOUSE_RADIUS and dist != 0:
            repel_strength = (1 - dist / MOUSE_RADIUS) * REPULSION_FORCE
            shape['x'] += dx / dist * repel_strength
            shape['y'] += dy / dist * repel_strength
        else:
            # Gently return to spiral position
            shape['x'] += (target_x - shape['x']) * RETURN_SPEED
            shape['y'] += (target_y - shape['y']) * RETURN_SPEED

        # Draw in symmetrical arms
        for arm in range(ARMS):
            a = (2 * math.pi / ARMS) * arm
            rot_x = CENTER_X + (shape['x'] - CENTER_X) * math.cos(a) - (shape['y'] - CENTER_Y) * math.sin(a)
            rot_y = CENTER_Y + (shape['x'] - CENTER_X) * math.sin(a) + (shape['y'] - CENTER_Y) * math.cos(a)
            canvas.create_oval(rot_x - size, rot_y - size, rot_x + size, rot_y + size, fill=color, outline='')

    root.after(20, animate)

animate()
root.mainloop()
