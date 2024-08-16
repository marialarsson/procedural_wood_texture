#pragma once

#include "common.h"


namespace diffwood {

void periodic_noise_3d(int num, const float *p, float *out, bool is_cuda);

class periodic_noise_3d_op {
public:
    const int num;
    const float *const p;
    float *const out;

    periodic_noise_3d_op(int num, const float *p, float *out)
            : num{ num }, p{ p }, out{ out } { }

    HOST_DEVICE inline
    void operator()(int idx) const
    {
        if (idx >= num)
            return;

        // Create noise for each component of vec3 independently
        constexpr auto PI = Pi<float>;
        const auto px = p[idx * 3 + 0];
        const auto py = p[idx * 3 + 1];
        const auto pz = p[idx * 3 + 2];

        float noiseX = std::sin(2.0f * PI * px) * std::cos(2.0f * PI * py) * std::sin(2.0f * PI * pz);
        noiseX += 0.5f * std::sin(4.0f * PI * px) * std::cos(4.0f * PI * py) * std::sin(4.0f * PI * pz);
        noiseX += 0.25f * std::sin(8.0f * PI * px) * std::cos(8.0f * PI * py) * std::sin(8.0f * PI * pz);

        float noiseY = std::cos(2.0f * PI * px) * std::sin(2.0f * PI * py) * std::cos(2.0f * PI * pz);
        noiseY += 0.5f * std::cos(4.0f * PI * px) * std::sin(4.0f * PI * py) * std::cos(4.0f * PI * pz);
        noiseY += 0.25f * std::cos(8.0f * PI * px) * std::sin(8.0f * PI * py) * std::cos(8.0f * PI * pz);

        float noiseZ = std::sin(2.0f * PI * px + 1.0f) * std::cos(2.0f * PI * py + 1.0f) * std::sin(2.0f * PI * pz + 1.0f);
        noiseZ += 0.5f * std::sin(4.0f * PI * px + 1.0f) * std::cos(4.0f * PI * py + 1.0f) * std::sin(4.0f * PI * pz + 1.0f);
        noiseZ += 0.25f * std::sin(8.0f * PI * px + 1.0f) * std::cos(8.0f * PI * py + 1.0f) * std::sin(8.0f * PI * pz + 1.0f);

        // Combine into vec3 and return the noise
        out[idx * 3 + 0] = noiseX;
        out[idx * 3 + 1] = noiseY;
        out[idx * 3 + 2] = noiseZ;
    }

};

} // namespace diffwood


