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




vec2[2] radial_cell(float d, float a, float cell_dim, float i, float j){

    float ring_id = ceil(d/cell_dim) + i;
    ring_id = max(ring_id,1.0);
    float cell_d = (ring_id-0.5)*cell_dim;

    float angle_num = round(ring_id*2*PI);
    float angle_step = 1.0/angle_num;
    float angle_id = mod(floor(a*angle_num) + j, angle_num);
    float cell_a = angle_id*angle_step + 0.5*angle_step;

    vec2 cell_id = vec2(ring_id, angle_id);
    
    vec3 my_noise = periodic_noise_3d(vec3(cell_id,0.0));
    my_noise = 0.5*sin(my_noise);
    cell_d += cell_dim*my_noise.x;
    cell_a += angle_step*my_noise.y;

    float cell_x = cell_d*cos(2*PI*cell_a);
    float cell_y = cell_d*sin(2*PI*cell_a);
    vec2 cell_coords = vec2(cell_x,cell_y);

    return vec2[2](cell_id, cell_coords);
}

      min_dist = min(min_dist, dist);
      if (dist==min_dist){
        closest_cell_coord = cell_coords;
      }