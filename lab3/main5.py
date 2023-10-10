#!/usr/bin/env python3
import sys
import math
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def spin(angle):
    # glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    # glRotatef(angle, 0.0, 0.0, 1.0)


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def draw_sierpinski_pyramid(x, y, z, a, level):
    if level > 0:
        level -= 1
        a /= 2
        h = a * math.sqrt(2) / 2

        draw_sierpinski_pyramid(x, y, z, a, level)
        draw_sierpinski_pyramid(x, y, z + a, a, level)
        draw_sierpinski_pyramid(x + a, y, z + a, a, level)
        draw_sierpinski_pyramid(x + a, y, z, a, level)
        draw_sierpinski_pyramid(x + a / 2, y + h, z + a / 2, a, level)

    else:
        draw_pyramid(x, y, z, a)


def draw_pyramid(x, y, z, a):
    h = a * math.sqrt(2) / 2

    # podstawa
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 1.0)

    glVertex3f(x, y, z)
    glVertex3f(x, y, z + a)
    glVertex3f(x + a, y, z + a)
    glEnd()
    glBegin(GL_TRIANGLES)
    glVertex3f(x + a, y, z + a)
    glVertex3f(x + a, y, z)
    glVertex3f(x, y, z)
    glEnd()

    # sciany
    glBegin(GL_TRIANGLES)
    glVertex3f(x, y, z)
    glVertex3f(x + a/2, y + h, z + a/2)
    glVertex3f(x + a, y, z)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex3f(x, y, z)
    glVertex3f(x + a/2, y + h, z + a / 2)
    glVertex3f(x, y, z + a)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex3f(x, y, z + a)
    glVertex3f(x + a/2, y + h, z + a / 2)
    glVertex3f(x + a, y, z + a)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex3f(x + a, y, z + a)
    glVertex3f(x + a / 2, y + h, z + a / 2)
    glVertex3f(x + a, y, z)
    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time * 30 / math.pi)
    axes()

    draw_sierpinski_pyramid(0, 0, 0, 5, 3)

    glFlush()


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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

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
