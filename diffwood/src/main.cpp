#include <cstdio>
#include <vector>
#include <stdexcept>
#include <numeric>
#include <algorithm>

#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>

#include "diffwood.h"


namespace nb = nanobind;
using namespace nb::literals;

template<typename T> using TensorX = nb::ndarray<nb::pytorch, T, nb::shape<-1>, nb::c_contig>;
template<typename T> using TensorXX = nb::ndarray<nb::pytorch, T, nb::shape<-1, -1>, nb::c_contig>;
template<typename T> using TensorXXX = nb::ndarray<nb::pytorch, T, nb::shape<-1, -1, -1>, nb::c_contig>;
template<typename T, long dim0> using TensorN = nb::ndarray<nb::pytorch, T, nb::shape<dim0>, nb::c_contig>;
template<typename T, long dim1> using TensorXN = nb::ndarray<nb::pytorch, T, nb::shape<-1, dim1>, nb::c_contig>;
template<typename T, long dim0> using TensorNX = nb::ndarray<nb::pytorch, T, nb::shape<dim0, -1>, nb::c_contig>;
template<typename T, long dim0, long dim1> using TensorNN = nb::ndarray<nb::pytorch, T, nb::shape<dim0, dim1>, nb::c_contig>;
template<typename T, long dim2> using TensorXXN = nb::ndarray<nb::pytorch, T, nb::shape<-1, -1, dim2>, nb::c_contig>;

#define CHECK_TENSOR_SIZE(tensor, dim, size) if (tensor.shape(dim) != size) throw std::runtime_error(#tensor " has an invalid tensor size")
#define CHECK_CUDA_SUPPORT(is_cuda) if (is_cuda && !diffwood::cuda::is_available()) throw std::runtime_error("CUDA is not supported")

namespace {

void periodic_noise_3d(TensorXN<float, 3> p,
                       TensorXN<float, 3> out)
{
    const bool is_cuda = p.device_type() == nb::device::cuda::value;
    CHECK_CUDA_SUPPORT(is_cuda);

    const auto num = static_cast<int>(p.shape(0));
    CHECK_TENSOR_SIZE(out, 0, num);

    diffwood::periodic_noise_3d(num, p.data(), out.data(), is_cuda);
}

} // namespace


NB_MODULE(_diffwoodcore, m)
{
    m.def("cuda_is_available", [] { return diffwood::cuda::is_available(); });

    m.def("periodic_noise_3d", &::periodic_noise_3d);
}

