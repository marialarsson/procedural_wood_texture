import numpy as np
import math
import pyrr
from OpenGL.GL import *


def update_rotation(shader, t, xrot0=-math.pi/5, yrot0=math.pi/4, zrot0=0, xrotf=0.1, yrotf=0.16, zrotf=0.0, print_rot=False):

    glUseProgram(shader)
    rot_x = pyrr.Matrix44.from_x_rotation(xrot0 + xrotf * t)
    rot_y = pyrr.Matrix44.from_y_rotation(yrot0 + yrotf * t)
    rot_z = pyrr.Matrix44.from_z_rotation(zrot0 + zrotf * t)
    modelLoc = glGetUniformLocation(shader, "model")
    glUniformMatrix4fv(modelLoc, 1, GL_FALSE,  rot_x * rot_y * rot_z)
    

    #transformLoc = glGetUniformLocation(shader, "transform")
    #glUniformMatrix4fv(transformLoc, 1, GL_FALSE, rot_x * rot_y * rot_z)


def draw_cuboid_with_procedural_texture(shader, inds, t, offset=0,  xrot0=-math.pi/5, yrot0=math.pi/4, zrot0=0.0, xrotf=0.1, yrotf=0.16, zrotf=0.0):
    
    glUseProgram(shader)
    update_rotation(shader, t, xrot0=xrot0, yrot0=yrot0, zrot0=zrot0, xrotf=xrotf, yrotf=yrotf, zrotf=zrotf)  
    glDrawElements(GL_TRIANGLES, len(inds), GL_UNSIGNED_INT, ctypes.c_void_p(offset * inds.itemsize))

    

