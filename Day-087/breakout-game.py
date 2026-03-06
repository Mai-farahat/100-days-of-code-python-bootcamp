"""
BREAKOUT - Classic Arcade Game
Built with Python Turtle
"""

import turtle
import time
import random

# ─── Constants ────────────────────────────────────────────────────────────────
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
PADDLE_W      = 120
PADDLE_H      = 12
BALL_SIZE      = 16
BALL_SPEED_INIT = 5
MAX_SPEED      = 12

BRICK_COLS  = 10
BRICK_ROWS  = 6
BRICK_W     = 70
BRICK_H     = 22
BRICK_PADX  = 8
BRICK_PADY  = 6
BRICKS_TOP  = 230  # y of top row centre

ROW_COLORS = ["#FF3B3B", "#FF7A00", "#FFD700", "#4ADE80", "#38BDF8", "#C084FC"]
ROW_POINTS = [7, 7, 5, 5, 3, 3]   # points per brick per row

LIVES = 3

# ─── Setup ────────────────────────────────────────────────────────────────────
screen = turtle.Screen()
screen.title("BREAKOUT")
screen.bgcolor("#0d0d1a")
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.tracer(0)   # manual updates for speed


# ─── Helper – fast rectangle stamp ───────────────────────────────────────────
def make_rect(w, h, color, border=None):
    """Return a turtle pre-shaped as a filled rectangle."""
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.penup()
    t.shape("square")
    t.shapesize(stretch_wid=h/20, stretch_len=w/20)
    t.fillcolor(color)
    t.pencolor(border if border else color)
    t.resizemode("user")
    return t


