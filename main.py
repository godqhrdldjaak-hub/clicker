import turtle
import time
import random
import math

# --------------------
# Variables & AI Settings
# --------------------
last_time = time.perf_counter()
gameEnd = False

# Set difficulty to Hard for the advanced predictive AI
AI_DIFFICULTY = "Hard"

# Keyboard state (Human plays via 'w' and 's')
keys = {}

# Particle Spark System
particles = []

# Sprite Settings
sballminx = -350
sballmaxx = 350
sballminy = -250
sballmaxy = 250

sballsize = 1.2
lballsize = 2

move_speed = 155
paddle_speed = 400  # High speed for pro AI

Lscore = 0
Rscore = 0

# Scene 2 Yellow Ball state
yellow_spawned = False
yellow_active = False

# --------------------
# Screen
# --------------------
screen = turtle.Screen()
screen.setup(800, 600)
screen.title("Game - Player vs Pro AI with Sparks (Instant Reset)")
screen.tracer(0)

# --------------------
# Helper Functions
# --------------------
def create_sprite(shape, color, x, y, stretch_w=2, stretch_len=1):
    sprite = turtle.Turtle()
    sprite.speed(0)
    sprite.shape(shape)
    sprite.color(color)
    sprite.shapesize(stretch_wid=stretch_w, stretch_len=stretch_len)
    sprite.penup()
    sprite.goto(x, y)
    return sprite

def create_ball(shape, color, x, y, stretch_w=2, stretch_len=1, angle=0):
    ball = create_sprite(shape, color, x, y, stretch_w, stretch_len)
    # Restrict initial heading to point toward the player (left side: 135 to 225 degrees)
    ball.setheading(random.randint(135, 225))
    ball.hideturtle()
    return ball

def create_paddle(shape, color, x, y, stretch_w=2, stretch_len=1):
    paddle = create_sprite(shape, color, x, y, stretch_w, stretch_len)
    paddle.setheading(90)
    paddle.showturtle()
    return paddle

# --------------------
# Particle Sparks System
# --------------------
def create_sparks(x, y):
    for _ in range(6):  # Create 6 tiny spark dots per collision
        p = turtle.Turtle()
        p.speed(0)
        p.shape("circle")
        p.color("yellow" if random.random() > 0.5 else "orange")
        p.shapesize(stretch_wid=0.3, stretch_len=0.3)
        p.penup()
        p.goto(x, y)
        p.setheading(random.randint(0, 360))
        particles.append({
            "turtle": p,
            "speed": random.randint(120, 220),
            "life": 12  # Lifespan in frames
        })

def update_particles(dt):
    global particles
    active_particles = []
    for p_data in particles:
        p = p_data["turtle"]
        p.forward(p_data["speed"] * dt)
        p_data["life"] -= 1
        if p_data["life"] <= 0:
            p.hideturtle()
            p.clear()
        else:
            active_particles.append(p_data)
    particles = active_particles

# --------------------
# Sprite Creation
# --------------------
small_balls = []

for i in range(3):
    ball = create_ball("circle", "blue", random.randint(sballminx, sballmaxx), random.randint(sballminy, sballmaxy), sballsize, sballsize)
    small_balls.append(ball)

ball = create_ball("circle", "blue", 0, 0, lballsize, lballsize)
gameoverball = create_ball("circle", "red", 0, 0, 2, 2, random.randint(1, 120))

# Yellow Bonus Ball for Scene 2
yellow_ball = create_ball("circle", "yellow", 0, 0, lballsize, lballsize)

leftpaddle = create_paddle("square", "black", -400, 0, 1, 3)
rightpaddle = create_paddle("square", "black", 391, 0, 1, 3)

endingtext = turtle.Turtle()
endingtext.penup()
endingtext.goto(0, 100)
endingtext.color("cyan")
endingtext.hideturtle()

scoretext = turtle.Turtle()
scoretext.hideturtle()
scoretext.penup()
scoretext.goto(0, 210)

def update_score():
    scoretext.clear()
    scoretext.write(f"LScore: {Lscore}   RScore: {Rscore}", align="center", font=("Arial", 24, "bold"))

update_score()

# --------------------
# Input Handling
# --------------------
def set_key(key, state):
    keys[key] = state

controls = ["w", "s", "a", "d"]

screen.listen()
for k in controls:
    screen.onkeypress(lambda k=k: set_key(k, True), k)
    screen.onkeyrelease(lambda k=k: set_key(k, False), k)

# --------------------
# Instant Ball Reset
# --------------------
def reset_ball(ball_obj):
    ball_obj.hideturtle()
    ball_obj.goto(0, 0)
    # Instantly serve toward player (left side) without pausing
    ball_obj.setheading(random.randint(135, 225))
    ball_obj.showturtle()

# --------------------
# Collisions
# --------------------
def collision_with_paddleL(b, paddle):
    global Lscore
    if b.distance(paddle) < 30 and (90 < b.heading() < 270):
        create_sparks(b.xcor(), b.ycor())
        Lscore = Lscore + 1
        update_score()
        return True
    return False

def collision_with_paddleR(b, paddle):
    global Rscore
    if b.distance(paddle) < 30 and (b.heading() < 90 or b.heading() > 270):
        create_sparks(b.xcor(), b.ycor())
        Rscore = Rscore + 1
        update_score()
        reset_ball(b)  # Instantly reset and serve when point is scored
        return True
    return False

