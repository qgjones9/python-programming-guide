# [turtle — Turtle graphics](https://docs.python.org/3/library/turtle.html)

**`turtle`** implements Logo-style **turtle graphics**: a pen-bearing cursor moves in a tkinter canvas, drawing lines and fills. It targets education and quick visual output without third-party plotting libraries. Canonical docs: [turtle.html](https://docs.python.org/3/library/turtle.html).

Requires **`tkinter`** at runtime (`No module named '_tkinter'` otherwise). Optional in minimal Python builds.

---

## Mental model

| Idea | Detail |
|------|--------|
| Turtle | Arrow on screen with position `(x, y)` and heading |
| **`forward` / `backward`** | Move along heading, drawing by default |
| **`left` / `right`** | Turn in degrees |
| **`penup` / `pendown`** | Move without drawing |
| **`begin_fill` / `end_fill`** | Filled polygons |
| **Home** | `(0, 0)` facing east |

---

## Usage modes — [How to…](https://docs.python.org/3/library/turtle.html#how-to)

| Mode | Pattern |
|------|---------|
| **Procedural** | `import turtle` then `turtle.forward(100)` |
| **Module namespace** | `from turtle import *` in interactive sessions |
| **Object-oriented** | `Screen()` + `Turtle()` instances |
| **Script** | `if __name__ == "__main__":` guard; optional `turtle.done()` |

---

### Basic drawing — [Basic drawing](https://docs.python.org/3/library/turtle.html#basic-drawing)

```python
# Goal: compute vertices of a regular polygon without a display
import math

def regular_polygon_points(n, radius, rotation_deg=0):
    points = []
    for i in range(n):
        angle = math.radians(rotation_deg + i * 360 / n)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        points.append((round(x, 3), round(y, 3)))
    return points

triangle = regular_polygon_points(3, 100)
assert len(triangle) == 3
assert all(abs(x) <= 100 and abs(y) <= 100 for x, y in triangle)
```

```python
# Goal: draw a triangle procedurally (illustrative — requires tkinter + display)
# import turtle
# turtle.forward(100)
# turtle.left(120)
# turtle.forward(100)
# turtle.left(120)
# turtle.forward(100)
# turtle.bye()
assert True
```

---

### Pen control — [Pen control](https://docs.python.org/3/library/turtle.html#pen-control)

| Function | Effect |
|----------|--------|
| **`color(pencolor)`**, **`fillcolor(c)`** | Stroke and fill colors |
| **`width(w)`** | Line thickness |
| **`up()` / `down()`** | Pen up/down (aliases `penup`/`pendown`) |
| **`begin_fill()` / `end_fill()`** | Fill enclosed path |
| **`clear()` / `clearscreen()`** | Clear drawing or reset all turtles |

---

### Position and heading — [The turtle's position](https://docs.python.org/3/library/turtle.html#the-turtle-s-position)

| Function | Returns / effect |
|----------|------------------|
| **`pos()`** | `(x, y)` tuple |
| **`heading()`** | Degrees from east |
| **`goto(x, y)`** | Move to coordinates |
| **`home()`** | Origin, east-facing |
| **`setheading(angle)`** | Absolute orientation |

Stopping a spin loop when back near origin: **`abs(pos()) < 1`**.

---

### Object-oriented API — [Object-oriented turtle graphics](https://docs.python.org/3/library/turtle.html#object-oriented-turtle-graphics)

| Class | Role |
|-------|------|
| **`Screen()`** | Canvas, world coordinates, background, animation |
| **`Turtle()`** / **`RawTurtle`** | Individual pen |
| **`TurtleScreen`** | Low-level screen behind `Screen` |

```python
# Goal: OO turtle setup pattern (illustrative — requires tkinter + display)
# from turtle import Screen, Turtle
# screen = Screen()
# screen.title("Demo")
# t = Turtle()
# t.speed(3)
# t.forward(80)
# screen.bye()
assert True
```

---

### Screen configuration — [How to configure Screen and Turtles](https://docs.python.org/3/library/turtle.html#how-to-configure-screen-and-turtles)

| Call | Purpose |
|------|---------|
| **`setup(width, height, startx, starty)`** | Window size/position |
| **`title(name)`**, **`bgcolor(c)`** | Window title and background |
| **`tracer(n)`**, **`update()`** | Animation batching |
| **`onkey` / `listen` / `mainloop`** | Simple event handling |
| **`register_shape(name, shape)`** | Custom polygons |
| **`write(docstring)`** | On-screen help text |

Use **`turtle.mode("logo")`** vs **`"standard"`** vs **`"world"`** to change coordinate semantics.

---

### Algorithmic patterns — [Making algorithmic patterns](https://docs.python.org/3/library/turtle.html#making-algorithmic-patterns)

Nested loops combine color changes and incremental **`forward`** steps—good for teaching loop nesting without external assets.

```python
# Goal: star-drawing loop termination condition (pure math)
import math

def star_returns_home(steps, turn=170, step_size=200):
    x = y = 0.0
    heading = 0.0
    for _ in range(steps):
        heading = (heading + turn) % 360
        rad = math.radians(heading)
        x += step_size * math.cos(rad)
        y += step_size * math.sin(rad)
        if math.hypot(x, y) < 1:
            return True
    return False

# Logo-style star often closes in finite steps
assert isinstance(star_returns_home(360), bool)
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Call **`turtle.done()`** or **`mainloop()`** in scripts | Keeps window open until closed |
| Use **`screen.bye()`** / **`turtle.bye()`** in tests | Closes tk window cleanly |
| Batch animation with **`tracer(0)`** + single **`update()`** | Faster complex drawings |
| Prefer **OO API** when multiple pens needed | Clearer state per turtle |
| Run **`help(turtle)`** or **`Screen().write`** helpers | Built-in docstrings for learners |

---

## See also

- [`tkinter`](../tkinter-python-interface-to-tcltk/index.md) — underlying GUI toolkit
- [Graphical user interfaces with Tk](../index.md) — section hub
