#version 330 core
#define PI 3.1415926535897932384626433832795

in vec3 out_position;

// pith 
uniform vec3 pith_org = vec3(0.2, 0.4, 0.0); //vec3(0.7, 0.2, 0.0); //vec3(0.2, 0.4, 0.0);
uniform vec3 pith_dir_in = vec3(0.5, 1.0, 0.0); //vec3(0.3, 0.0, 1.0); //vec3(0.5, 1.0, 0.0)

// annual rings
uniform float average_ring_distance = 0.1;
uniform vec3 earlywood_col = vec3(0.75,0.70,0.54);
uniform vec3 latewood_col = vec3(0.56,0.47,0.33);

//fibers
uniform float fiber_cell_dim = 0.005; //cell size

// pores
uniform float pore_radius = 0.2; //ratio of elipse size in cell
uniform float pore_occurance_rate = 0.75;
uniform vec3 pore_cell_dims = vec3(0.02, 0.02, 0.2); //cell radial, angular, height dimensions

// rays
uniform float ray_radius = 0.2; //ratio of elipse size in cell
uniform float ray_occurance_rate = 0.5;
uniform vec3 ray_cell_dims = vec3(0.15, 0.02, 0.15); //cell radial, angular, height dimensions
uniform vec3 ray_col = vec3(0.66,0.59,0.35);


out vec4 fragColor;

// Noise functions

float noise_1d(float p){
    float x = p*124477.3;
    float noise = sin(x);
    noise *= 53758.4453;
    return fract(noise);
}

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
    float x = dot(p, vec3(1299.3, 123.4, 234.5));
    float y = dot(p, vec3(345.6, 4956.7, 567.8));
    float z = dot(p, vec3(6798.9, 789.0, 890.1));
    vec3 noise = sin(vec3(x,y,z));
    noise *= 53758.4453;
    return fract(noise);
}

vec3 periodic_noise_3d(vec3 p) {
    // Create noise for each component of vec3 independently
    float noiseX = sin(2.0 * PI * p.x) * cos(2.0 * PI * p.y) * sin(2.0 * PI * p.z);
    noiseX += 0.5 * sin(4.0 * PI * p.x) * cos(4.0 * PI * p.y) * sin(4.0 * PI * p.z);
    noiseX += 0.25 * sin(8.0 * PI * p.x) * cos(8.0 * PI * p.y) * sin(8.0 * PI * p.z);

    float noiseY = cos(2.0 * PI * p.x) * sin(2.0 * PI * p.y) * cos(2.0 * PI * p.z);
    noiseY += 0.5 * cos(4.0 * PI * p.x) * sin(4.0 * PI * p.y) * cos(4.0 * PI * p.z);
    noiseY += 0.25 * cos(8.0 * PI * p.x) * sin(8.0 * PI * p.y) * cos(8.0 * PI * p.z);

    float noiseZ = sin(2.0 * PI * p.x + 1.0) * cos(2.0 * PI * p.y + 1.0) * sin(2.0 * PI * p.z + 1.0);
    noiseZ += 0.5 * sin(4.0 * PI * p.x + 1.0) * cos(4.0 * PI * p.y + 1.0) * sin(4.0 * PI * p.z + 1.0);
    noiseZ += 0.25 * sin(8.0 * PI * p.x + 1.0) * cos(8.0 * PI * p.y + 1.0) * sin(8.0 * PI * p.z + 1.0);

    // Combine into vec3 and return the noise
    return vec3(noiseX, noiseY, noiseZ);
}

float periodic_noise_1d(vec2 p) {
    // Create a basic periodic noise using sine and cosine
    float noise = sin(2.0 * PI * p.x) * cos(2.0 * PI * p.y);
    noise += 0.5 * sin(4.0 * PI * p.x) * cos(4.0 * PI * p.y);
    noise += 0.25 * sin(8.0 * PI * p.x) * cos(8.0 * PI * p.y);
    
    // Normalize to range [0, 1]
    return 0.5 * (noise + 1.0);
}

// Supporting functions

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

