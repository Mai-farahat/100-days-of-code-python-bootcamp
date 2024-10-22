from turtle import Turtle, Screen
import random

is_race_on = False
screen = Screen()
screen.setup(width=500, height=400)
user_bet = screen.textinput(title='Make your bet', prompt='Which turtle will win the race? Enter a color: ')
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
y_position = [-125, -75, -25, 25, 75, 125]
all_turtles = []

for pos_index in range(6):
    new_turtle = Turtle(shape='turtle')
    new_turtle.color(colors[pos_index])
    new_turtle.penup()
    new_turtle.goto(-230, y_position[pos_index])
    all_turtles.append(new_turtle)

if user_bet:
    is_race_on = True


while is_race_on:

    for turtle in all_turtles:
        if turtle.xcor() > 230:
            is_race_on = False
            winning_color = turtle.pencolor()
            if winning_color == user_bet:
                print(f"you win! The {winning_color} turtle is the winner.")
            else:
                print(f"you lose! The {winning_color} turtle is the winner.")

        turtle.forward(random.randint(0, 10))


screen.exitonclick()