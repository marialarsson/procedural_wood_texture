import numpy as np
import matplotlib.pyplot as plt
from OpenGL.GL import *
import OpenGL.GL.shaders
from PIL import Image
from PIL import ImageOps

def buffer_verts_and_inds(verts,inds, tex_coords=False):
    
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, verts.itemsize * len(verts), verts, GL_STATIC_DRAW)

    # Create EBO
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, inds.itemsize * len(inds), inds, GL_STATIC_DRAW)


    float_size = ctypes.sizeof(ctypes.c_float)
    stride = 8 * float_size  # Total number of floats in a vertex (x, y, z, s, t, nx, ny, nz)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Texture coordinate attribute (s, t)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * float_size))
    glEnableVertexAttribArray(1)

    # Normal attribute (nx, ny, nz)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(5 * float_size))
    glEnableVertexAttribArray(2)

    glBindVertexArray(0)




def update_shader_camera_uniforms(shader, view, projection, model, light_pos):

    glUseProgram(shader)

    view_loc = glGetUniformLocation(shader, "view")
    proj_loc = glGetUniformLocation(shader, "projection")
    model_loc = glGetUniformLocation(shader, "model")
    light_loc = glGetUniformLocation(shader, "lightPosition")
    

    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glUniform3fv(light_loc, 1, GL_FALSE, light_pos)


