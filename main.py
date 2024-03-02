from tkinter import *
import pandas
import random
from gtts import gTTS
from playsound import playsound

BACKGROUND_COLOR = "#FFEECC"
current_card = {}
data_d = {}

# --------------------New Flash Cards ------------------#
try:
    data = pandas.read_csv("/Users/fatmaekbic/PycharmProjects/English-Turkish/data/Words_to_learn.cvs")
except FileNotFoundError:
    original_data = pandas.read_csv("/Users/fatmaekbic/PycharmProjects/English-Turkish/data/english_words.csv")
    data_d = original_data.to_dict(orient="records")
else:
    data_d = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(data_d)
    canvas.itemconfig(canvas_image, image=front_pic)
    canvas.itemconfig(title, text="English", fill="black")
    canvas.itemconfig(word, text=current_card["English"], fill="black")
    pronounce(current_card["English"], 'en', slow=True)
    flip_timer = window.after(4000, func=flip)


def flip():
    canvas.itemconfig(canvas_image, image=back_pic)
    canvas.itemconfig(title, text="Turkish", fill="black")
    canvas.itemconfig(word, text=current_card["Turkish"], fill="black")



def pronounce(text, lang, slow=False):
    # Generate pronunciation audio file
    tts = gTTS(text=text, lang=lang, slow=slow)
    tts.save("pronunciation.mp3")
    # Play the pronunciation audio file
    playsound("pronunciation.mp3")


def is_known():
    data_d.remove(current_card)
    d = pandas.DataFrame(data_d)
    d.to_csv("data/Words_to_learn.csv", index=False)
    print(len(d))

    next_card()


# ----------------- UI Setup -------------------------#
window = Tk()
window.title("Flashy")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip)

canvas = Canvas(width=800, height=526, highlightthickness=0)
front_pic = PhotoImage(file="/Users/fatmaekbic/PycharmProjects/English-Turkish/images/card_front.png")
back_pic = PhotoImage(file="/Users/fatmaekbic/PycharmProjects/English-Turkish/images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=front_pic)
title = canvas.create_text(400, 150, text="Title", font=("Arial", 40, "italic"), fill="black")
word = canvas.create_text(400, 263, text="word", font=("Arial", 60, "bold"), fill="black")
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
cross = PhotoImage(file="images/wrong.png")
cross_button = Button(image=cross, width=100, height=100, highlightthickness=0, command=next_card)
cross_button.grid(row=2, column=0)

right = PhotoImage(file="images/right.png")
right_button = Button(image=right, width=100, height=100, highlightthickness=0, command=is_known)
right_button.grid(row=2, column=1)

next_card()
window.mainloop()
