#include "noise.h"


namespace diffwood {

void periodic_noise_3d(const float p[3], float out[3]) {
    // Create noise for each component of vec3 independently
    constexpr auto PI = Pi<float>;
    const auto px = p[0];
    const auto py = p[1];
    const auto pz = p[2];

    float noiseX = sin(2.0f * PI * px) * cos(2.0f * PI * py) * sin(2.0f * PI * pz);
    noiseX += 0.5f * sin(4.0f * PI * px) * cos(4.0f * PI * py) * sin(4.0f * PI * pz);
    noiseX += 0.25f * sin(8.0f * PI * px) * cos(8.0f * PI * py) * sin(8.0f * PI * pz);

    float noiseY = cos(2.0 * PI * px) * sin(2.0 * PI * py) * cos(2.0 * PI * pz);
    noiseY += 0.5 * cos(4.0 * PI * px) * sin(4.0 * PI * py) * cos(4.0 * PI * pz);
    noiseY += 0.25 * cos(8.0 * PI * px) * sin(8.0 * PI * py) * cos(8.0 * PI * pz);

    float noiseZ = sin(2.0 * PI * px + 1.0) * cos(2.0 * PI * py + 1.0) * sin(2.0 * PI * pz + 1.0);
    noiseZ += 0.5 * sin(4.0 * PI * px + 1.0) * cos(4.0 * PI * py + 1.0) * sin(4.0 * PI * pz + 1.0);
    noiseZ += 0.25 * sin(8.0 * PI * px + 1.0) * cos(8.0 * PI * py + 1.0) * sin(8.0 * PI * pz + 1.0);

    // Combine into vec3 and return the noise
    out[0] = noiseX;
    out[1] = noiseY;
    out[2] = noiseZ;
}

} // namespace diffwood


