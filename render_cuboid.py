import glfw
from OpenGL.GL import *
import numpy as np
import pyrr
import math
import sys


sys.path.append("COMMON")
import render_utils
import shader_utils
import draw_utils

def main():
    if not glfw.init():
        return

    # Initiate window
    height = 1200
    width = 1440
    window = glfw.create_window(width, height, "Cuboid", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # Set up shaders
    VERTEX_SHADER = shader_utils.get_vertex_shader()
    FRAGMENT_SHADER_PROCEDURAL_WOOD = shader_utils.get_procedural_wood_fragment_shader()

    # Compile The Program and shaders
    shader_procedural_wood = render_utils.create_shader_program(VERTEX_SHADER, FRAGMENT_SHADER_PROCEDURAL_WOOD)
        
    # Set proportions of cubiod
    cuboid_H=1.0
    cuboid_W=1.0
    cuboid_D=1.0

    glUseProgram(0)

    # Create and buffer cuboid vertecies and indices
    verts, face_inds, line_inds = render_utils.get_cuboid_with_normals(cuboid_H,cuboid_W,cuboid_D)
    inds =  np.concatenate([face_inds, line_inds])
    render_utils.buffer_verts_and_inds(verts, inds)

    glClearColor(1.0, 1.0, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    # Setup view
    view = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0,0.0,-5.0]))
    projection = pyrr.matrix44.create_perspective_projection(20.0, 720/600, 0.1, 100.0)
    model = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0,0.0,0.0]))
    glLoadIdentity()

    render_utils.update_shader_camera_uniforms(shader_procedural_wood, view, projection, model)
    
    # set rotation of cuboid    
    xrot0 = -math.pi/5 
    yrot0 = math.pi/4 
    zrot0 = 0.0

    while not glfw.window_should_close(window):

        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        t = 0 # time, can control rotation etc.

        draw_utils.draw_cuboid_with_procedural_texture(shader_procedural_wood, face_inds, 0*t, xrot0=xrot0, yrot0=yrot0, zrot0=zrot0)

        # Finalize
        img = render_utils.get_image_from_glbuffer(width,height)
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

    # save
    path = 'screenshot.png'
    img.save(path, 'PNG')
    print("Saved", path)

if __name__ == "__main__":
    main()
