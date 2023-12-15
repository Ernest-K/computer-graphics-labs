#!/usr/bin/env python3
import sys
import math

import numpy
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


N = 20
tab = [[[0] * 3 for i in range(N)] for j in range(N)]

u_derivative = [[[0] * 3 for i in range(N)] for j in range(N)]
v_derivative = [[[0] * 3 for i in range(N)] for j in range(N)]

normals = [[[0] * 3 for i in range(N)] for j in range(N)]

viewer = [0.0, 0.0, 20.0]

theta = 0.0
phi = 0.0

theta_light = 0.0
phi_light = 0.0

pix2angle = 1.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0

mouse_x_pos_old = 0
mouse_y_pos_old = 0

delta_x = 0
delta_y = 0

r_pressed = 0
g_pressed = 0
b_pressed = 0
color_index = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


def generate_vertices():
    global tab
    u_array = [u / (N - 1) for u in range(0, N)]
    v_array = [v / (N - 1) for v in range(0, N)]

    global u_derivative
    global v_derivative

    for i in range(0, N):
        for j in range(0, N):
            # x
            tab[i][j][0] = (-90 * u_array[i] ** 5 + 225 * u_array[i] ** 4 - 270 * u_array[i] ** 3 + 180 * u_array[
                i] ** 2 - 45 * u_array[i]) * math.cos(math.pi * v_array[j])
            # y
            tab[i][j][1] = (160 * u_array[i] ** 4 - 320 * u_array[i] ** 3 + 160 * u_array[i] ** 2 - 5)
            # z
            tab[i][j][2] = (-90 * u_array[i] ** 5 + 225 * u_array[i] ** 4 - 270 * u_array[i] ** 3 + 180 * u_array[
                i] ** 2 - 45 * u_array[i]) * math.sin(math.pi * v_array[j])

            # x_u derivative
            u_derivative[i][j][0] = (- 450 * u_array[i]**4 + 900 * u_array[i]**3 - 810 * u_array[i]**2 + 360 * u_array[i] - 45) * (math.cos(math.pi * v_array[j]))
            # y_u derivative
            u_derivative[i][j][1] = (640 * u_array[i]**3 - 960 * u_array[i]**2 + 320 * u_array[i])
            # z_u derivative
            u_derivative[i][j][2] = (- 450 * u_array[i]**4 + 900 * u_array[i]**3 - 810 * u_array[i]**2 + 360 * u_array[i] - 45) * (math.sin(math.pi * v_array[j]))

            # x_v derivative
            v_derivative[i][j][0] = math.pi * (90 * u_array[i]**5 - 225 * u_array[i]**4 + 270 * u_array[i]**3 - 180 * u_array[i]**2 + 45 * u_array[i]) * (math.sin(math.pi * v_array[j]))
            # y_v derivative
            v_derivative[i][j][1] = 0
            # z_v derivative
            v_derivative[i][j][2] = (-math.pi) * (90 * u_array[i]**5 - 225 * u_array[i]**4 + 270 * u_array[i]**3 - 180 * u_array[i]**2 + 45 * u_array[i]) * (math.cos(math.pi * v_array[j]))

    return tab


def get_normals(tab):
    global normals

    for i in range(0, N):
        for j in range(0, N):
            normals[i][j][0] = (u_derivative[i][j][1] * v_derivative[i][j][2] - u_derivative[i][j][2] * v_derivative[i][j][1])
            normals[i][j][1] = (u_derivative[i][j][2] * v_derivative[i][j][0] - u_derivative[i][j][0] * v_derivative[i][j][2])
            normals[i][j][2] = (u_derivative[i][j][0] * v_derivative[i][j][1] - u_derivative[i][j][1] * v_derivative[i][j][0])

            length = math.sqrt(abs(normals[i][j][0]) ** 2 + abs(normals[i][j][1]) ** 2 + abs(normals[i][j][2]) ** 2)

            if length != 0:
                normals[i][j][0] /= length
                normals[i][j][1] /= length
                normals[i][j][2] /= length
            else:
                normals[i][j][0] = 0.0
                normals[i][j][1] = 1.0
                normals[i][j][2] = 0.0

            # if i > N / 2 or i == 0:
            #     normals[i][j][0] *= -1.0
            #     normals[i][j][1] *= -1.0
            #     normals[i][j][2] *= -1.0

    return normals


