#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <task.h>
#include <sem.h>
#include <mutex.h>
#include <timer.h>

#define CLOCK_RES 1e-9
#define LIMITE_DA_FILA 5

RT_MUTEX mutex_quantidade_carros;

struct Fila{
	int num_carros;
	RT_SEM semaforo;
}filas[LIMITE_DA_FILA];

RT_TASK geradora_de_transito;
RT_TASK medicao_da_fila;
RT_TASK gerenciadora;
RT_TASK consumo;

//[sem1,sem2,sem3,...,semN]
//[fila1=n,fila2=n,fila3=n,...,filaN=m]

int fila_de_carros[LIMITE_DA_FILA];
int quantidade_de_carros[LIMITE_DA_FILA]; //ler_carros()
int index_do_semaforo_da_fila = 0;
int quantidade_de_carros_saindo_por_vez = 3;

int tempo_anterior_thread_1 = 0;
int tempo_anterior_thread_2 = 0;
int tempo_anterior_thread_3 = 0;
int tempo_anterior_thread_4 = 0;
float fator_tempo = 2;
int show_time = 0;
int show_extra_text = 0;

void gerar_carros(void *arg)//tempo = 6500 ns
{
	RTIME inicio, fim;

	rt_task_set_periodic(NULL, TM_NOW, 4e8*fator_tempo);  
	srand(time(NULL));

	while(1){
		int tempo_atual_do_sistema = rt_timer_read();

		if(tempo_atual_do_sistema - tempo_anterior_thread_1 > 4e8*fator_tempo)
		{
			if (show_extra_text) printf("Iniciou gerar carros ... \n");
			inicio = rt_timer_read();

			int numero_aleatorio_de_carros = 1 + (rand() % 3);
			int fila_aleatoria = (rand() % LIMITE_DA_FILA);
			
			filas[fila_aleatoria].num_carros += numero_aleatorio_de_carros;
			printf("\033[0;33m");
			printf("Carros que chegaram na fila %d: %d \n", fila_aleatoria, numero_aleatorio_de_carros);
			printf("\033[0;0m");
			//printf("Fila: %d, Nº de Carros: %d\n", fila_aleatoria, filas[fila_aleatoria].num_carros);
			
			fim = rt_timer_read();
			if(show_time) printf("TEMPO DO GERAR CARROS: %ld.%06ld; \n", (long)(fim - inicio));// / 1000000,(long)(fim - inicio) % 1000000); assim fica em +-800.0002 ns??
			if (show_extra_text) printf("Gerou carros ... ");
			//printf("TEMPO DO GERAR CARROS: %ld.%06ld; \n", (long)(inicio-fim) / 1000000,(long)(inicio-fim) % 1000000);
			//long tempo_bloqueio = ((fim - inicio) - 1000);
			//printf("T BLOQUEIO : %ld.%06ld \n", tempo_bloqueio);
			tempo_anterior_thread_1 = tempo_atual_do_sistema;
		}    
		rt_task_wait_period(NULL);
	}
}

void ler_fila(void *arg)//tempo = 12000 ns
{
	RTIME inicio, fim;
	int i=0;

	rt_task_set_periodic(NULL, TM_NOW, 1e8*fator_tempo);
	
	while(1){   
		
		int tempo_atual_do_sistema = rt_timer_read();
	
		if(tempo_atual_do_sistema - tempo_anterior_thread_2 > 1e8*fator_tempo)
		{
			if (show_extra_text) printf("Iniciou leitura de fila ... \n");
			inicio = rt_timer_read();
			rt_mutex_acquire(&mutex_quantidade_carros,0);
			for (i = 0; i < LIMITE_DA_FILA; i++){
				rt_sem_p(&filas[i].semaforo,TM_NONBLOCK);  
				
				quantidade_de_carros[i] = filas[i].num_carros;		
				printf("___%d___ ",filas[i].num_carros);

				
				rt_sem_broadcast (&filas[i].semaforo);//libera filas
			}
			rt_mutex_release(&mutex_quantidade_carros);
			if (show_extra_text) printf(" \n Leu filas ... \n");
			printf("\n"); 
			fim = rt_timer_read();
			if(show_time) printf("TEMPO DO LER FILAS: %ld.%06ld; \n", (long)(fim - inicio));// / 1000000, (long)(fim - inicio) % 1000000);
			//long tempo_bloqueio = ((fim - inicio) - 12000);
			//printf("T BLOQUEIO : %ld.%06ld \n", tempo_bloqueio);
			tempo_anterior_thread_2 = tempo_atual_do_sistema;
		}
		rt_task_wait_period(NULL);
	}
}
//heuristica
void abrir_semaforo(void *arg)//tempo = 18000 ns
{
	RTIME inicio, fim;
	rt_task_set_periodic(NULL, TM_NOW, 2e8*fator_tempo);
	
	while(1){      
		
		int tempo_atual_do_sistema = rt_timer_read();
	
		if(tempo_atual_do_sistema - tempo_anterior_thread_3 > 2e8*fator_tempo)
		{
			
			inicio = rt_timer_read();
			rt_task_suspend(&consumo);
			rt_mutex_acquire(&mutex_quantidade_carros,0);
			if (show_extra_text) printf("Iniciou heuristica ... \n");
			int numero_max = quantidade_de_carros[0];

			for(int i = 0; i < LIMITE_DA_FILA; ++i){
				if(quantidade_de_carros[i] >= numero_max){
					numero_max = quantidade_de_carros[i];
					index_do_semaforo_da_fila = i;
				}       
			}
			printf("\033[0;35m");
			printf("Semaforo que ira abrir: %d\n", index_do_semaforo_da_fila);
			printf("\033[0;0m");
			rt_mutex_release(&mutex_quantidade_carros);
			rt_task_resume(&consumo);
			fim = rt_timer_read();
			if (show_extra_text) printf("Terminou Heuristica");
			if(show_time) printf("TEMPO DO ABRIR SEMAFORO: %ld.%06ld; \n", (long)(fim - inicio));// / 1000000,(long)(fim - inicio) % 1000000);
			//long tempo_bloqueio = ((fim - inicio) - 10000);
			//printf("T BLOQUEIO : %ld.%06ld \n", tempo_bloqueio);
			tempo_anterior_thread_3 = tempo_atual_do_sistema;
		}   

		

		rt_task_wait_period(NULL);
	}
}

