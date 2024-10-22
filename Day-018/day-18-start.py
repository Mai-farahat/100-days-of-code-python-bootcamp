import turtle
from turtle import Turtle, Screen
import heroes
import random


timmy_the_turtle = Turtle()
timmy_the_turtle.shape("turtle")
timmy_the_turtle.color("hotpink")

# challenge 1
def draw_square():
    for _ in range(4):
        timmy_the_turtle.forward(100)
        timmy_the_turtle.right(90)

# draw_square()

# challenge 2
def draw_dashed_line():
    for _ in range(15):
        timmy_the_turtle.forward(10)
        timmy_the_turtle.penup()
        timmy_the_turtle.forward(10)
        timmy_the_turtle.pendown()

# draw_dashed_line()

colours = ["brown", "light salmon", "rosy brown", "medium orchid", "light coral", 'cadet blue']

# challenge 3
# def draw_different_shapes(num_sides):
#     angle = 360 / num_sides
#     for _ in range(num_sides):
#         timmy_the_turtle.forward(100)
#         timmy_the_turtle.right(angle)

# for i in range(3, 11):
    # timmy_the_turtle.color(random.choice(colours))
    # draw_different_shapes(i)


# challenge 4
directions = [0, 90, 180, 270]

timmy_the_turtle.speed("fastest")
turtle.colormode(255)

# random RGB colors
def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    color_tuple = (r, g, b)
    return color_tuple


# for _ in range(200):
#     timmy_the_turtle.pensize(15)
#     timmy_the_turtle.color(random_color())
#     timmy_the_turtle.forward(30)
#     timmy_the_turtle.setheading(random.choice(directions))


# challenge 5
def draw_spirograph(size_of_gap):
    for _ in range(int(360 / size_of_gap)):
        timmy_the_turtle.color(random_color())
        timmy_the_turtle.circle(100)
        current_heading = timmy_the_turtle.heading()
        timmy_the_turtle.setheading(current_heading + size_of_gap)

draw_spirograph(5)



screen = Screen()
screen.exitonclick()