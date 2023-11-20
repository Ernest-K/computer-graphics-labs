import sys
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

viewer = [0.0, 0.0, 20.0]

N = 20
points = [[[0] * 3 for _ in range(N)] for _ in range(N)]
normals = [[[0] * 3 for _ in range(N)] for _ in range(N)]
for i in range(N):
    u = 1 / (N - 1) * i
    for j in range(N):
        v = 1 / (N - 1) * j
        x = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.cos(math.pi * v)
        y = 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2 - 5
        z = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.sin(math.pi * v)

        points[i][j][0] = x
        points[i][j][1] = y
        points[i][j][2] = z

        length = math.sqrt(x ** 2 + y ** 2 + z ** 2)
        normals[i][j][0] = x / length
        normals[i][j][1] = y / length
        normals[i][j][2] = z / length

R = 12

theta = 0.0
phi = 0.0
pix2angle = 1.0

theta_light = 0.0
phi_light = 0.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0
mouse_y_pos_old = 0
delta_y = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient_0 = [0.0, 0.0, 0.0, 0.5]
light_diffuse_0 = [0.0, 0.0, 0.0, 1.0]
light_specular_0 = [1.0, 1.0, 1.0, 1.0]
light_position_0 = [-10.0, 10.0, 0.0, 1.0]

att_constant_0 = 1.0
att_linear_0 = 0.05
att_quadratic_0 = 0.001

light_ambient_1 = [0.0, 0.0, 0.0, 0.5]
light_diffuse_1 = [0.0, 0.0, 0.0, 1.0]
light_specular_1 = [1.0, 1.0, 1.0, 1.0]
light_position_1 = [10.0, -10.0, 0.0, 1.0]

att_constant_1 = 1.0
att_linear_1 = 0.05
att_quadratic_1 = 0.001

light_mode = 0
color_index = 0

normals_mode = 0


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)


def shutdown():
    pass


def render(time):
    global theta
    global phi
    global theta_light
    global phi_light

    fix_colors(light_ambient_0)
    fix_colors(light_diffuse_0)
    fix_colors(light_ambient_1)
    fix_colors(light_diffuse_1)

    first_light()
    second_light()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    if right_mouse_button_pressed:
        theta_light += delta_x * pix2angle
        phi_light += delta_y * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0, 0.0)

    light_sphere(light_position_0[0], light_position_0[1], light_position_0[2])
    light_sphere(light_position_1[0], light_position_1[1], light_position_1[2])

    draw_egg()

    if normals_mode == 1:
        draw_normals()

    print(f'R: {light_ambient_0[0]} G: {light_ambient_0[1]} B: {light_ambient_0[2]} ', end='')
    print(f'| R: {light_ambient_1[0]} G: {light_ambient_1[1]} B: {light_ambient_1[2]}')

    glFlush()


def first_light():
    light_position_0[0] = math.cos(theta_light * math.pi / 180) * math.cos(phi_light * math.pi / 180) * R
    light_position_0[1] = math.sin(phi_light * math.pi / 180) * R
    light_position_0[2] = math.sin(theta_light * math.pi / 180) * math.cos(phi_light * math.pi / 180) * R

    glLightfv(GL_LIGHT0, GL_POSITION, light_position_0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient_0)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse_0)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular_0)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant_0)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear_0)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic_0)


def second_light():
    light_position_1[0] = -math.cos(theta_light * math.pi / 180) * math.cos(phi_light * math.pi / 180) * R
    light_position_1[1] = -math.sin(phi_light * math.pi / 180) * R
    light_position_1[2] = -math.sin(theta_light * math.pi / 180) * math.cos(phi_light * math.pi / 180) * R

    glLightfv(GL_LIGHT1, GL_POSITION, light_position_1)
    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient_1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse_1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular_1)

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant_1)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear_1)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic_1)


def draw_egg():
    global points
    global normals
    global N

    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glNormal3f(normals[i][j][0], normals[i][j][1], normals[i][j][2])
            glVertex3f(points[i][j][0], points[i][j][1], points[i][j][2])
            glNormal3f(normals[i + 1][j][0], normals[i + 1][j][1], normals[i + 1][j][2])
            glVertex3f(points[i + 1][j][0], points[i + 1][j][1], points[i + 1][j][2])
        glEnd()


def draw_normals():
    for i in range(N):
        for j in range(N):
            glBegin(GL_LINES)
            glVertex3f(points[i][j][0], points[i][j][1], points[i][j][2])
            glVertex3f(points[i][j][0] + normals[i][j][0],
                       points[i][j][1] + normals[i][j][1],
                       points[i][j][2] + normals[i][j][2])
            glEnd()


def example_object():
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)


def light_sphere(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 1.0, 10, 10)
    gluDeleteQuadric(quadric)
    glPopMatrix()


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
    global light_mode
    global normals_mode

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
        return

    if key == GLFW_KEY_R and action == GLFW_PRESS:
        color_index = 0
        return

    if key == GLFW_KEY_G and action == GLFW_PRESS:
        color_index = 1
        return

    if key == GLFW_KEY_B and action == GLFW_PRESS:
        color_index = 2
        return

    if key == GLFW_KEY_SPACE and action == GLFW_PRESS:
        light_mode = (light_mode + 1) % 2
        return

    if key == GLFW_KEY_KP_ADD and action == GLFW_PRESS:
        if light_mode == 0:
            light_ambient_0[color_index] += 0.1
            light_diffuse_0[color_index] += 0.1
        else:
            light_ambient_1[color_index] += 0.1
            light_diffuse_1[color_index] += 0.1
        return

    if key == GLFW_KEY_KP_SUBTRACT and action == GLFW_PRESS:
        if light_mode == 0:
            light_ambient_0[color_index] -= 0.1
            light_diffuse_0[color_index] -= 0.1
        else:
            light_ambient_1[color_index] -= 0.1
            light_diffuse_1[color_index] -= 0.1

    if key == GLFW_KEY_ENTER and action == GLFW_PRESS:
        normals_mode = (normals_mode + 1) % 2


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old
    global delta_y
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


def fix_colors(array: list):
    if array[0] < 0:
        array[0] = 0
    if array[1] < 0:
        array[1] = 0
    if array[2] < 0:
        array[2] = 0
    if array[0] > 1:
        array[0] = 1
    if array[1] > 1:
        array[1] = 1
    if array[2] > 1:
        array[2] = 1


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