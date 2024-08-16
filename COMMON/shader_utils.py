import numpy as np
from OpenGL.GL import *
from scipy.ndimage import zoom


def get_vertex_shader():
    VERTEX_SHADER = """

            #version 330 core

            layout(location = 0) in vec3 in_position;
            layout (location = 1) in vec2 in_tex_coord;
            layout (location = 2) in vec3 in_normal;

            uniform mat4 model;
            uniform mat4 view;
            uniform mat4 projection;
            uniform mat4 transform;

            out vec3 fragPos;
            out vec3 normal;
            out vec3 texCoords3D;
            out mat3 TBN; 
            out mat3 baseTBN;
            

            void main() {

                //3d texture coordinates
                texCoords3D = in_position;

                // Transform position from object space to world space
                vec4 worldPosition = model * vec4(in_position, 1.0);
                fragPos = worldPosition.xyz;

                //Tangent-Binormal-Normal matrix (absolute)
                vec3 baseTangent = cross( normalize( vec3(0.5,0.5,0.5) ), normalize(in_normal) );
                vec3 baseBinormal =  normalize(cross(in_normal, baseTangent));
                baseTBN = mat3(baseTangent, baseBinormal, in_normal);

                // Transform normal from object space to world space
                vec3 worldNormal = normalize(mat3(transpose(inverse(model))) * in_normal);
                normal = worldNormal;

                //Tangent-Binormal-Normal matrix (transformed)
                vec3 tangent = normalize( mat3(transpose(inverse(model))) * baseTangent );
                vec3 binormal = normalize(cross(normal, tangent));
                TBN = mat3(tangent, binormal, normal);

                // Transform position from world space to screen space
                gl_Position = projection * view * worldPosition;

            }
          """
    return VERTEX_SHADER



def get_procedural_wood_fragment_shader():

    FRAGMENT_SHADER = open("COMMON//procedural_wood_fragment_shader.frag",'r').read()

    return FRAGMENT_SHADER