def collision_with_paddleL_yellow(b, paddle):
    global Lscore
    if b.distance(paddle) < 30 and (90 < b.heading() < 270):
        create_sparks(b.xcor(), b.ycor())
        Lscore = Lscore + 2
        update_score()
        return True
    return False

def collision_with_paddleR_yellow(b, paddle):
    global Rscore
    if b.distance(paddle) < 30 and (b.heading() < 90 or b.heading() > 270):
        create_sparks(b.xcor(), b.ycor())
        Rscore = Rscore + 2
        update_score()
        reset_ball(b)
        return True
    return False

def move_ball(b, speed, dt, lp, rp):
    b.showturtle()
    b.forward(speed * dt)

    if b.ycor() > 280 or b.ycor() < -280:
        create_sparks(b.xcor(), b.ycor())
        b.setheading(-b.heading())

    if lp is not None and collision_with_paddleL(b, lp):
        b.setheading(180 - b.heading())
        return True

    elif rp is not None and collision_with_paddleR(b, rp):
        b.setheading(180 - b.heading())
        return True

    return False

def move_yellow_ball(b, speed, dt, lp, rp):
    b.showturtle()
    b.forward(speed * dt)

    if b.ycor() > 280 or b.ycor() < -280:
        create_sparks(b.xcor(), b.ycor())
        b.setheading(-b.heading())

    if lp is not None and collision_with_paddleL_yellow(b, lp):
        b.setheading(180 - b.heading())
        return True

    elif rp is not None and collision_with_paddleR_yellow(b, rp):
        b.setheading(180 - b.heading())
        return True

    return False

def endpage(b, speed, dt, lp, rp):
    if b.xcor() > 400 and not collision_with_paddleR(b, rp):
        return True
    if b.xcor() < -400 and not collision_with_paddleL(b, lp):
        return True
    return False
        
def scene2(r_score, l_score):
    if r_score > 2 or l_score > 2:
        return True
    return False

# --------------------
# Advanced Predictive AI Logic
# --------------------
def predict_landing_y(b, target_x):
    sim_x, sim_y = b.xcor(), b.ycor()
    heading = b.heading()
    rad = math.radians(heading)
    sim_dx = math.cos(rad)
    sim_dy = math.sin(rad)
    
    if sim_dx <= 0:
        return sim_y
        
    for _ in range(300):
        if sim_x >= target_x:
            break
        sim_x += sim_dx * 10
        sim_y += sim_dy * 10
        
        if sim_y > 280:
            sim_y = 280 - (sim_y - 280)
            sim_dy = -sim_dy
        elif sim_y < -280:
            sim_y = -280 + (-280 - sim_y)
            sim_dy = -sim_dy
            
    return sim_y

def ai_move(paddle, balls, speed, dt):
    paddle_y = paddle.ycor()
    
    target_ball = None
    max_dx = -9999
    
    for b in balls:
        if b.isvisible():
            rad = math.radians(b.heading())
            dx = math.cos(rad)
            if dx > 0 and b.xcor() < 390:
                if dx > max_dx:
                    max_dx = dx
                    target_ball = b
                    
    if not target_ball:
        target_ball = balls[0]

    target_y = predict_landing_y(target_ball, rightpaddle.xcor())

    tolerance = 4
    ai_speed = speed * 1.25

    if paddle_y < target_y - tolerance:
        paddle.setheading(90)
        paddle.forward(ai_speed * dt)
    elif paddle_y > target_y + tolerance:
        paddle.setheading(90)
        paddle.backward(ai_speed * dt)

# --------------------
# Game Loop
# --------------------
def game_loop():
    global last_time, gameEnd, yellow_spawned, yellow_active

    current_time = time.perf_counter()
    dt = current_time - last_time
    last_time = current_time

    # Update spark particles every frame
    update_particles(dt)

    # Left Paddle Movement (Human controlled)
    if keys.get("w"):
        leftpaddle.forward(paddle_speed * dt)
    if keys.get("s"):
        leftpaddle.backward(paddle_speed * dt)

    # Continuous gameplay without countdown pause
    all_active_balls = [ball, gameoverball]
    if yellow_active:
        all_active_balls.append(yellow_ball)
    all_active_balls.extend(small_balls)
    
    ai_move(rightpaddle, all_active_balls, paddle_speed, dt)

    move_ball(ball, move_speed, dt, leftpaddle, rightpaddle)

    if scene2(Rscore, Lscore):
        if not yellow_spawned:
            yellow_spawned = True
            yellow_active = True

        for i in range(1):
            move_ball(small_balls[i], move_speed, dt, leftpaddle, rightpaddle)
            if endpage(small_balls[i], move_speed, dt, leftpaddle, rightpaddle):
                gameEnd = True

        if move_ball(gameoverball, move_speed, dt, leftpaddle, rightpaddle):
            gameEnd = True

        if yellow_active:
            move_yellow_ball(yellow_ball, move_speed, dt, leftpaddle, rightpaddle)
            if yellow_ball.xcor() > 400 or yellow_ball.xcor() < -400:
                yellow_ball.hideturtle()
                yellow_active = False

    if endpage(ball, move_speed, dt, leftpaddle, rightpaddle):
        gameEnd = True

    if gameEnd:
        endingtext.write("gameover", align="center", font=("Arial", 50, "bold"))

    screen.update()

    if not gameEnd:
        screen.ontimer(game_loop, 16)

# --------------------
# Run the game
# --------------------
game_loop()
turtle.done()