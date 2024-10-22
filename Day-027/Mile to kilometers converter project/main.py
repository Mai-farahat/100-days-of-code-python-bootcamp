from tkinter import *

def mile_to_km():
    miles = float(input.get())
    km = round(miles * 1.609)
    Km_result_label.config(text=f"{km}")

window = Tk()
window.title("Mile to Km Converter")
window.config(padx=20, pady=20)

#Entry
input = Entry(width=7)
input.grid(column=1, row=0)

#Label
mile_label = Label(text="Miles")
mile_label.grid(column=2, row=0)

is_equal_label = Label(text="is equal to")
is_equal_label.grid(column=0, row=1)

Km_result_label = Label(text="0")
Km_result_label.grid(column=1, row=1)

Km_label = Label(text="Km")
Km_label.grid(column=2, row=1)

calc_button = Button(text="Calculate", command=mile_to_km)
calc_button.grid(column=1, row=2)


window.mainloop()