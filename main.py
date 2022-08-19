BACKGROUND_COLOR = "#B1DDC6"
import pandas
from tkinter import *
import random

window = Tk()
window.minsize(800, 800)
window.title("Flassy")
window.config(padx=10, pady=50, bg=BACKGROUND_COLOR)
score = 0
choices = [0, 2]
rand_choice = 1
times = 0


def flip_front():
    global rand_choice
    print(word)
    rand_choice = random.choice(choices)
    canvas.itemconfig(canvas_lan, text="French")
    canvas.itemconfig(canvas_text, text=f"{word[rand_choice]}")
    canvas.itemconfig(canvas_img, image=img_front)


def flip_back():
    canvas.itemconfig(canvas_lan, text="English")
    canvas.itemconfig(canvas_text, text=f"{word[1]}")
    canvas.itemconfig(canvas_img, image=img_back)


def start_timer():
    right.config(command=right_click)
    flip_back()
    window.after(3000, flip_front)


def score_update():
    global score
    score += 1
    score_label.config(text=f"Score: {score}")


def remove_word(word):
    for key in ["French", "English"]:
        data_dict[key].pop(times)
        data_save = pandas.DataFrame(data_dict)
        data_save.to_csv("./data/french_words.csv", index=False)


def word_generator():
    global times
    n = list(data_dict["English"].keys())
    times = random.choice(n)
    i = random.choice(n)
    word_generator = [value[times] for (key, value) in data_dict.items()]
    word_generator.append(data_dict["French"][i])
    return word_generator


def wrong_click():
    global word
    if (rand_choice == 2):
        score_update()
    word = word_generator()
    start_timer()


def right_click():
    global word
    if (rand_choice == 0):
        score_update()
        remove_word(word)
    word = word_generator()
    start_timer()


# OPEN CSV
data = pandas.read_csv("./data/french_words.csv")
data_dict = data.to_dict()
word = word_generator()
# GUI
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
img_front = PhotoImage(file="./images/card_front.png")
img_back = PhotoImage(file="./images/card_back.png")
canvas_img = canvas.create_image(400, 260, image=img_front)
canvas_text = canvas.create_text(400, 260, font=("Time New Roman", 80, "bold"))
canvas_lan = canvas.create_text(400, 100, font=("Time New Roman", 50, "italic"))
canvas.grid(row=1, column=0, columnspan=10)
# SCORE
score_label = Label(text=f"Score: {score}", bg=BACKGROUND_COLOR, font=("Time New Roman", 30))
score_label.grid(row=0, column=4)
# BUTTON
wrong_img = PhotoImage(file="./images/wrong.png")
right_img = PhotoImage(file="./images/right.png")
wrong = Button(image=wrong_img, command=wrong_click, bg=BACKGROUND_COLOR)
wrong.grid(row=2, column=2)
right = Button(image=right_img, command=start_timer, bg=BACKGROUND_COLOR)
right.grid(row=2, column=7)

window.mainloop()
