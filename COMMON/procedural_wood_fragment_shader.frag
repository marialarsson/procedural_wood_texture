#version 330 core
#define PI 3.1415926535897932384626433832795

in vec3 out_position;

// pith 
uniform vec3 pith_org = vec3(0.2, 0.0, 0.0);
uniform vec3 pith_dir_in = vec3(0.0, 0.2, 1.0);

// annual rings
uniform float average_ring_distance = 0.1;
uniform vec3 earlywood_col = vec3(0.79,0.74,0.6);
uniform vec3 latewood_col = vec3(0.52,0.42,0.29);

// pores
uniform float pore_radius = 0.3; //ratio of elipse size in cell
uniform float pore_occurance_rate = 0.8;
uniform vec3 pore_cell_dims = vec3(0.03, 0.03, 0.3); //cell radial, angular, height dimensions

// rays
uniform float ray_radius = 0.45; //ratio of elipse size in cell
uniform float ray_occurance_rate = 0.1;
uniform vec3 ray_cell_dims = vec3(0.2, 0.02, 0.2); //cell radial, angular, height dimensions


out vec4 fragColor;

// Supporting functions


float noise_1d(vec2 p){
    float x = dot(p, vec2(12.3, 123.4));
    float y = dot(p, vec2(345.6, 456.7));
    vec2 noise = sin(vec2(x,y));
    noise *= 53758.4453;
    return fract(noise.x+noise.y);
}

float noise_1d(vec3 p){
    float x = dot(p, vec3(12.3, 123.4, 234.5));
    float y = dot(p, vec3(345.6, 456.7, 567.8));
    float z = dot(p, vec3(678.9, 789.0, 890.1));
    vec3 noise = sin(vec3(x,y,z));
    noise *= 53758.4453;
    return fract(noise.x+noise.y+noise.z);
}

vec2 noise_2d(vec2 p){
    float x = dot(p, vec2(123.4, 234.5));
    float y = dot(p, vec2(345.6, 456.7));
    vec2 noise = sin(vec2(x,y));
    noise *= 43758.5453;
    return fract(noise);
}

vec3 noise_3d(vec3 p){
    float x = dot(p, vec3(12.3, 123.4, 234.5));
    float y = dot(p, vec3(345.6, 456.7, 567.8));
    float z = dot(p, vec3(678.9, 789.0, 890.1));
    vec3 noise = sin(vec3(x,y,z));
    noise *= 53758.4453;
    return fract(noise);
}

float map(float value, float min1, float max1, float min2, float max2) {
  return min2 + (value - min1) * (max2 - min2) / (max1 - min1);
}

float pointLineDistance(vec3 ro, vec3 rd, vec3 p){
  float t = dot(p - ro, rd); //parameter (t) of closest point on ray from center
  vec3 cp = ro + rd * t;     //closest point (cp) on ray from center
  return length(p-cp);       //distance between center (p) and closest point (cpt)
}

vec3 closestPointOnLine(vec3 ro, vec3 rd, vec3 p){
  float t = dot(p - ro, rd); //parameter (t) of closest point on ray from center
  vec3 cp = ro + rd * t;     //closest point (cp) on ray from center
  return cp;
}

float ellipse_in_radial_cell(float d, float a, float h, vec3 cell_dims, float occurance_rate, float rad, float smooth_edge_ratio){

    float ring_id = ceil(d/cell_dims.x);
    float cell_d = fract(d/cell_dims.x)-0.5;

    float angle_num = round(ring_id*2*PI*cell_dims.x/cell_dims.y);
    float angle_id = floor(a*angle_num);
    float cell_a = fract(a*angle_num)-0.5;

    float noise_h = h + noise_1d(vec2(ring_id,angle_id));//additional height position noise
    float height_id = floor(noise_h/cell_dims.z);
    float cell_h = fract(noise_h/cell_dims.z)-0.5;

    vec3 cell_id = vec3(ring_id, angle_id, height_id);
    vec3 coords_in_cell = vec3(cell_d, cell_a, cell_h);

    float f=1.0;

    float noise_factor = noise_1d(cell_id);
    if (noise_factor<occurance_rate){
        coords_in_cell += (0.5-rad)*noise_3d(cell_id);  
        float vlen = length(coords_in_cell);
        f = smoothstep(rad,rad+smooth_edge_ratio*rad,vlen);
    }
    
    return f;
}


