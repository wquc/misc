#include <stdio.h>
#include <math.h>	/* fabs */
#include <stdlib.h>     /* strtod */

const double TOL = 1e-12;

struct Point {
    double x;
    double y;
    double z;
};

double func(double t, struct Point vec, struct Point p0, double r0);
double grad(double t, struct Point vec, struct Point p0);
void intersect(double t, struct Point vec, struct Point p0);
void forcevec(double t, struct Point vec, struct Point p0);

int main(int argc, char* argv[]) {
    if(argc!=9) {
        printf("Wrong number of parameters!\n"); 
        printf("Expect the following (8) arguments:\n"); 
        printf("Coordinate of SMD atom: [x1] [y1] [z1]\n"); 
        printf("Coordinate of Pore COM: [x2] [y2] [z2]\n"); 
        printf("[Radius] and [Initial_guess]\n"); 
        return 1;
    }
    // Read and store input
    double x1 = strtod(argv[1], NULL);  
    double y1 = strtod(argv[2], NULL);
    double z1 = strtod(argv[3], NULL);
    double x2 = strtod(argv[4], NULL);
    double y2 = strtod(argv[5], NULL);
    double z2 = strtod(argv[6], NULL);
    double R0 = strtod(argv[7], NULL);
    double IG = strtod(argv[8], NULL);

    struct Point P1 = {x1, y1, z1};
    struct Point P2 = {x2, y2, z2};
    struct Point V  = {P1.x-P2.x, P1.y-P2.y, P1.z-P2.z};

    // Newton Raphson with Initial guess 1.0
    double x = IG; 
    double h = func(x, V, P2, R0)/grad(x, V, P2);
    while(fabs(h) >= TOL) {
        h = func(x, V, P2, R0)/grad(x, V, P2);
        x = x - h;
    }
    forcevec(x, V, P2);
    return 0;
}

double func(double t, struct Point vec, struct Point p0, double r0) {
    double x_sq = (vec.x*t+p0.x)*(vec.x*t+p0.x);
    double y_sq = (vec.y*t+p0.y)*(vec.y*t+p0.y);
    double z_sq = (vec.z*t+p0.z)*(vec.z*t+p0.z);
    return x_sq + y_sq + z_sq - r0*r0;
}

double grad(double t, struct Point vec, struct Point p0) {
    double x_gr = 2.0*vec.x*(vec.x*t+p0.x);
    double y_gr = 2.0*vec.y*(vec.y*t+p0.y);
    double z_gr = 2.0*vec.z*(vec.z*t+p0.z);
    return x_gr + y_gr + z_gr;
}

void intersect(double t, struct Point vec, struct Point p0) {
	double x = vec.x*t + p0.x;
	double y = vec.y*t + p0.y;
	double z = vec.z*t + p0.z;
	printf("%6.4f %6.4f %6.4f\n", x, y, z);
}

void  forcevec(double t, struct Point vec, struct Point p0) {
	double x = vec.x*t + p0.x;
	double y = vec.y*t + p0.y;
	double z = vec.z*t + p0.z;
	printf("%6.4f %6.4f %6.4f\n", x-p0.x, p0.y, p0.z);
}