def get_cuboid_with_normals(h, w, d):
    vertices = []
    tex_coords = []
    normals = []

    # Front face A (normal pointing in the +z direction)
    vertices.extend([
        -0.5 * h, -0.5 * w, 0.5 * d,   # Vertex 0
         0.5 * h, -0.5 * w, 0.5 * d,   # Vertex 1
         0.5 * h,  0.5 * w, 0.5 * d,   # Vertex 2
        -0.5 * h,  0.5 * w, 0.5 * d    # Vertex 3
    ])
    tex_coords.extend([
        0.0, 1.0,   # Texture coordinate for Vertex 0
        1.0, 1.0,   # Texture coordinate for Vertex 1
        1.0, 0.0,   # Texture coordinate for Vertex 2
        0.0, 0.0    # Texture coordinate for Vertex 3
    ])
    normals.extend([
        0.0, 0.0, 1.0,  # Normal for Vertex 0
        0.0, 0.0, 1.0,  # Normal for Vertex 1
        0.0, 0.0, 1.0,  # Normal for Vertex 2
        0.0, 0.0, 1.0   # Normal for Vertex 3
    ])

    # Back face F (normal pointing in the -z direction)
    vertices.extend([
        -0.5 * h, -0.5 * w, -0.5 * d,   # Vertex 4
         0.5 * h, -0.5 * w, -0.5 * d,   # Vertex 5
         0.5 * h,  0.5 * w, -0.5 * d,   # Vertex 6
        -0.5 * h,  0.5 * w, -0.5 * d    # Vertex 7
    ])
    tex_coords.extend([
        1.0, 1.0,   # Texture coordinate for Vertex 4
        0.0, 1.0,   # Texture coordinate for Vertex 5
        0.0, 0.0,   # Texture coordinate for Vertex 6
        1.0, 0.0    # Texture coordinate for Vertex 7
    ])
    normals.extend([
        0.0, 0.0, -1.0,  # Normal for Vertex 4
        0.0, 0.0, -1.0,  # Normal for Vertex 5
        0.0, 0.0, -1.0,  # Normal for Vertex 6
        0.0, 0.0, -1.0   # Normal for Vertex 7
    ])

    # Left face C (normal pointing in the -x direction)
    vertices.extend([
        -0.5 * h, -0.5 * w, -0.5 * d,   # Vertex 8
        -0.5 * h, -0.5 * w,  0.5 * d,   # Vertex 9
        -0.5 * h,  0.5 * w,  0.5 * d,   # Vertex 10
        -0.5 * h,  0.5 * w, -0.5 * d    # Vertex 11
    ])
    tex_coords.extend([
        0.0, 1.0,   # Texture coordinate for Vertex 8
        1.0, 1.0,   # Texture coordinate for Vertex 9
        1.0, 0.0,   # Texture coordinate for Vertex 10
        0.0, 0.0    # Texture coordinate for Vertex 11
    ])
    normals.extend([
        -1.0, 0.0, 0.0,  # Normal for Vertex 8
        -1.0, 0.0, 0.0,  # Normal for Vertex 9
        -1.0, 0.0, 0.0,  # Normal for Vertex 10
        -1.0, 0.0, 0.0   # Normal for Vertex 11
    ])

    # Right face E (normal pointing in the +x direction)
    vertices.extend([
         0.5 * h, -0.5 * w, -0.5 * d,   # Vertex 12
         0.5 * h, -0.5 * w,  0.5 * d,   # Vertex 13
         0.5 * h,  0.5 * w,  0.5 * d,   # Vertex 14
         0.5 * h,  0.5 * w, -0.5 * d    # Vertex 15
    ])
    tex_coords.extend([
        1.0, 1.0,   # Texture coordinate for Vertex 12
        0.0, 1.0,   # Texture coordinate for Vertex 13
        0.0, 0.0,   # Texture coordinate for Vertex 14
        1.0, 0.0    # Texture coordinate for Vertex 15
    ])
    normals.extend([
        1.0, 0.0, 0.0,  # Normal for Vertex 12
        1.0, 0.0, 0.0,  # Normal for Vertex 13
        1.0, 0.0, 0.0,  # Normal for Vertex 14
        1.0, 0.0, 0.0   # Normal for Vertex 15
    ])

    # Top face B (normal pointing in the +y direction)
    vertices.extend([
        -0.5 * h,  0.5 * w,  0.5 * d,   # Vertex 16
         0.5 * h,  0.5 * w,  0.5 * d,   # Vertex 17
         0.5 * h,  0.5 * w, -0.5 * d,   # Vertex 18
        -0.5 * h,  0.5 * w, -0.5 * d    # Vertex 19
    ])
    tex_coords.extend([
        0.0, 1.0,   # Texture coordinate for Vertex 16
        1.0, 1.0,   # Texture coordinate for Vertex 17
        1.0, 0.0,   # Texture coordinate for Vertex 18
        0.0, 0.0    # Texture coordinate for Vertex 19
    ])
    normals.extend([
        0.0, 1.0, 0.0,  # Normal for Vertex 16
        0.0, 1.0, 0.0,  # Normal for Vertex 17
        0.0, 1.0, 0.0,  # Normal for Vertex 18
        0.0, 1.0, 0.0   # Normal for Vertex 19
    ])

    # Bottom face D (normal pointing in the -y direction)
    vertices.extend([
        -0.5 * h, -0.5 * w, -0.5 * d,   # Vertex 20
         0.5 * h, -0.5 * w, -0.5 * d,   # Vertex 21
         0.5 * h, -0.5 * w,  0.5 * d,   # Vertex 22
        -0.5 * h, -0.5 * w,  0.5 * d    # Vertex 23
    ])
    tex_coords.extend([
        0.0, 1.0,   # Texture coordinate for Vertex 20
        1.0, 1.0,   # Texture coordinate for Vertex 21
        1.0, 0.0,   # Texture coordinate for Vertex 22
        0.0, 0.0    # Texture coordinate for Vertex 23
    ])
    normals.extend([
        0.0, -1.0, 0.0,  # Normal for Vertex 20
        0.0, -1.0, 0.0,  # Normal for Vertex 21
        0.0, -1.0, 0.0,  # Normal for Vertex 22
        0.0, -1.0, 0.0   # Normal for Vertex 23
    ])


    # Combine vertices and texture coordinates and normals into one list
    vertices_with_tex_coords_and_normals = []
    for i in range(len(vertices) // 3):
        vertices_with_tex_coords_and_normals.extend(vertices[i*3:i*3+3])
        vertices_with_tex_coords_and_normals.extend(tex_coords[i*2:i*2+2])
        vertices_with_tex_coords_and_normals.extend(normals[i*3:i*3+3])

    # Define face indices
    face_indices = [0, 1, 2, 0, 2, 3,   # Front face
                    16, 17, 18, 16, 18, 19,  # Top face
                    8, 9, 10, 8, 10, 11,   # Left face
                    20, 21, 22, 20, 22, 23,   # Bottom face
                    12, 13, 14, 12, 14, 15,   # Right face
                    4, 5, 6, 4, 6, 7]   # Back face
                    
                    
                
    # Define line indices for wireframe rendering
    line_indices = [0, 1, 1, 2, 2, 3, 3, 0,     # Front face
                    4, 5, 5, 6, 6, 7, 7, 4,     # Back face
                    8, 9, 9, 10, 10, 11, 11, 8,     # Left face
                    12, 13, 13, 14, 14, 15, 15, 12,   # Right face
                    16, 17, 17, 18, 18, 19, 19, 16,   # Top face
                    20, 21, 21, 22, 22, 23, 23, 20]   # Bottom face

    return np.array(vertices_with_tex_coords_and_normals, dtype=np.float32), np.array(face_indices, dtype=np.uint32), np.array(line_indices, dtype=np.uint32)


def get_cuboid(h,w,d):

    vertices = []
    tex_coords = []

    # Define vertices and texture coordinates for each face separately
    # Front face A
    vertices.extend([
        -0.5 * h, -0.5 * w, 0.5 * d,   # Vertex 0
         0.5 * h, -0.5 * w, 0.5 * d,   # Vertex 1
         0.5 * h,  0.5 * w, 0.5 * d,   # Vertex 2
        -0.5 * h,  0.5 * w, 0.5 * d    # Vertex 3
    ])
    tex_coords.extend([
        0.0, 1.0,   # Texture coordinate for Vertex 0
        1.0, 1.0,   # Texture coordinate for Vertex 1
        1.0, 0.0,   # Texture coordinate for Vertex 2
        0.0, 0.0    # Texture coordinate for Vertex 3
    ])

    # Back face F
    vertices.extend([
        -0.5 * h, -0.5 * w, -0.5 * d,   # Vertex 4
         0.5 * h, -0.5 * w, -0.5 * d,   # Vertex 5
         0.5 * h,  0.5 * w, -0.5 * d,   # Vertex 6
        -0.5 * h,  0.5 * w, -0.5 * d    # Vertex 7
    ])
    tex_coords.extend([
        1.0, 1.0,   # Texture coordinate for Vertex 4
        0.0, 1.0,   # Texture coordinate for Vertex 5
        0.0, 0.0,   # Texture coordinate for Vertex 6
        1.0, 0.0    # Texture coordinate for Vertex 7
    ])

    # Left face C
    vertices.extend([
        -0.5 * h, -0.5 * w, -0.5 * d,   # Vertex 8
        -0.5 * h, -0.5 * w,  0.5 * d,   # Vertex 9
        -0.5 * h,  0.5 * w,  0.5 * d,   # Vertex 10
        -0.5 * h,  0.5 * w, -0.5 * d    # Vertex 11
    ])
    tex_coords.extend([
        0.0, 1.0,   # Texture coordinate for Vertex 8
        1.0, 1.0,   # Texture coordinate for Vertex 9
        1.0, 0.0,   # Texture coordinate for Vertex 10
        0.0, 0.0    # Texture coordinate for Vertex 11
    ])

    # Right face E
    vertices.extend([
         0.5 * h, -0.5 * w, -0.5 * d,   # Vertex 12
         0.5 * h, -0.5 * w,  0.5 * d,   # Vertex 13
         0.5 * h,  0.5 * w,  0.5 * d,   # Vertex 14
         0.5 * h,  0.5 * w, -0.5 * d    # Vertex 15
    ])
    tex_coords.extend([
        1.0, 1.0,   # Texture coordinate for Vertex 12
        0.0, 1.0,   # Texture coordinate for Vertex 13
        0.0, 0.0,   # Texture coordinate for Vertex 14
        1.0, 0.0    # Texture coordinate for Vertex 15
    ])

    # Top face B
    vertices.extend([
        -0.5 * h,  0.5 * w,  0.5 * d,   # Vertex 16
         0.5 * h,  0.5 * w,  0.5 * d,   # Vertex 17
         0.5 * h,  0.5 * w, -0.5 * d,   # Vertex 18
        -0.5 * h,  0.5 * w, -0.5 * d    # Vertex 19
    ])
    tex_coords.extend([
        0.0, 1.0,   # Texture coordinate for Vertex 16
        1.0, 1.0,   # Texture coordinate for Vertex 17
        1.0, 0.0,   # Texture coordinate for Vertex 18
        0.0, 0.0    # Texture coordinate for Vertex 19
    ])

    # Bottom face D
    vertices.extend([
        -0.5 * h, -0.5 * w, -0.5 * d,   # Vertex 20
         0.5 * h, -0.5 * w, -0.5 * d,   # Vertex 21
         0.5 * h, -0.5 * w,  0.5 * d,   # Vertex 22
        -0.5 * h, -0.5 * w,  0.5 * d    # Vertex 23
    ])
    tex_coords.extend([
        0.0, 1.0,   # Texture coordinate for Vertex 20
        1.0, 1.0,   # Texture coordinate for Vertex 21
        1.0, 0.0,   # Texture coordinate for Vertex 22
        0.0, 0.0    # Texture coordinate for Vertex 23
    ])

    # Combine vertices and texture coordinates into one list
    vertices_with_tex_coords = []
    for i in range(len(vertices) // 3):
        vertices_with_tex_coords.extend(vertices[i*3:i*3+3])
        vertices_with_tex_coords.extend(tex_coords[i*2:i*2+2])

    # Define face indices
    face_indices = [0, 1, 2, 0, 2, 3,   # Front face
                    16, 17, 18, 16, 18, 19,  # Top face
                    8, 9, 10, 8, 10, 11,   # Left face
                    20, 21, 22, 20, 22, 23,   # Bottom face
                    12, 13, 14, 12, 14, 15,   # Right face
                    4, 5, 6, 4, 6, 7]   # Back face
                    
                    
                    

    # Define line indices for wireframe rendering
    line_indices = [0, 1, 1, 2, 2, 3, 3, 0,     # Front face
                    4, 5, 5, 6, 6, 7, 7, 4,     # Back face
                    8, 9, 9, 10, 10, 11, 11, 8,     # Left face
                    12, 13, 13, 14, 14, 15, 15, 12,   # Right face
                    16, 17, 17, 18, 18, 19, 19, 16,   # Top face
                    20, 21, 21, 22, 22, 23, 23, 20]   # Bottom face

    return np.array(vertices_with_tex_coords, dtype=np.float32), np.array(face_indices, dtype=np.uint32), np.array(line_indices, dtype=np.uint32)


def create_shader_program(VERT, FRAG):

    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(VERT, GL_VERTEX_SHADER),OpenGL.GL.shaders.compileShader(FRAG, GL_FRAGMENT_SHADER))
    return shader


def get_image_from_glbuffer(width, height):
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGB", (width, height), data)
    image = ImageOps.flip(image) # in my case image is flipped top-bottom for some reason
    return image
