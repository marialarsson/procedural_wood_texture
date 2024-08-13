# procedural_wood_texture
glwf/glsl implementation of procedural wood texture

![Alt text](./screenshot_fiber_ring_pore_ray_offset_angle.png)


## Fiber construction

<p float="center">
  <img src="/screenshot_fiber_1.png" width="100" />
  <img src="/screenshot_fiber_2.png" width="100" />
  <img src="/screenshot_fiber_3.png" width="100" />
  <img src="/screenshot_fiber_4.png" width="100" />
</p>

## Ring construction

<p float="center">
  <img src="/screenshot_rings_1.png" width="100" />
  <img src="/screenshot_rings_2.png" width="100" />
  <img src="/screenshot_rings_3.png" width="100" />
</p>

## Pore construction

<p float="center">
  <img src="/screenshot_pore_1.png" width="100" />
  <img src="/screenshot_pore_2.png" width="100" />
  <img src="/screenshot_pore_3.png" width="100" />
  <img src="/screenshot_pore_4.png" width="100" />
</p>

## Ray construation

<p float="center">
  <img src="/screenshot_ray_1.png" width="100" />
  <img src="/screenshot_ray_2.png" width="100" />
  <img src="/screenshot_ray_3.png" width="100" />
  <img src="/screenshot_ray_4.png" width="100" />
</p>

## Putting everything together

<p float="center">
  <img src="/screenshot_rings_fibers_1.png" width="100" />
  <img src="/screenshot_rings_fibers_2.png" width="100" />
  <img src="/screenshot_fiber_ring_pore.png" width="100" />
  <img src="/screenshot_fiber_ring_pore_ray.png" width="100" />
</p>



## Changing pith origin and orientation

<p float="center">
  <img src="/screenshot_fiber_ring_pore_ray_offset.png" width="100" />
  <img src="/screenshot_fiber_ring_pore_ray_offset_angle.png" width="100" />
</p>



##To dos

Normal map (especially pores will look better if rendered with a normal map)
- Create the normal map from height field
- Set up lights

Import information from step 1 of the optimization (pith center line, etc.).

Heartwood/sapwood difference.

Knots.

Consider changing ray construction to enable more raidus-wise overlap.

...
