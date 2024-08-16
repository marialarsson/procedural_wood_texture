#include "noise.h"

#include "common.cuh"


namespace diffwood {
namespace cuda {

void periodic_noise_3d(int num, const float *p, float *out)
{
    cuda::parallel_for(num, periodic_noise_3d_op{ num, p, out });
}

} // namespace cuda
} // namespace diffwood