void fluxo(void *arg) //tempo = 12000 ns
{
	RTIME inicio, fim;
	rt_task_set_periodic(NULL, TM_NOW, 4e8*fator_tempo);
	
	while(1){	
		
		int tempo_atual_do_sistema = rt_timer_read();

		if(tempo_atual_do_sistema - tempo_anterior_thread_4 > 4e8*fator_tempo)
		{

			inicio = rt_timer_read();	
			

			rt_sem_p(&filas[index_do_semaforo_da_fila].semaforo,TM_INFINITE);	
			//rt_mutex_acquire(&mutex_quantidade_carros,0);
			printf("\033[0;36m");
			printf("Liberando fluxo no semaforo : %d\n", index_do_semaforo_da_fila);
			if (quantidade_de_carros[index_do_semaforo_da_fila] == 0){  
				printf("Fila: %d, Zerada\n", index_do_semaforo_da_fila);
			}
			else if(quantidade_de_carros[index_do_semaforo_da_fila] > quantidade_de_carros_saindo_por_vez){ 
				filas[index_do_semaforo_da_fila].num_carros -= quantidade_de_carros_saindo_por_vez;

			}
			else{
				filas[index_do_semaforo_da_fila].num_carros -= quantidade_de_carros[index_do_semaforo_da_fila];
				//printf("Fila: %d, Sobrou: %d\n", index_do_semaforo_da_fila, quantidade_de_carros[index_do_semaforo_da_fila]);
			}
			printf("\033[0;0m");
			if (show_extra_text) printf("Liberou alguns carros ... \n");
			rt_sem_broadcast(&filas[index_do_semaforo_da_fila].semaforo);	
			//printf("Antes: %d, Depois: %d\n", (quantidade_de_carros[index_do_semaforo_da_fila] + quantidade_de_carros_saindo_por_vez), quantidade_de_carros[index_do_semaforo_da_fila]);
			//printf("Antes: %d, Depois: %d\n", (filas[index_do_semaforo_da_fila].num_carros + quantidade_de_carros_saindo_por_vez), filas[index_do_semaforo_da_fila].num_carros);
			//printf("Fila: %d, Sobrou: %d\n", index_do_semaforo_da_fila, quantidade_de_carros[index_do_semaforo_da_fila]);

			//rt_mutex_release(&mutex_quantidade_carros); 
		    fim = rt_timer_read();	
			if(show_time) printf("TEMPO DO FLUXO: %ld.%06ld; \n", (long)(fim - inicio));// / 1000000,(long)(fim - inicio) % 1000000);
			//long tempo_bloqueio = ((fim - inicio) - 9500);
			//printf("T BLOQUEIO : %ld.%06ld \n", tempo_bloqueio);
			tempo_anterior_thread_4 = tempo_atual_do_sistema;
		}

		rt_task_wait_period(NULL);
	}
}

int main(int argc, char* argv[])
{
	 mlockall(MCL_CURRENT|MCL_FUTURE);
	 
	printf("\033[0;0m");
	  
	rt_mutex_create(&mutex_quantidade_carros,"mutex_quantidade_carros");

	rt_task_create(&geradora_de_transito, "thread_1", 0, 2, 0);//6500ns
	rt_task_create(&medicao_da_fila, "thread_2", 0, 3, 0);//13000
	rt_task_create(&gerenciadora, "thread_3", 0, 2, 0);//18000
	rt_task_create(&consumo, "thread_4", 0, 1, 0);//10000
	
	for(int i=0;i<LIMITE_DA_FILA-1;i++){
		rt_sem_create(&filas[i].semaforo, "Semaforo", 1, S_PRIO);
	}

	rt_task_start(&geradora_de_transito, &gerar_carros, 0);
	rt_task_start(&medicao_da_fila, &ler_fila, 0);
	rt_task_start(&gerenciadora, &abrir_semaforo, 0);
	rt_task_start(&consumo, &fluxo, 0);

	pause();
	printf("\033[0;0m");
	return 0;
}