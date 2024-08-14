import numpy as np
from OpenGL.GL import *
from scipy.ndimage import zoom


def get_vertex_shader():
    VERTEX_SHADER = """

            #version 330 core

            layout(location = 0) in vec3 in_position;
            layout (location = 1) in vec2 in_tex_coord;
            layout (location = 2) in vec3 in_normal;

            uniform mat4 projection;
            uniform mat4 view;
            uniform mat4 model;
            uniform mat4 transform;

            out vec3 out_position;
            out vec3 out_abs_normal;
            out vec3 out_normal;
            

            void main() {
                gl_Position = projection * view * model * transform * vec4(in_position, 1.0);
                out_abs_normal = in_normal;
                out_normal = normalize(transpose(inverse(mat3(model))) * in_normal);
                out_position = in_position;
            }
          """
    return VERTEX_SHADER



def get_procedural_wood_fragment_shader():

    FRAGMENT_SHADER = open("COMMON//procedural_wood_fragment_shader.frag",'r').read()

    return FRAGMENT_SHADER