def draw_normal():
    for i in range(N):
        for j in range(N):
            glBegin(GL_LINES)
            glVertex(normals[i][j][0] + tab[i][j][0], normals[i][j][1] + tab[i][j][1], normals[i][j][2] + tab[i][j][2])
            glVertex(tab[i][j][0], tab[i][j][1], tab[i][j][2])
            glEnd()


def draw_egg():
    tab = generate_vertices()
    normal = get_normals(tab)


    glColor3f(0.21, 0.54, 0.90)
    for i in range(0, N - 1):
        for j in range(0, N - 1):

            glBegin(GL_TRIANGLES)
            glNormal3f(normal[i][j][0], normal[i][j][1], normal[i][j][2])
            glVertex3f(tab[i][j][0], tab[i][j][1], tab[i][j][2])
            glNormal3f(normal[i + 1][j][0], normal[i + 1][j][1], normal[i + 1][j][2])
            glVertex3f(tab[i + 1][j][0], tab[i + 1][j][1], tab[i + 1][j][2])
            glNormal3f(normal[i][j + 1][0], normal[i][j + 1][1], normal[i][j + 1][2])
            glVertex3f(tab[i][j + 1][0], tab[i][j + 1][1], tab[i][j + 1][2])
            glEnd()

            glBegin(GL_TRIANGLES)
            glNormal3f(normal[i + 1][j + 1][0], normal[i + 1][j + 1][1], normal[i + 1][j + 1][2])
            glVertex3f(tab[i + 1][j + 1][0], tab[i + 1][j + 1][1], tab[i + 1][j + 1][2])
            glNormal3f(normal[i + 1][j][0], normal[i + 1][j][1], normal[i + 1][j][2])
            glVertex3f(tab[i + 1][j][0], tab[i + 1][j][1], tab[i + 1][j][2])
            glNormal3f(normal[i][j + 1][0], normal[i][j + 1][1], normal[i][j + 1][2])
            glVertex3f(tab[i][j + 1][0], tab[i][j + 1][1], tab[i][j + 1][2])
            glEnd()


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    # glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    # glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)



def shutdown():
    pass


def render(time):
    global theta
    global phi
    global theta_light
    global phi_light

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle
        if theta > 360:
            theta -= 360
        elif theta < 0:
            theta += 360
        if phi > 360:
            phi -= 360
        elif phi < 0:
            phi += 360

    if right_mouse_button_pressed:
        theta_light += delta_x * pix2angle
        phi_light += delta_y * pix2angle
        if theta_light > 360:
            theta_light -= 360
        elif theta_light < 0:
            theta_light += 360
        if phi_light > 360:
            phi_light -= 360
        elif phi_light < 0:
            phi_light += 360

    xs = 10 * math.cos(theta_light * (math.pi / 180)) * math.cos(phi_light * (math.pi / 180))
    ys = 10 * math.sin(phi_light * (math.pi / 180))
    zs = 10 * math.sin(theta_light * (math.pi / 180)) * math.cos(phi_light * (math.pi / 180))

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_POSITION, [xs, ys, zs])

    glEnable(GL_LIGHT0)

    draw_egg()
    # draw_normal()
    
    # quadric = gluNewQuadric()
    # gluQuadricDrawStyle(quadric, GLU_FILL)
    # gluSphere(quadric, 3.0, 10, 10)
    # gluDeleteQuadric(quadric)

    glTranslate(xs, ys, zs)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)


    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global color_index

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_R and action == GLFW_PRESS:
        color_index = 0

    if key == GLFW_KEY_G and action == GLFW_PRESS:
        color_index = 1

    if key == GLFW_KEY_B and action == GLFW_PRESS:
        color_index = 2

    if key == GLFW_KEY_UP and action == GLFW_PRESS:
        if light_ambient[color_index] < 1.0:
            light_ambient[color_index] += 0.1

    if key == GLFW_KEY_DOWN and action == GLFW_PRESS:
        if light_ambient[color_index] > 0.0:
            light_ambient[color_index] -= 0.1

    if action == GLFW_RELEASE:
        if color_index == 0:
            print(f'R: {round(light_ambient[color_index], 1)}')
        elif color_index == 1:
            print(f'G: {round(light_ambient[color_index], 1)}')
        elif color_index == 2:
            print(f'B: {round(light_ambient[color_index], 1)}')


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global delta_y
    global mouse_x_pos_old
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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