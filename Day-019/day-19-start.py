from turtle import Turtle, Screen

tim = Turtle()
tim.speed("fastest")

def move_forward():
    tim.forward(10)

def move_backwards():
    tim.backward(10)

def turn_left():
    tim.setheading(tim.heading() + 10)

def turn_right():
    tim.setheading(tim.heading() - 10)

def clear():
    tim.clear()
    tim.penup()
    tim.home()
    tim.pendown()

my_keys = ['w', 's', 'a', 'd', 'c']

screen = Screen()
screen.listen()
def my_move(func, key):
    screen.onkey(func, key)


my_move(move_forward, my_keys[0])
my_move(move_backwards, my_keys[1])
my_move(turn_left, my_keys[2])
my_move(turn_right, my_keys[3])
my_move(clear, my_keys[4])

screen.exitonclick()