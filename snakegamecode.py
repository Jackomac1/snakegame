import tkinter as tk
import random
import os

# Fixed settings
canvas_width = 400
canvas_height = 400
box_size = 20
game_speed = 100

# high score counter
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
else:
    high_score = 0

# Open the graphics window
window = tk.Tk()
window.title("Snake Game")
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="sky blue")
canvas.pack()

# Set the variables for starting
snake_positions = []
snake_boxes = []
snake_direction = None
food_box = None
food_position = (0, 0)
score = 0
game_running = True
game_over_text = None

# write the score board on the window
score_text = canvas.create_text(10, 10, anchor="nw", fill="white", font=("Arial", 12),
                                text=f"Score: {score}  High Score: {high_score}")

# update the score board each time food is hit
def update_score():
    canvas.itemconfig(score_text, text=f"Score: {score}  High Score: {high_score}")
    

# extend the snake
def draw_snake():
    for pos_x, pos_y in snake_positions:
        box = canvas.create_rectangle(pos_x, pos_y, pos_x + box_size, pos_y + box_size, fill="green")
        snake_boxes.append(box)

#drop a new piece of food
def place_food():
    global food_box, food_position
    while True:
        food_x = random.randint(0, (canvas_width - box_size) // box_size) * box_size
        food_y = random.randint(0, (canvas_height - box_size) // box_size) * box_size
        if (food_x, food_y) not in snake_positions:
            break
    food_position = (food_x, food_y)
    food_box = canvas.create_rectangle(food_x, food_y, food_x + box_size, food_y + box_size, fill="purple")

def move_snake():
    global score, food_box, food_position, high_score, game_running, game_speed

    if not game_running or snake_direction is None:
        return

    head_x, head_y = snake_positions[0]

    if snake_direction == "Up":
        head_y -= box_size
    elif snake_direction == "Down":
        head_y += box_size
    elif snake_direction == "Left":
        head_x -= box_size
    elif snake_direction == "Right":
        head_x += box_size

    new_head = (head_x, head_y)

    # check if the snake has hit the wall or itself
    if (head_x < 0 or head_x >= canvas_width or
        head_y < 0 or head_y >= canvas_height or
        new_head in snake_positions):
        end_game()
        return

    snake_positions.insert(0, new_head)
    new_box = canvas.create_rectangle(head_x, head_y, head_x + box_size, head_y + box_size, fill="green")
    snake_boxes.insert(0, new_box)

    if new_head == food_position:
        canvas.delete(food_box)
        place_food()
        score += 1
        if score > 10:
            game_speed = max(30, game_speed - 5)

        if score > high_score:
            high_score = score
        update_score()
    else:
        canvas.delete(snake_boxes[-1])
        snake_boxes.pop()
        snake_positions.pop()

    window.after(game_speed, move_snake)

def handle_key_press(event):
    global snake_direction
    key = event.keysym
    opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}

    if key in ["Up", "Down", "Left", "Right"]:
        if snake_direction is None:
            snake_direction = key
            move_snake()
        elif snake_direction != opposites.get(key):
            snake_direction = key
    elif key == "Return" and not game_running:
        restart_game()

def end_game():
    global game_running, game_over_text
    game_running = False
    game_over_text = canvas.create_text(canvas_width // 2, canvas_height // 2 + 20, fill="white",
                       font=("Arial", 14), text="Press Enter to restart")
    save_high_score()

def save_high_score():
    with open("highscore.txt", "w") as file:
        file.write(str(high_score))

def restart_game():
    global snake_positions, snake_boxes, snake_direction, food_box, food_position
    global score, game_running, game_over_text, game_speed

    # Clear everything
    for box in snake_boxes:
        canvas.delete(box)
    snake_boxes.clear()
    snake_positions.clear()

    if food_box is not None:
        canvas.delete(food_box)
    if game_over_text is not None:
        canvas.delete(game_over_text)
    canvas.itemconfig(score_text, text="")

    # Reset state
    score = 0
    snake_direction = None
    game_running = True
    game_speed = 100

    # Start fresh
    snake_positions.append((100, 100))
    draw_snake()
    place_food()
    update_score()

# start game
snake_positions.append((100, 100))
draw_snake()
place_food()
update_score()

# make arrow keys work
window.bind("<Key>", handle_key_press)

# run the full game
window.mainloop()
