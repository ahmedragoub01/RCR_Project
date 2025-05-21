#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_CLAUSES 20
#define MAX_VARIABLES 12

FILE *fich_base = NULL;
FILE *fich_temp = NULL;

int nbr_propositions, nbr_variables, nbr_clauses, i;
int but[MAX_CLAUSES], non_but[MAX_CLAUSES];
char nom_base[20], c;

int main() {
    printf("Nom du fichier (sans extension) : ");
    scanf("%19s", nom_base);

    strcat(nom_base, ".cnf");

    fich_base = fopen(nom_base, "r+");
    if (fich_base == NULL) {
        printf("Impossible d'ouvrir BC...\n");
        return 1;
    } else {
        printf("BC ouvert avec succes\n");
    }

    fich_temp = fopen("Temp.cnf", "w+");
    if (fich_temp == NULL) {
        printf("Impossible de transférer BC \n");
        return 1;
    }

    fscanf(fich_base, "p cnf %d %d", &nbr_variables, &nbr_clauses);
    nbr_clauses += 1;
    fprintf(fich_temp, "p cnf %d %d\n", nbr_variables, nbr_clauses);

    // Copier le contenu restant
    c = fgetc(fich_base);
    while (c != EOF) {
        fputc(c, fich_temp);
        c = fgetc(fich_base);
    }

    printf("Liste des variables de la BC (littéraux):\n");
    printf("1: Na;\t\t2: Nb;\t\t3: Nc;\n");
    printf("4: Cea;\t\t5: Ceb;\t\t6: Cec;\n");
    printf("7: Coa;\t\t8: Cob;\t\t9: Coc;\n");
    printf("10: Ma;\t\t11: Mb;\t\t12: Mc;\n\n");

    printf("Donnez le nombre de littéraux : \n");
    scanf("%d", &nbr_propositions);

    for (i = 1; i <= nbr_propositions; i++) {
        printf("Entrez le littéral %d : \n", i);
        scanf("%d", &but[i]);
        if (but[i] > -13 && but[i] < 13)
            non_but[i] = -but[i];
        else
            puts("Erreur, code invalide");
    }

    fprintf(fich_temp, "\n");
    for (i = 1; i <= nbr_propositions; i++)
        fprintf(fich_temp, "%d ", non_but[i]);
    fprintf(fich_temp, "0\n");

    fclose(fich_base);
    fclose(fich_temp);

    // Appel à UBCSAT (GSAT algorithm)
    system("ubcsat -alg gsat -i Temp.cnf > results.txt");

    FILE *fich = fopen("results.txt", "r");
    if (fich == NULL) {
        printf("Impossible d'acceder aux resultats...\n");
        return 1;
    }

    int termine = 0;
    char texte[1000];

    while (fgets(texte, sizeof(texte), fich) && !termine) {
        if (strstr(texte, "c best")) {
            printf("\nBC U {Non but} est satisfaisable (UBCSAT).\n");
            termine = 1;
        }
    }

    if (!termine) {
        printf("\nBC U {Non but} est non satisfaisable.\n");
        for (i = 1; i <= nbr_propositions; i++)
            printf("%d ", -but[i]);
        printf((nbr_propositions > 1) ? "ne peuvent pas être atteints\n" : "ne peut pas être atteint\n");
    }

    fclose(fich);

    return 0;
}
