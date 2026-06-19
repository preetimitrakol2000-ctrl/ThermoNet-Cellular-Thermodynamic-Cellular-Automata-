#include <stdio.h>
#include <stdlib.h>

#define WIDTH 10
#define HEIGHT 10

// Performs one step of thermal diffusion across a 2D grid matrix
void diffuse_heat(double* current, double* next, double thermal_diffusivity) {
    for (int y = 1; y < HEIGHT - 1; y++) {
        for (int x = 1; x < WIDTH - 1; x++) {
            int idx = y * WIDTH + x;
            
            // 4-Neighbor Laplacian (discrete spatial derivative)
            double center = current[idx];
            double up     = current[(y - 1) * WIDTH + x];
            double down   = current[(y + 1) * WIDTH + x];
            double left   = current[y * WIDTH + (x - 1)];
            double right  = current[y * WIDTH + (x + 1)];
            
            // Explicit finite difference update formula
            next[idx] = center + thermal_diffusivity * (up + down + left + right - 4.0 * center);
        }
    }
}

// Helper to update boundaries (simulate a constant external heat source at the top edge)
void enforce_boundaries(double* grid, double source_temp) {
    for (int x = 0; x < WIDTH; x++) {
        grid[x] = source_temp; // Top row stays hot
    }
}