# ─── Scoreboard ───────────────────────────────────────────────────────────────
class Scoreboard:
    def __init__(self):
        self.score = 0
        self.lives = LIVES
        self.level = 1
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.penup()
        self.t.color("white")
        self.draw()

    def draw(self):
        self.t.clear()
        self.t.goto(-SCREEN_WIDTH//2 + 20, SCREEN_HEIGHT//2 - 35)
        self.t.write(f"SCORE  {self.score:05d}", font=("Courier", 14, "bold"))
        self.t.goto(0, SCREEN_HEIGHT//2 - 35)
        self.t.write(f"LEVEL {self.level}", font=("Courier", 14, "bold"), align="center")
        self.t.goto(SCREEN_WIDTH//2 - 20, SCREEN_HEIGHT//2 - 35)
        self.t.write("♥ " * self.lives, font=("Courier", 14, "bold"), align="right")

    def add(self, pts):
        self.score += pts
        self.draw()

    def lose_life(self):
        self.lives -= 1
        self.draw()
        return self.lives

    def next_level(self):
        self.level += 1
        self.draw()


# ─── Paddle ───────────────────────────────────────────────────────────────────
class Paddle:
    def __init__(self):
        self.t = make_rect(PADDLE_W, PADDLE_H, "#60a5fa", "#93c5fd")
        self.t.goto(0, -SCREEN_HEIGHT//2 + 50)
        self.t.showturtle()
        self.speed = 0
        self._dx = 22

    def go_left(self):  self.speed = -self._dx
    def go_right(self): self.speed =  self._dx
    def stop(self):     self.speed = 0

    def move(self):
        x = self.t.xcor() + self.speed
        half = SCREEN_WIDTH//2 - PADDLE_W//2
        x = max(-half, min(half, x))
        self.t.setx(x)

    @property
    def x(self): return self.t.xcor()
    @property
    def y(self): return self.t.ycor()


# ─── Ball ─────────────────────────────────────────────────────────────────────
class Ball:
    def __init__(self):
        self.t = make_rect(BALL_SIZE, BALL_SIZE, "#f9fafb", "#ffffff")
        self.t.showturtle()
        self.reset()

    def reset(self):
        self.t.goto(0, -80)
        angle = random.uniform(40, 140)   # degrees from +x axis
        import math
        rad = math.radians(angle)
        self.dx = BALL_SPEED_INIT * math.cos(rad)
        self.dy = -BALL_SPEED_INIT * math.sin(rad)  # start going down
        self.dy = abs(self.dy) * -1  # always launch upward
        # recalc: launch upward
        rad2 = math.radians(random.choice([45, 60, 75, 105, 120, 135]))
        import math as m
        self.dx = BALL_SPEED_INIT * m.cos(rad2)
        self.dy = BALL_SPEED_INIT * m.sin(rad2)

    def move(self):
        self.t.setx(self.t.xcor() + self.dx)
        self.t.sety(self.t.ycor() + self.dy)

    def bounce_x(self): self.dx *= -1
    def bounce_y(self): self.dy *= -1

    def speed_up(self, factor=1.05):
        import math
        mag = math.hypot(self.dx, self.dy)
        new_mag = min(mag * factor, MAX_SPEED)
        scale = new_mag / mag
        self.dx *= scale
        self.dy *= scale

    @property
    def x(self): return self.t.xcor()
    @property
    def y(self): return self.t.ycor()


# ─── Brick ────────────────────────────────────────────────────────────────────
class Brick:
    def __init__(self, x, y, color, points):
        self.t = make_rect(BRICK_W, BRICK_H, color, color)
        self.t.goto(x, y)
        self.t.showturtle()
        self.x = x
        self.y = y
        self.points = points
        self.alive = True

    def destroy(self):
        self.alive = False
        self.t.hideturtle()
        self.t.clear()


# ─── Collision helpers ────────────────────────────────────────────────────────
def ball_hits_paddle(ball, paddle):
    bx, by = ball.x, ball.y
    px, py = paddle.x, paddle.y
    hw = (PADDLE_W + BALL_SIZE) / 2
    hh = (PADDLE_H + BALL_SIZE) / 2
    return abs(bx - px) < hw and abs(by - py) < hh

def ball_hits_brick(ball, brick):
    bx, by = ball.x, ball.y
    hw = (BRICK_W  + BALL_SIZE) / 2
    hh = (BRICK_H + BALL_SIZE) / 2
    return abs(bx - brick.x) < hw and abs(by - brick.y) < hh


# ─── Message overlay ─────────────────────────────────────────────────────────
msg_turtle = turtle.Turtle()
msg_turtle.hideturtle()
msg_turtle.penup()
msg_turtle.color("white")

def show_message(line1, line2="", line3=""):
    msg_turtle.clear()
    msg_turtle.goto(0, 60)
    msg_turtle.write(line1, align="center", font=("Courier", 28, "bold"))
    if line2:
        msg_turtle.goto(0, 10)
        msg_turtle.write(line2, align="center", font=("Courier", 16, "normal"))
    if line3:
        msg_turtle.goto(0, -30)
        msg_turtle.write(line3, align="center", font=("Courier", 14, "normal"))
    screen.update()

def clear_message():
    msg_turtle.clear()


# ─── Build brick wall ─────────────────────────────────────────────────────────
def build_bricks():
    bricks = []
    total_w  = BRICK_COLS * (BRICK_W + BRICK_PADX) - BRICK_PADX
    start_x  = -total_w // 2 + BRICK_W // 2
    for row in range(BRICK_ROWS):
        color  = ROW_COLORS[row]
        points = ROW_POINTS[row]
        y = BRICKS_TOP - row * (BRICK_H + BRICK_PADY)
        for col in range(BRICK_COLS):
            x = start_x + col * (BRICK_W + BRICK_PADX)
            bricks.append(Brick(x, y, color, points))
    return bricks


# ─── Main game loop ───────────────────────────────────────────────────────────
def play_game():
    scoreboard = Scoreboard()
    paddle     = Paddle()
    ball       = Ball()
    bricks     = build_bricks()

    # Key bindings
    screen.listen()
    screen.onkeypress(paddle.go_left,  "Left")
    screen.onkeypress(paddle.go_left,  "a")
    screen.onkeypress(paddle.go_right, "Right")
    screen.onkeypress(paddle.go_right, "d")
    screen.onkeyrelease(paddle.stop,   "Left")
    screen.onkeyrelease(paddle.stop,   "a")
    screen.onkeyrelease(paddle.stop,   "Right")
    screen.onkeyrelease(paddle.stop,   "d")

    game_over  = False
    won        = False
    paused     = True
    level_hits = 0   # hits this level (to track speed-ups)

    show_message("BREAKOUT", "← → or A/D  to move paddle", "Press SPACE to launch!")

    launched = False
    def launch(_=None):
        nonlocal paused, launched
        if paused:
            paused   = False
            launched = True
            clear_message()

    screen.onkeypress(launch, "space")
    screen.onkeypress(launch, "Return")

    # Wait for launch
    while not launched:
        screen.update()
        time.sleep(0.016)

    # ── Game loop ──
    while not game_over and not won:
        paddle.move()
        ball.move()

        # Wall collisions
        if ball.x >  SCREEN_WIDTH//2 - BALL_SIZE//2:  ball.bounce_x()
        if ball.x < -SCREEN_WIDTH//2 + BALL_SIZE//2:  ball.bounce_x()
        if ball.y >  SCREEN_HEIGHT//2 - BALL_SIZE//2 - 40: ball.bounce_y()

        # Ball fell off bottom
        if ball.y < -SCREEN_HEIGHT//2:
            lives_left = scoreboard.lose_life()
            if lives_left <= 0:
                game_over = True
                break
            # Reset ball, pause for re-launch
            ball.reset()
            paused   = True
            launched = False
            show_message("BALL LOST!", f"{lives_left} {'life' if lives_left==1 else 'lives'} remaining", "Press SPACE to continue")
            while not launched:
                paddle.move()
                screen.update()
                time.sleep(0.016)

        # Paddle collision
        if ball.dy < 0 and ball_hits_paddle(ball, paddle):
            ball.bounce_y()
            # Add angle influence based on hit position
            offset = (ball.x - paddle.x) / (PADDLE_W / 2)   # -1 … +1
            ball.dx = offset * MAX_SPEED * 0.8
            ball.speed_up(1.03)
            level_hits += 1

        # Brick collisions
        for brick in bricks:
            if brick.alive and ball_hits_brick(ball, brick):
                # Determine bounce direction
                overlap_x = (BRICK_W  + BALL_SIZE) / 2 - abs(ball.x - brick.x)
                overlap_y = (BRICK_H + BALL_SIZE) / 2 - abs(ball.y - brick.y)
                if overlap_x < overlap_y:
                    ball.bounce_x()
                else:
                    ball.bounce_y()
                brick.destroy()
                scoreboard.add(brick.points)
                bricks = [b for b in bricks if b.alive]
                level_hits += 1
                if level_hits % 8 == 0:
                    ball.speed_up(1.04)
                break   # one brick per frame

        # Check win
        if not bricks:
            won = True
            break

        screen.update()
        time.sleep(0.012)

    # ── End screen ──
    screen.update()
    if won:
        show_message("🎉  YOU WIN! 🎉", f"Final Score: {scoreboard.score}", "Close window to exit")
    else:
        show_message("GAME OVER", f"Final Score: {scoreboard.score}", "Close window to exit")

    screen.update()
    turtle.done()


# ─── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    play_game()