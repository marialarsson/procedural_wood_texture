#include "diffwood.h"


namespace diffwood::cuda {

bool is_available()
{
#if defined(DIFFWOOD_CUDA)
    return true;
#else
    return false;
#endif
}

} // namespace diffwood::cuda


