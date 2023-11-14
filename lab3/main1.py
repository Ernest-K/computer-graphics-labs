#!/usr/bin/env python3
import sys
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

N = 20

tab = [[[0] * 3 for i in range(N)] for j in range(N)]
u_array = [u / (N-1) for u in range(0, N)]
v_array = [v / (N-1) for v in range(0, N)]

print(u_array)
print(v_array)

for i in range(0, N):
    for j in range(0, N):
        # x
        tab[i][j][0] = (-90 * u_array[i] ** 5 + 225 * u_array[i] ** 4 - 270 * u_array[i] ** 3 + 180 * u_array[i] ** 2 - 45 * u_array[i]) * math.cos(math.pi * v_array[j])
        # y
        tab[i][j][1] = (160 * u_array[i] ** 4 - 320 * u_array[i] ** 3 + 160 * u_array[i] ** 2 - 5)
        # z
        tab[i][j][2] = (-90 * u_array[i] ** 5 + 225 * u_array[i] ** 4 - 270 * u_array[i] ** 3 + 180 * u_array[i] ** 2 - 45 * u_array[i]) * math.sin(math.pi * v_array[j])


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


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


def draw_egg():
    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 1.0)
    for i in range(0, N):
        for j in range(0, N):
            glVertex3f(tab[i][j][0],
                       tab[i][j][1],
                       tab[i][j][2])
    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # axes()
    spin(time * 180 / math.pi)

    draw_egg()

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