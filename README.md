# procedural_wood_texture
glwf/glsl implementation of procedural wood texture

![Alt text](./output_main.gif)



## Texture coordinates

<p float="center">
  <img src="/screenshot_texcoords.png" width="150" />
  <img src="/screenshot_modified_coords.png" width="150" />
</p>

1: Input 3D coordinates (x,y,z). 2: Modified cylindrical coordinates (d,a,h) - distance from pith (d), angle around pith (a), height along pith (h).


## Ring construction

<p float="center">
  <img src="/screenshot_rings_1.png" width="150" />
  <img src="/screenshot_rings_2.png" width="150" />
  <img src="/screenshot_rings_3.png" width="150" />
</p>

1: Distance field with a modulus operator at a constant value. 2: Noise added to ring distances. 3: Distortion noise added.

## Fiber construction

<p float="center">
  <img src="/screenshot_fiber_1.png" width="150" />
  <img src="/screenshot_fiber_2.png" width="150" />
  <img src="/screenshot_fiber_3.png" width="150" />
  <img src="/screenshot_fiber_4.png" width="150" />
</p>

1: Radial vonoroi cells (scaled up for visibility). 2: Add noise to cell center point positions (within cell boundary). 3: Scale down. 4: Distortion noise added.


## Pore construction

<p float="center">
  <img src="/screenshot_pore_1.png" width="150" />
  <img src="/screenshot_pore_2.png" width="150" />
  <img src="/screenshot_pore_3.png" width="150" />
  <img src="/screenshot_pore_4.png" width="150" />
  <img src="/screenshot_pore_5.png" width="150" />
</p>

1: Base pattern of pores. 2: Pore position in cell noise added. 3: Pore height offset noise added. 4: Distortion noise added. 5: Occurance rate added.

## Ray construation

<p float="center">
  <img src="/screenshot_ray_1.png" width="150" />
  <img src="/screenshot_ray_2.png" width="150" />
  <img src="/screenshot_ray_3.png" width="150" />
  <img src="/screenshot_ray_4.png" width="150" />
  <img src="/screenshot_ray_5.png" width="150" />
</p>

1: Base pattern of rays. 2: Ray position in cell noise added. 3: Ray height offset noise added. 4: Distortion noise added. 5: Occurance rate added.


## Normals

<p float="center">
  <img src="/screenshot_height_map.png" width="150" />
  <img src="/screenshot_local_normals.png" width="150" />
</p>

1: Height map based on fibers and pores. 2: Normalmap calcualted based on height map.


## Putting everything together

<p float="center">
  <img src="/screenshot_rings_fibers_1.png" width="150" />
  <img src="/screenshot_rings_fibers_2.png" width="150" />
  <img src="/screenshot_pore.png" width="150" />
  <img src="/screenshot_ray.png" width="150" />
  <img src="/screenshot_normals.png" width="150" />
</p>

1: Combining fibers and annual rings (let fibers be "pixels" of the annual rings). 2: Blend two colors depending on greyscale value in previous. 3: Add pores. 4: Add rays. 5: Add normal map. 

## Parameter overview

<p float="center">
  <img src="/screenshot_random_pith.png" width="150" />
  <img src="/screenshot_random_rings.png" width="150" />
  <img src="/screenshot_random_fibers.png" width="150" />
  <img src="/screenshot_random_pores.png" width="150" />
  <img src="/screenshot_random_rays.png" width="150" />
  <img src="/screenshot_random_all.png" width="150" />
</p>

1: Random pith origina and direction. 2: Random annual ring distances and transitions (constant colors). 3: Random fiber size and mix. 4: Random pore size and occurance rate. 5: Random ray size and occurance rate (constant color). 6: Random all above.

## To do:s

Set up lights

Import information from step 1 of the optimization (pith center line, etc.).

Heartwood/sapwood difference.

Knots.

Consider changing ray construction to enable more raidus-wise overlap.

...
