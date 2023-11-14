#!/usr/bin/env python3
import sys
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

N = 20
points = [[[0] * 3 for i in range(N)] for j in range(N)]
normals = [[[0] * 3 for i in range(N)] for j in range(N)]

viewer = [0.0, 0.0, 10.0]

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
    global points
    global normals


    u_array = [u / (N - 1) for u in range(0, N)]
    v_array = [v / (N - 1) for v in range(0, N)]

    for i in range(0, N):
        for j in range(0, N):
            x = (-90 * u_array[i] ** 5 + 225 * u_array[i] ** 4 - 270 * u_array[i] ** 3 + 180 * u_array[
                i] ** 2 - 45 * u_array[i]) * math.cos(math.pi * v_array[j])
            y = (160 * u_array[i] ** 4 - 320 * u_array[i] ** 3 + 160 * u_array[i] ** 2 - 5)
            z = (-90 * u_array[i] ** 5 + 225 * u_array[i] ** 4 - 270 * u_array[i] ** 3 + 180 * u_array[
                i] ** 2 - 45 * u_array[i]) * math.sin(math.pi * v_array[j])

            points[i][j][0] = x
            points[i][j][1] = y
            points[i][j][2] = z

            length = math.sqrt(x ** 2 + y ** 2 + z ** 2)
            normals[i][j][0] = x / length
            normals[i][j][1] = y / length
            normals[i][j][2] = z / length


def draw_egg():
    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glNormal3f(normals[i][j][0], normals[i][j][1], normals[i][j][2])
            glVertex3f(points[i][j][0], points[i][j][1], points[i][j][2])
            glNormal3f(normals[i + 1][j][0], normals[i + 1][j][1], normals[i + 1][j][2])
            glVertex3f(points[i + 1][j][0], points[i + 1][j][1], points[i + 1][j][2])
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

    xs = 5 * math.cos(theta_light * (math.pi / 180)) * math.cos(phi_light * (math.pi / 180))
    ys = 5 * math.sin(phi_light * (math.pi / 180))
    zs = 5 * math.sin(theta_light * (math.pi / 180)) * math.cos(phi_light * (math.pi / 180))

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_POSITION, [xs, ys, zs])

    glEnable(GL_LIGHT0)

    draw_egg()

    # glTranslate(xs, ys, zs)
    #
    # quadric = gluNewQuadric()
    # gluQuadricDrawStyle(quadric, GLU_LINE)
    # gluSphere(quadric, 0.5, 6, 5)
    # gluDeleteQuadric(quadric)


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