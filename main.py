import math
from tkinter import *
import time

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    # detener la cuenta regresiva
    window.after_cancel(timer)
    timer_label.config(text="Timer", font=(FONT_NAME, 25, "bold"), fg=GREEN, bg=YELLOW)
    check_label.config(text="", font=(FONT_NAME, 25, "normal"))
    canvas.itemconfig(timer_text, text="00:00")
    # hay que llevar las reps totales a 0 porque sino cuando esta en work y le damos reset y despues le damos de nuevo play arranca en descanso
    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #


def start_timer():
    global reps
    global timer_label

    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # if it´s the 8th rep:
    if reps % 8 == 0:
        count_down(long_break_sec)
        timer_label.config(text="LONG BREAK", font=(FONT_NAME, 25, "bold"), fg=PINK, bg=YELLOW)
    # if it´s 2/4/6 rep:
    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="SHORT BREAK", font=(FONT_NAME, 25, "bold"), fg=GREEN, bg=YELLOW)
    # if it´s the 1/3/5/7 rep:
    else:
        count_down(work_sec)
        timer_label.config(text="WORK", font=(FONT_NAME, 25, "bold"), fg=RED, bg=YELLOW)
        print(reps)




# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    global reps
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        # hay que hacer eso porque sino aparece el segundero con 9 en vez de 09
        count_sec = "0" + str(count_sec)

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        # after 1000 miliseg call la funcion count_down
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        # add mark "✔" for cada sesion work realizada
        mark = ""
        for n in range(math.floor(reps/2)):
            mark += "✔"
        check_label.config(text=mark, font=(FONT_NAME, 25, "normal"))




# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro")

# Para que la imagen no quede apretada contra los bordes le damos padding
window.config(padx=100, pady=50, bg=YELLOW)

# Create a canvas (del tamaño de la image y background color)
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
# Create a photoimage
tomato_img = PhotoImage(file="tomato.png")
# Creamos una imagen que la localizamos en el centro de la pantalla
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 30, "bold"))
canvas.grid(column=1, row=1)

# Timer Label
timer_label = Label(text="Timer", font=(FONT_NAME, 25, "bold"), fg=GREEN, bg=YELLOW)
timer_label.grid(column=1, row=0)

# Check mark label
check_label = Label(fg=GREEN, bg=YELLOW)
check_label.grid(column=1, row=4)


# START Button
start_button = Button(text="START", command=start_timer, highlightthickness=0)
start_button.grid(column=0, row=3)

# RESET Button

reset_button = Button(text="RESET", command=reset_timer, highlightthickness=0)
reset_button.grid(column=2, row=3)





window.mainloop()
