from tkinter import *

window = Tk()
window.title("My First GUI Program")
window.minsize(width=500, height=300)
window.config(padx=100, pady=200)

#Label
my_label = Label(text="I Am a Label", font=("Arial", 24, "bold"))
# my_label.pack()
# my_label.place(x=100, y=200)
my_label.grid(column=0, row=0)
my_label.config(padx=50, pady=50)

# my_label["text"] = "New Text"
my_label.config(text="New Text")

def button_clicked():
    my_label["text"] = "Button got clicked"
    new_text = input.get()
    my_label["text"] = new_text

#Button
button = Button(text="click me", command=button_clicked)
# button.pack()
button.grid(column=1, row=1)
button2 = Button(text="PLAY")
button2.grid(column=2, row=0)

#Entry
input = Entry(width=10)
# input.pack()
input.grid(column=3, row=3)
print(input.get())


window.mainloop()
