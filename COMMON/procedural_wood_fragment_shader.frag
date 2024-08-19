#version 330 core
#define PI 3.1415926535897932384626433832795

in vec3 texCoords3D;
in vec3 fragPos;
in vec3 normal;
in mat3 TBN; 
in mat3 baseTBN; 

uniform vec3 viewPos;
uniform vec3 lightPos;

// pith 
uniform vec3 pith_org = vec3(0.6, 0.0, 0.4); //vec3(0.7, 0.2, 0.0); //vec3(0.2, 0.4, 0.0); //vec3(0.6, 0.0, 0.4); 
uniform vec3 pith_dir_in = vec3(0.5, 1.0, 0.0); //vec3(0.3, 0.0, 1.0); //vec3(0.5, 1.0, 0.0)

// annual rings
uniform float average_ring_distance = 0.1;
uniform vec3 earlywood_col = vec3(0.75,0.70,0.54);
uniform vec3 latewood_col = vec3(0.65,0.55,0.42);
uniform vec2 ring_col_mix_variables = vec2(0.4, 0.9);

//fibers
uniform float fiber_cell_dim = 0.005; //cell size

// pores
uniform float pore_radius = 0.15; //ratio of elipse size in cell
uniform float pore_equal_occurance_ratio = 0.8;
uniform float pore_ring_occurance_ratio = 0.2;
uniform vec3 pore_cell_dims = vec3(0.015, 0.015, 0.2); //cell radial, angular, height dimensions


// rays
uniform float ray_radius = 0.2; //ratio of elipse size in cell
uniform float ray_occurance_ratio = 0.5;
uniform vec3 ray_cell_dims = vec3(0.2, 0.015, 0.4); //cell radial, angular, height dimensions
uniform vec3 ray_color = vec3(0.66,0.56,0.40);

out vec4 fragColor;
// Noise functions


