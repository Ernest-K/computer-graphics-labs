#!/usr/bin/env python3
import math
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
    draw_sierpinski_triangle(-100, -100, 200, 4)
    glFlush()


def draw_triangle(x, y, a):
    glBegin(GL_TRIANGLES)  # wskazanie prymitywu
    glColor3f(RED, GREEN, BLUE)
    glVertex2f(x, y)
    glVertex2f(x + a, y)
    glVertex2f(x + a/2, y + a*math.sqrt(3)/2)
    glEnd()


def draw_sierpinski_triangle(x, y, a, level):
    if level > 0:
        level -= 1
        a /= 2

        draw_sierpinski_triangle(x, y, a, level) # lewo-dół
        draw_sierpinski_triangle(x+a, y, a, level) # prawo-dół
        draw_sierpinski_triangle(x+a/2, y + a*math.sqrt(3)/2, a, level) # góra
    else:
        draw_triangle(x, y, a)


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