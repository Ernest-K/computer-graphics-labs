#!/usr/bin/env python3
import sys
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


def draw_rect(x, y, size):
    glBegin(GL_QUADS)
    glVertex2f(x - size / 2, y - size / 2)
    glVertex2f(x + size / 2, y - size / 2)
    glVertex2f(x + size / 2, y + size / 2)
    glVertex2f(x - size / 2, y + size / 2)
    glEnd()


def draw_sierpinski_carpet(x, y, size, level, color):
    glColor3f(*color)

    if level == 0:
        draw_rect(x, y, size)
        return
    else:
        level -= 1
        size /= 3

        # Recursive calls for the eight surrounding squares
        draw_sierpinski_carpet(x - size - size / 2, y - size - size/2, size, level, color)
        draw_sierpinski_carpet(x - size - size / 2, y - size / 2, size, level, color)
        draw_sierpinski_carpet(x - size - size / 2, y + size / 2, size, level, color)
        draw_sierpinski_carpet(x - size / 2, y + size / 2, size, level, color)
        draw_sierpinski_carpet(x + size / 2, y + size / 2, size, level, color)
        draw_sierpinski_carpet(x + size / 2, y - size / 2, size, level, color)
        draw_sierpinski_carpet(x + size / 2, y - size - size / 2, size, level, color)
        draw_sierpinski_carpet(x - size / 2, y - size - size / 2, size, level, color)


def startup():
    update_viewport(None, 800, 800)
    glClearColor(0.5, 0.5, 0.5, 1.0)

def shutdown():
    pass

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    # Fixed color for all squares
    color = (0.0, 1.0, 0.0)  # Green

    # Draw the Sierpinski carpet
    draw_sierpinski_carpet(0.0, 0.0, 400.0, 4, color)

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
        glOrtho(-400.0, 400.0, -400.0 / aspect_ratio, 400.0 / aspect_ratio, 1.0, -1.0)
    else:
        glOrtho(-400.0 * aspect_ratio, 400.0 * aspect_ratio, -400.0, 400.0, 1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(800, 800, "Sierpinski Carpet", None, None)
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