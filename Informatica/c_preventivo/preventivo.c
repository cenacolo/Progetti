#include <stdio.h>

int main() {
  float costo_energia = 0.005 ;
  float costo_materiale;
  int tempo;
  float costo_parziale, costo_totale;
  int commesse;

  printf("Inserisci il tempo di stampa in minuti: ");
  scanf("%d", &tempo);
  printf("\nPLA:0.03 - TPU:0.05 - PTG:0.06\n");
printf("Inserisci il costo materiali: \n");
  scanf("%f", &costo_materiale);
  costo_parziale = (costo_energia+ costo_materiale) * tempo;
  printf("Costo parziale: %.2f\n", costo_parziale);

  printf("Inserisci il numero di commesse:\n ");
  scanf("%d", &commesse);

  costo_totale = costo_parziale * commesse;
  printf("Costo totale: %.2f\n", costo_totale);

  return 0;
}
