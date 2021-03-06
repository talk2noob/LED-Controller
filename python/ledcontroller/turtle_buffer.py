from Manifest import SendingBuffer, Color, turtle

class TurtleBuffer(SendingBuffer):
  __SCALE = 10
  __DOT_SIZE = 8
  """
  Simulates writing to the Arduino and LED strip using Turtle Graphics
  on the local machine.
  """
  def __init__(self, **kwargs):
    """Initializes the Turtle Graphics canvas."""
    SendingBuffer.__init__(self, **kwargs)
    turtle.colormode(1)
    turtle.screensize(canvwidth=self.__SCALE*(self.GetSize()+2),
      canvheight=self.__SCALE*2)
    turtle.setup(height=self.__SCALE*2 + 100)
    turtle.setworldcoordinates(-self.__SCALE, -self.__SCALE,
      self.__SCALE*(self.GetSize()+1), self.__SCALE)
    turtle.bgcolor(0.1, 0.1, 0.1)
    turtle.penup() # no connecting line
    turtle.hideturtle() # no turtle on screen
    turtle.tracer(0, 0) # no animation
    turtle.setundobuffer(None) # no undo buffer

  def Send(self, reverse=False):
    """Draws the current colors in Turtle Graphics. Also sends to Serial."""
    colors = self.GetColors()
    n = len(colors)
    if reverse:
      colors = reversed(colors)

    ave_color = Color()

    # Clear last time's drawings (dots).
    turtle.clear()
    # Draw the LEDs.
    for c in colors:
      turtle.dot(self.__DOT_SIZE, *c.GetRgb())
      turtle.fd(self.__SCALE)
      ave_color.Add(c, clamp=False)
    # Update the background. (Causes an update.)
    turtle.bgcolor(*ave_color.Scaled(0.4 * 1.0/n).GetRgb())
    # Retrace.
    turtle.right(180)
    turtle.fd(self.__SCALE*n)
    turtle.left(180)

    SendingBuffer.Send(self, reverse=reverse)

