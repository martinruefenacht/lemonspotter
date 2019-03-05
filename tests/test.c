#include "mpi.h"
#include <stdio.h>
#include <stdlib.h>


int main(int argc, char** argv) {
		MPI_Finalize();

		MPI_Init(&argc, &argv);

return 0;
}
