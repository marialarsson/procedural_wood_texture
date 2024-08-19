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

    gif_frame_images = []

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

    # Pith
    pith_org = (0.6, 0.0, 0.4)
    pith_dir_in = (0.5, 1.0, 0.0)
    glUniform3f(glGetUniformLocation(shader_procedural_wood, "pith_org"), pith_org[0], pith_org[1], pith_org[2])
    glUniform3f(glGetUniformLocation(shader_procedural_wood, "pith_dir_in"), pith_dir_in[0], pith_dir_in[1], pith_dir_in[2])

    # Annual rings
    average_ring_distance = 0.1
    earlywood_col = (0.75, 0.70, 0.54)
    latewood_col = (0.65, 0.55, 0.42)
    ring_col_mix_variables = (0.4, 0.9)
    glUniform1f(glGetUniformLocation(shader_procedural_wood, "average_ring_distance"), average_ring_distance)
    glUniform3f(glGetUniformLocation(shader_procedural_wood, "earlywood_col"), earlywood_col[0], earlywood_col[1], earlywood_col[2])
    glUniform3f(glGetUniformLocation(shader_procedural_wood, "latewood_col"), latewood_col[0], latewood_col[1], latewood_col[2])
    glUniform2f(glGetUniformLocation(shader_procedural_wood, "ring_col_mix_variables"), ring_col_mix_variables[0], ring_col_mix_variables[1])


    # Fibers
    fiber_cell_dim = 0.005
    wood_fiber_color_noise_weight = 0.2
    glUniform1f(glGetUniformLocation(shader_procedural_wood, "fiber_cell_dim"), fiber_cell_dim)
    glUniform1f(glGetUniformLocation(shader_procedural_wood, "wood_fiber_color_noise_weight"), wood_fiber_color_noise_weight)

    # Pores
    pore_radius = 0.15
    pore_equal_occurance_ratio = 0.8
    pore_ring_occurance_ratio = 0.2
    pore_cell_dims = (0.015, 0.015, 0.2)
    glUniform1f(glGetUniformLocation(shader_procedural_wood, "pore_radius"), pore_radius)
    glUniform1f(glGetUniformLocation(shader_procedural_wood, "pore_equal_occurance_ratio"), pore_equal_occurance_ratio)
    glUniform1f(glGetUniformLocation(shader_procedural_wood, "pore_ring_occurance_ratio"), pore_ring_occurance_ratio)
    glUniform3f(glGetUniformLocation(shader_procedural_wood, "pore_cell_dims"), pore_cell_dims[0], pore_cell_dims[1], pore_cell_dims[2])

    # Rays
    ray_radius = 0.2
    ray_occurance_ratio = 0.5
    ray_cell_dims = (0.2, 0.015, 0.4)
    ray_color = (0.66, 0.56, 0.40)    
    glUniform1f(glGetUniformLocation(shader_procedural_wood, "ray_radius"), ray_radius)
    glUniform1f(glGetUniformLocation(shader_procedural_wood, "ray_occurance_ratio"), ray_occurance_ratio)
    glUniform3f(glGetUniformLocation(shader_procedural_wood, "ray_cell_dims"), ray_cell_dims[0], ray_cell_dims[1], ray_cell_dims[2])
    glUniform3f(glGetUniformLocation(shader_procedural_wood, "ray_color"), ray_color[0], ray_color[1], ray_color[2])

    t = 0
    tmax = 20

    while not glfw.window_should_close(window):
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        
        
        # rotate light around model
        light_distance = 4.0
        ang = math.pi + 2 * math.pi * t / tmax
        x = light_distance * math.cos(ang)
        y = light_distance*0.5
        z = light_distance * math.sin(ang)
        light_pos = [x, y, z]
        light_pos_loc = glGetUniformLocation(shader_procedural_wood, "lightPos")
        glUniform3f(light_pos_loc, light_pos[0], light_pos[1], light_pos[2])

        # variables
        # Define all variables

        # Pith
        pith_org = np.array([0.6, 0.0, 0.4])
        pith_dir_in = np.array([0.5, 1.0, 0.0])
        #pith_org = np.random.normal(loc=0.0, scale=1.0, size=3)
        #pith_dir_in = 2.0*(np.random.rand(3)-0.5)

        # Annual rings
        average_ring_distance = 0.1
        ring_col_mix_variables = np.array([0.4, 0.9])
        earlywood_col = np.array([0.75, 0.70, 0.54])
        latewood_col = np.array([0.65, 0.55, 0.42])
        #average_ring_distance = np.random.normal(loc=0.125, scale=0.025, size=1)
        #a = np.random.normal(loc=0.4, scale=0.1, size=1)
        #b = np.random.normal(loc=0.9, scale=0.05, size=1)
        #ring_col_mix_variables = np.array([a, b])

        # Fibers
        fiber_cell_dim = 0.005
        wood_fiber_color_noise_weight = 0.2
        #fiber_cell_dim = max(np.random.normal(loc=0.0075, scale=0.0025, size=1), 0.001)
        #wood_fiber_color_noise_weight = max(np.random.normal(loc=0.3, scale=0.2, size=1),0.0)

        # Pores
        pore_radius = 0.15
        pore_equal_occurance_ratio = 0.8
        pore_ring_occurance_ratio = 0.2
        pore_cell_dims = np.array([0.015, 0.015, 0.2])
        #pore_radius = max(min(np.random.normal(loc=0.20, scale=0.15, size=1),0.5),0.0)
        #pore_equal_occurance_ratio = np.random.rand(1)
        #pore_ring_occurance_ratio = np.random.rand(1)
        #pore_cell_dims = np.random.normal(loc=0.015, scale=0.005, size=2) * np.array([1.0,10.0]) + np.array([0.0,0.1])
        #pore_cell_dims = np.array([pore_cell_dims[0],pore_cell_dims[0],pore_cell_dims[1]])

        # Rays
        ray_radius = 0.2
        ray_occurance_ratio = 0.5
        ray_cell_dims = np.array([0.2, 0.015, 0.4])
        ray_color = np.array([0.66, 0.56, 0.40])
        #ray_radius = max(min(np.random.normal(loc=0.20, scale=0.05, size=1),0.5),0.0)
        #ray_occurance_ratio = np.random.rand(1)
        #ray_cell_dims = np.random.normal(loc=0.25, scale=0.05, size=3) * np.array([1.0,0.05,2.0]) + np.array([0.0,0.0,0.1])

        # Upload all uniforms
        glUniform3f(glGetUniformLocation(shader_procedural_wood, "pith_org"), pith_org[0], pith_org[1], pith_org[2])
        glUniform3f(glGetUniformLocation(shader_procedural_wood, "pith_dir_in"), pith_dir_in[0], pith_dir_in[1], pith_dir_in[2])
        glUniform1f(glGetUniformLocation(shader_procedural_wood, "average_ring_distance"), average_ring_distance)
        glUniform3f(glGetUniformLocation(shader_procedural_wood, "earlywood_col"), earlywood_col[0], earlywood_col[1], earlywood_col[2])
        glUniform3f(glGetUniformLocation(shader_procedural_wood, "latewood_col"), latewood_col[0], latewood_col[1], latewood_col[2])
        glUniform2f(glGetUniformLocation(shader_procedural_wood, "ring_col_mix_variables"), ring_col_mix_variables[0], ring_col_mix_variables[1])
        glUniform1f(glGetUniformLocation(shader_procedural_wood, "fiber_cell_dim"), fiber_cell_dim)
        glUniform1f(glGetUniformLocation(shader_procedural_wood, "wood_fiber_color_noise_weight"), wood_fiber_color_noise_weight)
        glUniform1f(glGetUniformLocation(shader_procedural_wood, "pore_radius"), pore_radius)
        glUniform1f(glGetUniformLocation(shader_procedural_wood, "pore_equal_occurance_ratio"), pore_equal_occurance_ratio)
        glUniform1f(glGetUniformLocation(shader_procedural_wood, "pore_ring_occurance_ratio"), pore_ring_occurance_ratio)
        glUniform3f(glGetUniformLocation(shader_procedural_wood, "pore_cell_dims"), pore_cell_dims[0], pore_cell_dims[1], pore_cell_dims[2])
        glUniform1f(glGetUniformLocation(shader_procedural_wood, "ray_radius"), ray_radius)
        glUniform1f(glGetUniformLocation(shader_procedural_wood, "ray_occurance_ratio"), ray_occurance_ratio)
        glUniform3f(glGetUniformLocation(shader_procedural_wood, "ray_cell_dims"), ray_cell_dims[0], ray_cell_dims[1], ray_cell_dims[2])
        glUniform3f(glGetUniformLocation(shader_procedural_wood, "ray_color"), ray_color[0], ray_color[1], ray_color[2])

        draw_utils.draw_cuboid_with_procedural_texture(shader_procedural_wood, face_inds, 0.00*t, xrot0=xrot0, yrot0=yrot0, zrot0=zrot0)

        # Finalize
        img = render_utils.get_image_from_glbuffer(width,height)
        if t%5==0: gif_frame_images.append(img)
        glfw.swap_buffers(window)
        glfw.poll_events()
        t+=1

        if t>=tmax: break
    
    glfw.terminate()

    # save still image
    path = 'screenshot.png'
    img.save(path, 'PNG')
    print("Saved png in", path)

    # save gif image
    if tmax<=20:
        path = 'output.gif'
        gif_frame_images[0].save(path,save_all=True, append_images=gif_frame_images[1:], optimize=False, duration=1000, loop=0)
        print("Saved gif in", path)


if __name__ == "__main__":
    main()




    