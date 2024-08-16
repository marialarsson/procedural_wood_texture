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

    glUseProgram(shader_procedural_wood)

    # Create and buffer cuboid vertecies and indices
    verts, face_inds, line_inds = render_utils.get_cuboid_with_normals(cuboid_H,cuboid_W,cuboid_D)
    inds =  np.concatenate([face_inds, line_inds])
    render_utils.buffer_verts_and_inds(verts, inds)

    glClearColor(1.0, 1.0, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    # Setup view
    light_position = np.array([3.0,3.0,-4.0])
    view_position = pyrr.Vector3([0.0,0.0,-5.0])
    target = pyrr.Vector3([0.0, 0.0, 0.0])
    up = pyrr.Vector3([0.0, 1.0, 0.0])
    view = pyrr.matrix44.create_look_at(view_position, target, up)
    projection = pyrr.matrix44.create_perspective_projection(20.0, 720/600, 0.1, 100.0)
    model = np.eye(4)
    glLoadIdentity()

    render_utils.update_shader_camera_uniforms(shader_procedural_wood, view, projection, model, view_position, light_position)
    
    # set rotation of cuboid    
    xrot0 = math.pi/5
    yrot0 = 5*math.pi/4
    zrot0 = 0.0

    t = 0

    while not glfw.window_should_close(window):

        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_utils.draw_cuboid_with_procedural_texture(shader_procedural_wood, face_inds, 0.00*t, xrot0=xrot0, yrot0=yrot0, zrot0=zrot0)

        # Finalize
        img = render_utils.get_image_from_glbuffer(width,height)
        glfw.swap_buffers(window)
        glfw.poll_events()
        t+=1
        
        # rotate light around model
        light_distance = 4.0
        ang = 0.03*t #math.pi/3
        x = light_distance * math.cos(ang)
        y = light_distance*1.0
        z = light_distance * math.sin(ang)
        #light_pos = [x, y, z]
        #light_pos_loc = glGetUniformLocation(shader_procedural_wood, "lightPos")
        #glUniform3f(light_pos_loc, light_pos[0], light_pos[1], light_pos[2])
    
    glfw.terminate()

    # save
    path = 'screenshot.png'
    img.save(path, 'PNG')
    print("Saved", path)

if __name__ == "__main__":
    main()
