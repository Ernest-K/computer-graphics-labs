#!/usr/bin/env python3
import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

RED = random.random()
GREEN = random.random()
BLUE = random.random()

def startup():

    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    draw_sierpinski_carpet(-100, -100, 200, 200, 3)
    glFlush()


def draw_rectangle(x, y, a, b, d=1.0):

    a *= d
    b *= d

    glBegin(GL_TRIANGLES) # wskazanie prymitywu
    glColor3f(RED, GREEN, BLUE)
    glVertex2f(x, y)
    glVertex2f(x+b, y+a)
    glVertex2f(x, y+a)
    glEnd()

    glBegin(GL_TRIANGLES)  # wskazanie prymitywu
    glVertex2f(x, y)
    glVertex2f(x + b, y)
    glVertex2f(x + b, y + a)
    glEnd()


def draw_sierpinski_carpet(x, y, height, width, level):
    if level > 0:
        level -= 1
        width /= 3
        height /= 3

        draw_sierpinski_carpet(x, y, height, width, level)  # lewo-dół
        draw_sierpinski_carpet(x + width, y, height, width, level)  # dół
        draw_sierpinski_carpet(x + 2 * width, y, height, width, level)  # prawo-dół
        draw_sierpinski_carpet(x + 2 * width, y + height, height, width, level)  # prawo
        draw_sierpinski_carpet(x + 2 * width, y + 2 * height, height, width, level)  # prawo-góra
        draw_sierpinski_carpet(x + width, y + 2 * height, height, width, level)  # góra
        draw_sierpinski_carpet(x, y + 2 * height, height, width, level)  # lewo-góra
        draw_sierpinski_carpet(x, y + height, height, width, level)  # lewo

    else:
        draw_rectangle(x, y, height, width)


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()