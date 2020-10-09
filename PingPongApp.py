from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

# TODO: Build the Game

class PongBall(Widget):
    # Velocity in X Direction (Left to Right)
    # Numeric Property will define it as a number or integer
    velocity_x = NumericProperty(0)     # Default value set to 0
    velocity_y = NumericProperty(0)
    # Control both variables at same time
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # Latest Position of Call = Current Velocity + Current Position
    def move(self):
        # A Form that gives Direction of Velocity
        self.pos = Vector(*self.velocity) + self.pos

class PongPaddle(Widget):
    score = NumericProperty(0)
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            ball.velocity_x *= -1


# TODO: Create the Game
class PongGame(Widget):
    # Need to tell our App / Python that ball is an object
    # Python will associate this ball that we defined in .kv
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self):
        # Change the velocity of the ball and randomize its direction
        self.ball.velocity = Vector(10, 0).rotate(randint(0, 360))


    # Moving the Ball by Calling the Move() and Other Fn
    def update(self, dt):
        self.ball.move()

        # Bounce off Top and Bottom - Reverse if it below Y Axis or Beyond Screen Height
        if (self.ball.y < 0) or (self.ball.y > self.height - 50):
            self.ball.velocity_y *= -1

        # Bounce off Left and Right - Reverse if it below X Axis or Beyond Screen Width
        if (self.ball.x < 0):
            self.ball.velocity_x *= -1
            self.player2.score += 1
        if (self.ball.x > self.width - 50):
            self.ball.velocity_x *= -1
            self.player1.score += 2

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

    def on_touch_move(self, touch):
        # Check if touch is on left side of the screen
        if touch.x < self.width / 1/4:
            self.player1.center_y = touch.y
        if touch.x > self.width * 3/4:
            self.player2.center_y = touch.y

# TODO: Create the App
class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/120.0) # 1 sec 60 images will be shown
        return game

# TODO: Run the App
PongApp().run()