// Main

void main() {

    vec3 p = out_position;
    //vec4 col = vec4(p, 0.0); //for debugging 3d texture coordinates

    // Analyze pixel position in relation to the pith (center line). 
    // Distnace (d), height (h), angle (a)
    vec3 pith_dir = normalize(pith_dir_in);
    vec3 closest_point_on_pith = closestPointOnLine(pith_org, pith_dir, p);
    float d = length(p-closest_point_on_pith);          //distance between current point and closest point on pith line
    vec3 h_st = pith_org - 2.0*pith_dir;                //set point from which the height will be calcualted
    float h = length(h_st-closest_point_on_pith);       //signed distance between closest point on line and pith origin
    vec3 base_vec = normalize(vec3(1.0,1.0,1.0));       //initiate a vector to compare vector angle to
    base_vec = normalize(cross(base_vec, pith_dir));    //make perpendicular to pith direction
    vec3 p_dir = normalize(p-closest_point_on_pith);    //vector from closest point on pith to pixel
    float a;                                            //angle around pith
    if(length(p_dir-base_vec)<0.0000001){               //edge cases
      a=0.0;
    }else if(length(p_dir-base_vec)>1.9999999){
      a=PI;
    }else{
      a = acos(dot(base_vec, p_dir));
      vec3 cross_vec = cross(base_vec, p_dir);
      if (dot(pith_dir, cross_vec) < 0) {
        a = 2.0*PI-a;
      }
    }
    a = map(a, 0.0, 2.0*PI, 0, 1.0); //map omega from range 0-2pi to 0-1.0

    // Annual rings
    //float a = sin(d/average_ring_distance);
    float c = mod(d,average_ring_distance) / average_ring_distance;
    c = c*c*c;
    //vec4 annual_ring_color = vec4(1.0, 1.0, c, 0.0);
    c = 1.0-c;
    vec4 annual_ring_color = vec4(c, c, c, 0.0);


    //Fibers (vonoroi noise)
    float fiber_grid_dim = 0.01;
    vec2 grid_pt = vec2(d*cos(2*PI*a),d*sin(2*PI*a))/fiber_grid_dim;
    vec2 grid_id = floor(grid_pt);
    vec2 grid_coords = fract(grid_pt)-0.5;
    float min_dist_from_px = 100.0;
    for(float i=-1.0; i<=1.0; i++){
        for(float j=-1.0; j<=1.0; j++){
            vec2 adj_grid_coords = vec2(i,j);
            vec2 my_noise = noise_2d(grid_id + adj_grid_coords);
            vec2 pt_on_adj_grid = adj_grid_coords + 0.5*sin(my_noise);
            float dist = length(grid_coords - pt_on_adj_grid);
            min_dist_from_px = min(min_dist_from_px, dist);
        }
    }
    float fc = 1.25*min_dist_from_px;
    vec4 fiber_color = vec4(fc, fc, fc, 0.0);
    //vec4 fiber_color = vec4(grid_coords,0.0,0.0);

    // Pores
    // Constructing the pore 'grid'
    float pore_f = 0.5 + ellipse_in_radial_cell(d,a,h,pore_cell_dims, pore_occurance_rate, pore_radius, 0.2);
    vec4 pore_color = vec4(pore_f,pore_f,pore_f,0.0);

    // Rays
    // Constructing the ray 'grid'
    float ray_f = 0.3 + ellipse_in_radial_cell(d,a,h,ray_cell_dims, ray_occurance_rate, ray_radius, 0.2);
    vec4 ray_color = vec4(ray_f,ray_f,ray_f,0.0);
    
    fragColor = annual_ring_color*pore_color*fiber_color*ray_color;
    //fragColor = fiber_color;
    //fragColor = annual_ring_color;
    //fragColor = pore_color;
    //fragColor = ray_color;
}