float noise_1d(vec3 p){
    float x = dot(p, vec3(12.3, 123.4, 234.5));
    float y = dot(p, vec3(345.6, 456.7, 567.8));
    float z = dot(p, vec3(678.9, 789.0, 890.1));
    vec3 noise = sin(vec3(x,y,z));
    noise *= 53758.4453;
    return fract(noise.x+noise.y+noise.z);
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

vec3 cylindricalToCartesian(vec3 cylCoords){
  float x = cylCoords.x*cos(2*PI*cylCoords.y);
  float y = cylCoords.x*sin(2*PI*cylCoords.y);
  float z = cylCoords.z;
  vec3 coords = vec3(x,y,z);
  return coords;
}

vec3 cartesianToCylindrical(vec3 coords){
  float r = length(vec2(coords.x, coords.y)); 
  float t = atan(coords.y, coords.x) / (2.0 * PI);  
  float h = coords.z;
  vec3 cylCoords = vec3(r,t,h);
  return cylCoords;
}


vec3 radial_cell_id(vec3 cylTexCoords, vec3 cell_dims, float i, float j){

    float ring_id = floor(cylTexCoords.x/cell_dims.x) + i;
    ring_id = max(ring_id,1.0);
    
    float angle_num = round(2*PI*ring_id*cell_dims.x/cell_dims.y);
    float angle_id = floor(cylTexCoords.y*angle_num) + j;
    angle_id = mod(angle_id, angle_num-1);

    float height_id = floor(cylTexCoords.z/cell_dims.z);

    vec3 cell_id = vec3(ring_id, angle_id, height_id);

    return cell_id;
}

vec3 radial_cell_in_coords(vec3 cylTexCoords, vec3 cell_dims){

    float ring_id = floor(cylTexCoords.x/cell_dims.x);
    float in_cell_rad = fract(cylTexCoords.x/cell_dims.x)-0.5;
    
    float angle_num = round(2*PI*ring_id*cell_dims.x/cell_dims.y);
    float angle_step = 1.0/angle_num;
    float in_cell_theta = fract(cylTexCoords.y*angle_num)-0.5;

    float in_cell_height = fract(cylTexCoords.z/cell_dims.z)-0.5;

    vec3 in_cell_cylindrical_coords = vec3(in_cell_rad, in_cell_theta, in_cell_height);

    return in_cell_cylindrical_coords;
}

vec3 radial_cell_ctr_coords(vec3 cell_id, vec3 cell_dims){

    float cell_ctr_rad = cell_dims.x*(cell_id.x+0.5);
    
    float angle_num = round(2*PI*cell_id.x*cell_dims.x/cell_dims.y);
    float angle_step = 1.0/angle_num;
    float cell_ctr_theta = angle_step*(cell_id.y+0.5);

    float cell_ctr_height = cell_dims.z*(cell_id.z+0.5);

    vec3 cell_ctr_cylindrical_coords = vec3(cell_ctr_rad, cell_ctr_theta, cell_ctr_height);
    vec3 cell_ctr_coords = cylindricalToCartesian(cell_ctr_cylindrical_coords);

    return cell_ctr_coords;
}

float ellipse_in_radial_cell(vec3 cylTexCoords, vec3 cell_dims, float occurance_ratio, float rad, float smooth_edge_ratio){

    vec3 cell_id = radial_cell_id(cylTexCoords, cell_dims, 0.0, 0.0);

    float noise_h = cylTexCoords.z + noise_1d(vec3(cell_id.x, cell_id.y, 0.0)); //additional height position noise
    vec3 cylTexCoords_temp = cylTexCoords;
    cylTexCoords_temp.z += noise_h;

    cell_id = radial_cell_id(cylTexCoords_temp, cell_dims, 0.0, 0.0);
    vec3 coords_in_cell = radial_cell_in_coords(cylTexCoords_temp, cell_dims);
   
    float f=1.0;

    float noise_factor = noise_1d(cell_id);
    if (noise_factor<occurance_ratio){
        vec3 pos_noise = sin(2*PI*noise_3d(cell_id));
        coords_in_cell += (0.5-rad)*pos_noise; 
        float vlen = length(coords_in_cell);
        f = smoothstep(rad,rad+smooth_edge_ratio*rad,vlen);
        //f = pos_noise.z;
    }

    

    return f;
}

vec3[3] vonoroi_radial_2d(vec3 cylCoords, vec3 cell_dims){

  // cartesian coordinates of pixel
  vec3 px_coords = cylindricalToCartesian(cylCoords);

  float min_dist = 100.0;
  vec3 min_dist_vec = vec3(99.0, 99.0, 99.0);
  vec3 closest_cell_id = vec3(0.0, 0.0, 0.0);
  vec3 closest_cell_ctr_coords = vec3(0.0, 0.0, 0.0);

  for(float i=-1.0; i<=1.0; i++){
    for(float j=-1.0; j<=1.0; j++){

      // Get cell id and cell center coordinates
      vec3 cell_id = radial_cell_id(cylCoords, cell_dims, i, j);
      vec3 cell_coords = radial_cell_ctr_coords(cell_id, cell_dims);

      // Add noise to cell center coordinates
      vec3 pos_noise = sin(2.0*PI*noise_3d(cell_id)) * cell_dims;
      cell_coords += 0.5 * pos_noise;

      // Ignore height
      cell_coords.z = px_coords.z;

      // Calcualte distance from pixel point to current cell center
      vec3 dist_vec = (cell_coords-px_coords)/cell_dims; 
      float dist = length(dist_vec);
      if (dist<=min_dist){
        min_dist = dist;
        min_dist_vec = dist_vec;
        closest_cell_id = cell_id;
        closest_cell_ctr_coords = cell_coords;
      }
    }
  }
  
  vec3 closest_cell_ctr_cylCoords = cartesianToCylindrical(closest_cell_ctr_coords);

  return vec3[3](min_dist_vec, closest_cell_id, closest_cell_ctr_cylCoords);
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

vec3 get_cylindrical_tex_coords(vec3 p, vec3 pith_org, vec3 pith_dir){
    vec3 closest_point_on_pith = closestPointOnLine(pith_org, pith_dir, p);
    float d = length(p-closest_point_on_pith);          //distance between current point and closest point on pith line
    vec3 h_st = pith_org - 2.0*pith_dir;                //set point from which the height will be calcualted
    float h = length(h_st-closest_point_on_pith);       //signed distance between closest point on line and pith origin
    vec3 base_vec = normalize(vec3(1.0,1.0,1.0));       //initiate a vector to compare vector angle to
    base_vec = normalize(cross(base_vec, pith_dir));    //make perpendicular to pith direction
    vec3 p_dir = normalize(p-closest_point_on_pith);    //vector from closest point on pith to pixel
    float a = acos(dot(base_vec, p_dir));               //angle around pith
    vec3 cross_vec = cross(base_vec, p_dir);
    float sign = sign(dot(pith_dir, cross_vec));
    a = a + (1.0 - sign) * PI;
    a = map(a, 0.0, 2.0*PI, 0, 1.0);                    //map angle from range 0-2pi to 0-1.0
    //Add some noise for distortion of distnace field
    vec3 distortion_noise = periodic_noise_3d(vec3(d,a,0.25*h)); //higher lower factor before h leads to more/less height-wise wavy-ness of the pattern
    d += 0.05*distortion_noise.x*d;
    a += 0.01*distortion_noise.y;
    d += 0.095; //ring center offset 
    return vec3(d,a,h);
}

float annual_ring_factor(vec3 cylTexCoords, float d, float ring_dist, vec2 transition_variables){

    //float c = mod(d+pnoise,ring_dist) / ring_dist; //old

    const int max_number_of_rings = 100;
    
    // list of ring rads
    float[max_number_of_rings] ring_rads;
    for (int i = 0; i < max_number_of_rings; i++) {

        ring_rads[i] = i * ring_dist;

        // add noise
        float pnoise = periodic_noise_3d(vec3(d, cylTexCoords.y,0.0)).x;
        pnoise += 2.0*periodic_noise_3d(vec3(d, d, d)).x;
        ring_rads[i] += 0.33*ring_dist*sin(pnoise);
    }

    // find nearest lower value
    int index = 0; //-1;  // Default if no lower value is found
    for (int i = 0; i < max_number_of_rings; i++) {
        if (ring_rads[i] <= d) {
            index = i;
        } else {
            break;
        }
    }

    // calcualte range and values for ring
    float ring_range = ring_rads[index+1]-ring_rads[index];
    float late_wood_start = ring_rads[index+1] - (1.0 - transition_variables[0])*ring_dist;
    float late_wood_peak =  ring_rads[index+1] - (1.0 - transition_variables[1])*ring_dist;
    
    // apply smoothsteps etc
    float c1 = smoothstep(late_wood_start, late_wood_peak, d);
    float c2 = 1.0-smoothstep(late_wood_peak, ring_rads[index+1], d);
    float c = min(c1, c2);
    
    return c;
}

float get_height_map_value(vec3 p, vec3 pith_org, vec3 pith_dir, vec3 p_dims, float p_rate, float p_rad, float f_dim, vec3 r_dims, float r_rate, float r_rad, float ring_dist, vec2 mix_variables){

    vec3 cylTexCoords = get_cylindrical_tex_coords(p, pith_org, pith_dir);
    float pc = ellipse_in_radial_cell(cylTexCoords, p_dims, p_rate, p_rad, 0.4);
    float rc = ellipse_in_radial_cell(cylTexCoords,r_dims, r_rate, r_rad, 0.01);
    vec3[3] fcd = vonoroi_radial_2d(cylTexCoords, vec3(f_dim,f_dim,99.0));
    //float ac = annual_ring_factor(cylTexCoords, fcd[1], ring_dist, mix_variables);
    float ac = annual_ring_factor(cylTexCoords, cylTexCoords.x, ring_dist, mix_variables);
    
    float fc = length(fcd[0]);
    fc = 0.5*(max(fc,ac) + fc);
    fc = 1.0-fc;
    fc = fc*0.02 + 0.9;

    ac = ac*0.1 + 0.9;
    
    float hc = pc*ac*fc;
    hc = mix(0.95, hc, rc);
    return hc;

}

// Main
void main() {
    
    // Get pixel position in relation to the pith (center line). 
    vec3 pith_dir = normalize(pith_dir_in);
    vec3 cylTexCoords = get_cylindrical_tex_coords(texCoords3D,pith_org,pith_dir);
    
    //Fibers (vonoroi)
    vec3[3] fiber_pattern = vonoroi_radial_2d(cylTexCoords, vec3(fiber_cell_dim,fiber_cell_dim,99.0));
    float fc = length(fiber_pattern[0]);
    vec3 f_cell_id =  fiber_pattern[1];
    vec3 f_cell_coords = fiber_pattern[2];
    //vec4 fiber_color = vec4(fc,fc,fc,0.0); //for debuggning

    // Annual rings
    //float c = annual_ring_factor(cylTexCoords, cylTexCoords.x, average_ring_distance, ring_col_mix_variables);
    float c = annual_ring_factor(cylTexCoords, f_cell_coords.x, average_ring_distance, ring_col_mix_variables);
    float noise_mix = 0.2*sin(noise_1d(f_cell_id));
    vec3 annual_ring_color = mix(earlywood_col, latewood_col, c+noise_mix); 
    //annual_ring_color = vec3(c,c,c); //for debugging

    // Pores
    // Constructing the pore 'grid'
    float pore_occurance_ratio = c*pore_ring_occurance_ratio + pore_equal_occurance_ratio;
    float pore_f = ellipse_in_radial_cell(cylTexCoords,pore_cell_dims, pore_occurance_ratio, pore_radius, 0.4);
    vec3 pore_color = 0.2*(1.0-vec3(pore_f,pore_f,pore_f));
    //vec3 pore_color = vec3(pore_f,pore_f,pore_f); // for debugging

    // Rays
    // Constructing the ray 'grid'
    float ray_f = ellipse_in_radial_cell(cylTexCoords,ray_cell_dims, ray_occurance_ratio, ray_radius, 0.1);
    //vec3 ray_color = vec3(ray_f,ray_f,ray_f); // for debuggung

    // Sample heights
    float stepSize = 0.01*fiber_cell_dim; // Adjust this based on your texture resolution
    float height_center = get_height_map_value( texCoords3D,                     pith_org, pith_dir, pore_cell_dims, pore_occurance_ratio, pore_radius, fiber_cell_dim, ray_cell_dims, ray_occurance_ratio, ray_radius, average_ring_distance, ring_col_mix_variables); // Your height function
    float height_x_plus = get_height_map_value( texCoords3D + stepSize * baseTBN[0], pith_org, pith_dir, pore_cell_dims, pore_occurance_ratio, pore_radius, fiber_cell_dim, ray_cell_dims, ray_occurance_ratio, ray_radius, average_ring_distance, ring_col_mix_variables);
    float height_x_minus = get_height_map_value(texCoords3D - stepSize * baseTBN[0], pith_org, pith_dir, pore_cell_dims, pore_occurance_ratio, pore_radius, fiber_cell_dim, ray_cell_dims, ray_occurance_ratio, ray_radius, average_ring_distance, ring_col_mix_variables);
    float height_y_plus = get_height_map_value( texCoords3D + stepSize * baseTBN[1], pith_org, pith_dir, pore_cell_dims, pore_occurance_ratio, pore_radius, fiber_cell_dim, ray_cell_dims, ray_occurance_ratio, ray_radius, average_ring_distance, ring_col_mix_variables);
    float height_y_minus = get_height_map_value(texCoords3D - stepSize * baseTBN[1], pith_org, pith_dir, pore_cell_dims, pore_occurance_ratio, pore_radius, fiber_cell_dim, ray_cell_dims, ray_occurance_ratio, ray_radius, average_ring_distance, ring_col_mix_variables);

    vec3 col_heightmap = vec3(height_center,height_center,height_center); // for debugging

    // Compute partial derivatives and normal thereafter
    float dHeightdx = height_x_plus - height_x_minus;
    float dHeightdy = height_y_plus - height_y_minus;
    vec3 computedNormal = normalize(vec3(-dHeightdx/stepSize, -dHeightdy/stepSize, 200.0));
    vec4 distorted_normal_color = vec4(computedNormal * 0.5 + 0.5, 1.0); // for debugging

    // Add normal map
    vec3 norm = normalize(TBN * computedNormal);
    //vec3 norm = normalize(normal); //for debuggning

    //Color pores by depth
    float dotProduct = dot(pith_dir, normalize(baseTBN[2]));
    float angle_between_1 = acos(dotProduct);
    dotProduct = dot(pith_dir, -normalize(baseTBN[2]));
    float angle_between_2 = acos(dotProduct);
    float angle_between = min(angle_between_1, angle_between_2);
    angle_between /= 0.6*PI;
    pore_color *= (1.0-angle_between);

    //Light/view direction setup
    vec3 lightDir = normalize(lightPos-fragPos);
    vec3 viewDir = normalize(viewPos-fragPos);
    vec3 reflectDir = reflect(-lightDir, norm);

    // Light properties
    float roughness = min(ray_f, 0.8-0.6*c);
    float ambientIntensity = 0.8;
    float diffuseIntensity = 0.5;
    float specularStrength = 0.5; // Controls the intensity of the specular highlight

    // Base color
    vec3 objectColor = annual_ring_color-pore_color;
    objectColor = mix(ray_color, objectColor, ray_f);

    // Ambient
    vec3 ambientColor = ambientIntensity * objectColor;

    // Diffuse 
    float diffuse = max(dot(norm, lightDir), 0.0);
    vec3 diffuseColor = diffuse * diffuseIntensity * objectColor;
        
    // Specular
    //roughness = 0.9; // for debugging
    float specular = pow(max(dot(viewDir, reflectDir), 0.0), (1.0 - roughness) * 128.0); // Roughness affects shininess
    vec3 specularColor = specularStrength * specular * vec3(1.0,1.0,1.0); // or use light color instead of object color

    // Combine diffuse, ambient, and specular
    vec3 color =  ambientColor + diffuseColor + specularColor;
    //color = diffuseColor;
    //color = specularColor;
    fragColor = vec4(color, 1.0);

    //All below for debugging
    //fragColor = annual_ring_color*fiber_color;
    //fragColor = fiber_color;
    //fragColor = vec4(annual_ring_color,1.0);
    //fragColor = vec4(pore_color,1.0);
    //fragColor = ray_color;
    //fragColor = vec4(d,a,h-2.0, 0.0); 
    //fragColor = vec4(col_heightmap,0.0);
    //fragColor = distorted_normal_color;
    //fragColor = vec4(roughness,roughness,roughness,0.0);
    //fragColor = vec4(lightPos,0.0);
}
