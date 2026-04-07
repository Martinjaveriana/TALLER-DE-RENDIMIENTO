#!/usr/bin/perl
#**************************************************************
#         		Pontificia Universidad Javeriana
#     Autor: J. Corredor 
#	  Nombre Estudiante: 
#     Fecha: 
#     Materia: Sistemas Operativos
#     Tema: Taller de Evaluación de Rendimiento
#     Fichero: script automatización ejecución por lotes 
#****************************************************************/

# Obtiene la ruta del proyecto 
$Path = `pwd`;
chomp($Path);

# Estos son los programas que se probaran / ejecutaran
@Nombre_Ejecutable = ("mxmPosixFxC","mxmPosixFxT","mxmForkFxC","mxmForkFxT");

#Define los tamanos de las matrices que se probaran
@Size_Matriz  = ("512","1024","2048");

#Define el numero de hilos con el que se ejecutara el programa: 1 hilo (secuencial), 2 hilos (paralelo)
@Num_Hilos    = (1,4,8,16);

#El numero de veces que se ejecutara cada iteracion del experimiento
$Repeticiones = 30;

#Indica donde estan los ejecutables y donde se guardaran los resultados 
$Resultados	  = "Soluciones";
$Binarios	  = "bin";


foreach $nombre (@Nombre_Ejecutable){
	foreach $size (@Size_Matriz){
		foreach $hilo (@Num_Hilos) {
		#Los tres ciclos anteriores hacen que se creen las combinaciones de los programas
			$file = "$Path/$Resultados/$nombre-".$size."-Hilos-".$hilo.".dat"; # Genera un nombre como: Soluciones/mxmPosixFxC-100-Hilos-1.dat
			printf("$file \n");
			for ($i=0; $i<$Repeticiones; $i++) {
				system("$Path/$Binarios/$nombre $size $hilo  >> $file"); #Guarda la info en los archivos
				printf("$Path/$Binarios/$nombre $size $hilo \n"); # Imprime la info
			}
			close($file);
		}
	}
}	