//pore
float ellipse_in_even_radial_cell(float d, float a, float h, vec3 cell_dims, float occurance_rate, float rad, float smooth_edge_ratio){

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
    //occurance_rate=1.0;
    if (noise_factor<occurance_rate){
        vec3 pos_noise = sin(2*PI*noise_3d(cell_id));
        coords_in_cell += (0.5-rad)*pos_noise;  
        float vlen = length(coords_in_cell);
        f = smoothstep(rad,rad+smooth_edge_ratio*rad,vlen);
    }
    //return (ring_id + angle_id)/(angle_num);
    return f;
}

//ray
float ellipse_in_radial_cell(float d, float a, float h, vec3 cell_dims, float occurance_rate, float rad, float smooth_edge_ratio){
    
    float angle_num = 128;
    float angle_step = 1.0/angle_num;
    float angle_id = floor(a*angle_num);
    float cell_a = fract(a*angle_num)-0.5;

    float ring_id = ceil(d/cell_dims.x);
    
    float angle_num_even = round(ring_id*2*PI*cell_dims.x/cell_dims.y);
    float angle_step_even = 1.0/angle_num_even;
    float width_correction_ratio = angle_step_even/angle_step;
    cell_a = cell_a*width_correction_ratio;
    float next = pow(2, ceil(log(width_correction_ratio)/log(2)));
    angle_id = next*floor((angle_id+floor(next/2))/next);
    angle_id = mod(angle_id,angle_num);

    angle_step = 1.0/(angle_num/next);
    cell_a = fract(a*(angle_num/next))-0.5;

    float noise_d = d + noise_1d(angle_id);//additional distance position noise
    ring_id = ceil(noise_d/cell_dims.x);
    float cell_d = fract(noise_d/cell_dims.x)-0.5;
    
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


vec2[2] radial_cell(float d, float a, float cell_dim, float i, float j){

    float ring_id = ceil(d/cell_dim) + i;
    ring_id = max(ring_id,1.0);
    float cell_d = (ring_id-0.5)*cell_dim;

    float angle_num = round(ring_id*2*PI);
    float angle_step = 1.0/angle_num;
    float angle_id = mod(floor(a*angle_num) + j, angle_num);
    float cell_a = angle_id*angle_step + 0.5*angle_step;

    vec2 cell_id = vec2(ring_id, angle_id);
    
    vec2 my_noise = noise_2d(cell_id);
    my_noise = 0.5*sin(my_noise);
    cell_d += cell_dim*my_noise.x;
    cell_a += angle_step*my_noise.y;

    float cell_x = cell_d*cos(2*PI*cell_a);
    float cell_y = cell_d*sin(2*PI*cell_a);
    vec2 cell_coords = vec2(cell_x,cell_y);

    return vec2[2](cell_id, cell_coords);
}

float[3] vonoroi_radial_grid(float d, float a, float cell_dim){

  // cartesian coordinates of pixel
  float px_x = d*cos(2*PI*a);
  float px_y = d*sin(2*PI*a);
  vec2 px_coords = vec2(px_x,px_y);

  float min_dist = 100.0;
  vec2 closest_cell_coord = vec2(0.0,0.0);


  for(float i=-1.0; i<=1.0; i++){
    for(float j=-1.0; j<=1.0; j++){
      vec2[2] cell = radial_cell(d, a, cell_dim, i, j);
      vec2 cell_id = cell[0];
      vec2 cell_coords = cell[1];
      vec2 my_noise = noise_2d(cell_id + cell_coords);
      cell_coords = cell_coords + 0.2*sin(2*PI*my_noise)*cell_dim;
      float dist = length(cell_coords-px_coords)/cell_dim;
      min_dist = min(min_dist, dist);
      if (dist==min_dist){
        closest_cell_coord = cell_coords;
      }
    }
  }

  float rad_coord_d = length(vec2(closest_cell_coord.x, closest_cell_coord.y));
  float rad_coord_a = atan(closest_cell_coord.y, closest_cell_coord.x) / (2.0 * PI);
    
  return float[3](min_dist, rad_coord_d, rad_coord_a);
}

// Vonoroi
float vonoroi_grid(float x, float y, float cell_dim){
  vec2 grid_pt = vec2(x,y)/cell_dim;
  vec2 grid_id = floor(grid_pt);
  vec2 grid_coords = fract(grid_pt)-0.5;
  float min_dist = 100.0;
  for(float i=-1.0; i<=1.0; i++){
    for(float j=-1.0; j<=1.0; j++){
        vec2 adj_grid_coords = vec2(i,j);
        vec2 my_noise = noise_2d(grid_id + adj_grid_coords);
        vec2 pt_on_adj_grid = adj_grid_coords + 0.5*sin(my_noise);
        float dist = length(grid_coords - pt_on_adj_grid);
        min_dist = min(min_dist, dist);
    }
  }
  return min_dist;
}


// Normal from neighborhood of height values
vec3 calculateNormal(float h1, float h2, float h3, float h4, float h, float h5, float h6, float h7, float h8) {
    // Sobel operator to compute x and y gradients
    float dx = h3 + 2.0 * h5 + h8 - h1 - 2.0 * h4 - h6;
    float dy = h1 + 2.0 * h2 + h3 - h6 - 2.0 * h7 - h8;

    // Normal vector is the cross product of the gradient with the z axis
    vec3 normal = normalize(vec3(-dx, -dy, 1.0));
    
    return normal;
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

    //Add some noise for distortion of distnace field
    vec3 distortion_noise = periodic_noise_3d(vec3(d,a,h));
    d += 0.025*distortion_noise.x;
    a += 0.03*distortion_noise.y;
    
    //Fibers (vonoroi)
    float[3] fiber_pattern = vonoroi_radial_grid(d, a, fiber_cell_dim);
    float min_dist = fiber_pattern[0];
    float fiber_cell_d = fiber_pattern[1];
    float fiber_cell_a = fiber_pattern[2];
    
    float fc = min_dist;
    //vec4 fiber_color = clamp(0.85+vec4(fc, fc, fc, 0.0),0.0,1.0);
    vec4 fiber_color = vec4(min_dist,min_dist,min_dist,0.0);

    // Annual rings
    float pnoise = 0.02*periodic_noise_1d(vec2(fiber_cell_d, a));
    pnoise += 0.075*periodic_noise_1d(vec2(fiber_cell_d, fiber_cell_d));

    float c = mod(fiber_cell_d+pnoise,average_ring_distance) / average_ring_distance;
    //float c = mod(d,average_ring_distance) / average_ring_distance;
    c = pow(c,4);
    float noise_mix = 0.3*sin(noise_1d(vec2(fiber_cell_d,fiber_cell_a)));
    vec3 col = mix(earlywood_col, latewood_col, c+noise_mix); 
    vec3 noise_col = noise_3d(vec3(fiber_cell_d,fiber_cell_a,0.0));
    col += 0.025*noise_col;
    vec4 annual_ring_color = vec4(col, 0.0);
    //annual_ring_color = vec4(c,c,c,0.0); //for debugging

    // Pores
    // Constructing the pore 'grid'
    float pore_f = ellipse_in_even_radial_cell(d,a,h,pore_cell_dims, pore_occurance_rate, pore_radius, 0.4);
    vec4 pore_color = 0.2*(1.0-vec4(pore_f,pore_f,pore_f,0.0));
    //vec4 pore_color = vec4(pore_f,pore_f,pore_f,0.0);

    // Rays
    // Constructing the ray 'grid'
    //float ray_f = ellipse_in_radial_cell(d,a,h,ray_cell_dims, ray_occurance_rate, ray_radius, 0.2);
    float ray_f = ellipse_in_even_radial_cell(d,a,h,ray_cell_dims, ray_occurance_rate, ray_radius, 0.4);
    vec4 ray_color = vec4(ray_col,0.0);
    //vec4 ray_color = vec4(ray_f,ray_f,ray_f,0.0);

    
    fragColor = annual_ring_color-pore_color;
    fragColor = mix(ray_color, fragColor, ray_f);
    //fragColor = annual_ring_color*fiber_color;
    //fragColor = fiber_color;
    //fragColor = annual_ring_color;
    //fragColor = pore_color;
    //fragColor = ray_color;
    // = vec4(d,a,h-2.0, 0.0); //for debugging


}
