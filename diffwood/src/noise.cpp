#include "noise.h"

#include "thread.h"


namespace diffwood {

namespace cuda {

extern
void periodic_noise_3d(int num, const float *p, float *out);

} // namespace cuda

void periodic_noise_3d(int num, const float *p, float *out, bool is_cuda)
{
    if (is_cuda) {
#if defined(DIFFWOOD_CUDA)
        cuda::periodic_noise_3d(num, p, out);
#else
        fprintf(stderr, "CUDA is not supported\n");
#endif
    }
    else {
        periodic_noise_3d_op func{ num, p, out };
        cpu::parallel_for(num, [&func] (int idx, int tid) { func(idx); });
    }
}

} // namespace diffwood


