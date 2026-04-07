/*#######################################################################################
 #* Fecha: 
 #* Autor: J. Corredor, PhD
 #* Modulo: 
 #       -     
 #* Versión:
 #*	 	Concurrencia de Tareas: Paralelismo sobre Multiplicación de Matrices
 #* Descripción:
 #       - 
######################################################################################*/

#ifndef __MODULOMM_H__
#define __MODULOMM_H__

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <pthread.h>
#include <sys/time.h>
#include "moduloMM.h"

struct timeval inicio, fin;

/*/////////////////////////////////////////////////
 * IMPRIME LA MATRIZ SI SU TAMAÑO ES MENOR A 13
 */////////////////////////////////////////////////////

void impMatrix(double *matrix, int D){
	if(D < 13){ //verifica el tamaño la matriz sea menor a 13
		printf("\n");
		for(int i=0; i<D*D; i++){ // el ciclo para cuando ya se imprimieron todos los elementos de la matriz de tamaño D
			if(i%D==0) printf("\n");
			printf("%.2f ", matrix[i]);
			/*
			 * Adicionalmente esta pone un enter cuando el numero de Elementos impresos es multiplo del tamaño de la matriz\
			 * Genious!
			 */
		}
		printf("\n**-----------------------------**\n");
		//cuando termina de imprimir la matriz imprime una linea :D
	}
}

/*
 *
 */

/*/////////////////////////////////////////////
 * se hace la   transpuesta
*/////////////////////////////////////////////
void matrixTRP(int N, double *mB, double *mT){
	for(int i=0; i<N; i++)
		for(int j=0; j<N; j++)
			mT[i*N+j] = mB[j*N+i];
	impMatrix(mT, N);
}


/*/////////////////////////////////////////////////////////
* se realiza la multiplicacion de filas por transpuesta
*//////////////////////////////////////////////////////////

void mxmForkFxT(double *mA, double *mT, double *mC, int D, int filaI, int filaF){
    for (int i = filaI; i < filaF; i++)
        for (int j = 0; j < D; j++) {
			double *pA, *pB, Suma = 0.0;
			pA = mA+i*D;
			pB = mT+j*D;
            for (int k = 0; k < D; k++, pA++, pB++) 
				Suma += *pA * *pB;	
			mC[i*D+j] = Suma;
        }
}


/*/////////////////////////////////////////////////////////
 se hace la multiplicacion filas por columnas
*//////////////////////////////////////////////////////////

void mxmForkFxC(double *mA, double *mB, double *mC, int D, int filaI, int filaF){
    for (int i = filaI; i < filaF; i++)
        for (int j = 0; j < D; j++) {
			double *pA, *pB, Suma = 0.0;
			pA = mA+i*D;
			pB = mB+j;
            for (int k = 0; k < D; k++, pA++, pB+=D) 
				Suma += *pA * *pB;	
			mC[i*D+j] = Suma;
        }
}

/*
 * se empieza a tomar el tiempo
*/
void InicioMuestra(){
	gettimeofday(&inicio, (void *)0);
}

/*
 * se detiene la muestra del tiempo
*/
void FinMuestra(){
	gettimeofday(&fin, (void *)0);
	fin.tv_usec -= inicio.tv_usec;
	fin.tv_sec  -= inicio.tv_sec;
	double tiempo = (double) (fin.tv_sec*1000000 + fin.tv_usec); 
	printf("%9.0f \n", tiempo);
}


void iniMatrix(double *m1, double *m2, int D){

	/*///////////////////////////////////////////////////////////////////////////////////////////////////////////
	 * Ademas hay que tener en cuenta que aunque nosotros pensamos las matrices de la siguiente manera:
	 *
	 *	1 2 3
	 *	4 5 6
	 *	7 8 9
	 *
	 * en el proyecto se almacenan de esta manera:
	 *
	 * [1 2 3 4 5 6 7 8 9]
	 *
	 * utilizando la vatiable D para saber el tamano de la fila
	 *
	 *////////////////////////////////////////////////////////////////////////////////////////////////////////////

	srand(time(NULL));
	/*/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	 * srand(time(NULL)); -> una opcion de configuracion que cambia la semilla de generacion de numeros aleatorios,
	 * para que con cada ejecucion, no sean los mismos y asi, me imagino que no reutilizar la memoria de ninguna manera o algo asi
	 *//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

	for(int i=0; i<D*D; i++, m1++, m2++){

		/*//////////////////////////////////////////////////////////////////////////////////////////////////////////
		 * Se calcula el numero de elementos osea, el ciclo va de 0 a el numero de elementos D*D
		 * el ciclo recorre de 0 hasta D*D-1 y asi se recorren todos elementos de la matriz
		 * Adicionalmente D*D se utilizara para generar el espacio sufiente para que el arreglo almacene D*D datos
		 */////////////////////////////////////////////////////////////////////////////////////////////////////////

		*m1 = (double)rand()/RAND_MAX*(5.0-1.0); //genera numeros entre 0 y 4

		/*/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		 * Se genera un numero aleatorio con rand(), nota, este numero esta entre 0 y RAND_MAX
		 * se toma la constante del sistema llamada RAND_MAX, NOTAAAAA hay que consultar esta variable
		 * despues se divide... al dividir se numero por el maximo que puede ser, genera que el resultado este entre 0 y 1
		 * despues de esto se multiplica el decimal que queda por 4 o por 7
		 */////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		*m2 = (double)rand()/RAND_MAX*(9.0-2.0); // genera numeros entre 0 y 7

		//NOTAAAAAAAAAAAAAAAAAAAA: investigar porque los numeros pequenos (decimales) son los mejores para las pruebas de rendimeinto
	}
}

#endif
