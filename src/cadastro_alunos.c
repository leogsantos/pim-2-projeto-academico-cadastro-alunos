/*
 * SISTEMA DE CADASTRO DE ALUNOS
 * Programa para cadastrar alunos com suas notas NP1, NP2 e PIM
 * Dados salvos em formato CSV para posterior processamento
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Constantes do programa
#define MAX_ALUNOS 100        // Máximo de alunos que podem ser cadastrados
#define MAX_NOME 100          // Tamanho máximo do nome do aluno
#define ARQUIVO_DADOS "alunos.csv" // Nome do arquivo de saída

// Estrutura para armazenar dados de um aluno
typedef struct {
    char nome[MAX_NOME];  // Nome completo do aluno
    float nota_np1;       // Nota da primeira prova (NP1)
    float nota_np2;       // Nota da segunda prova (NP2)
    float nota_pim;       // Nota do Projeto Integrado Multidisciplinar
} Aluno;

// Variáveis globais do programa
Aluno alunos[MAX_ALUNOS]; // Array para armazenar todos os alunos cadastrados
int total_alunos = 0;     // Contador de alunos cadastrados

// Protótipos das funções (declaração antecipada)
void exibir_menu();       // Exibe o menu principal
void cadastrar_aluno();   // Cadastra um novo aluno
void listar_alunos();     // Lista todos os alunos cadastrados
void salvar_dados();      // Salva dados no arquivo CSV
void carregar_dados();    // Carrega dados do arquivo CSV
void limpar_buffer();     // Limpa buffer de entrada
int validar_nota(float nota); // Valida se nota está entre 0.0 e 10.0

/*
 * FUNÇÃO PRINCIPAL
 * Controla o fluxo principal do programa com menu interativo
 */
int main() {
    int opcao; // Variável para armazenar opção escolhida pelo usuário
    
    // Cabeçalho do programa
    printf("=== SISTEMA DE CADASTRO DE ALUNOS ===\n\n");
    
    // Carrega dados existentes do arquivo CSV (se existir)
    carregar_dados();
    
    // Loop principal do menu
    do {
        exibir_menu();              // Mostra opções disponíveis
        printf("Digite sua opcao: ");
        scanf("%d", &opcao);        // Lê opção do usuário
        limpar_buffer();            // Remove caracteres extras do buffer
        
        // Executa ação baseada na opção escolhida
        switch(opcao) {
            case 1:
                cadastrar_aluno();  // Cadastra novo aluno
                break;
            case 2:
                listar_alunos();    // Exibe lista de alunos
                break;
            case 3:
                salvar_dados();     // Salva dados manualmente
                printf("\nDados salvos com sucesso!\n");
                printf("Pressione Enter para continuar...");
                getchar();
                break;
            case 4:
                salvar_dados();     // Salva antes de sair
                printf("\nSaindo do sistema...\n");
                break;
            default:
                printf("\nOpcao invalida! Tente novamente.\n");
                printf("Pressione Enter para continuar...");
                getchar();
        }
        
        system("cls"); // Limpa a tela para melhor visualização
        
    } while(opcao != 4); // Continua até usuário escolher sair
    
    return 0; // Programa executado com sucesso
}

/*
 * Exibe o menu principal com as opções disponíveis
 */
void exibir_menu() {
    printf("=== MENU PRINCIPAL ===\n");
    printf("1 - Cadastrar Aluno\n");
    printf("2 - Listar Alunos\n");
    printf("3 - Salvar Dados\n");
    printf("4 - Sair\n");
    printf("=====================\n");
}

/*
 * Função para cadastrar um novo aluno
 * Coleta nome e três notas, validando cada entrada
 */
void cadastrar_aluno() {
    // Verifica se ainda há espaço para novos alunos
    if(total_alunos >= MAX_ALUNOS) {
        printf("\nLimite maximo de alunos atingido!\n");
        printf("Pressione Enter para continuar...");
        getchar();
        return;
    }
    
    Aluno novo_aluno; // Estrutura temporária para novo aluno
    
    printf("\n=== CADASTRO DE ALUNO ===\n");
    
    // Coleta nome do aluno
    printf("Nome do aluno: ");
    fgets(novo_aluno.nome, MAX_NOME, stdin);
    novo_aluno.nome[strcspn(novo_aluno.nome, "\n")] = 0; // Remove quebra de linha
    
    // Coleta e valida nota NP1
    do {
        printf("Nota NP1 (0.0 a 10.0): ");
        scanf("%f", &novo_aluno.nota_np1);
        limpar_buffer();
        
        if(!validar_nota(novo_aluno.nota_np1)) {
            printf("Nota invalida! Digite uma nota entre 0.0 e 10.0.\n");
        }
    } while(!validar_nota(novo_aluno.nota_np1));
    
    // Coleta e valida nota NP2
    do {
        printf("Nota NP2 (0.0 a 10.0): ");
        scanf("%f", &novo_aluno.nota_np2);
        limpar_buffer();
        
        if(!validar_nota(novo_aluno.nota_np2)) {
            printf("Nota invalida! Digite uma nota entre 0.0 e 10.0.\n");
        }
    } while(!validar_nota(novo_aluno.nota_np2));
    
    // Coleta e valida nota PIM
    do {
        printf("Nota PIM (0.0 a 10.0): ");
        scanf("%f", &novo_aluno.nota_pim);
        limpar_buffer();
        
        if(!validar_nota(novo_aluno.nota_pim)) {
            printf("Nota invalida! Digite uma nota entre 0.0 e 10.0.\n");
        }
    } while(!validar_nota(novo_aluno.nota_pim));
    
    // Adiciona o aluno ao array principal
    alunos[total_alunos] = novo_aluno;
    total_alunos++; // Incrementa contador de alunos
    
    printf("\nAluno cadastrado com sucesso!\n");
    printf("Pressione Enter para continuar...");
    getchar();
}

/*
 * Lista todos os alunos cadastrados com suas respectivas notas
 */
void listar_alunos() {
    // Verifica se existem alunos cadastrados
    if(total_alunos == 0) {
        printf("\nNenhum aluno cadastrado!\n");
        printf("Pressione Enter para continuar...");
        getchar();
        return;
    }
    
    printf("\n=== LISTA DE ALUNOS CADASTRADOS ===\n\n");
    
    // Percorre array de alunos e exibe informações
    for(int i = 0; i < total_alunos; i++) {
        printf("Aluno %d:\n", i + 1);           // Numeração sequencial
        printf("Nome: %s\n", alunos[i].nome);
        printf("Nota NP1: %.2f\n", alunos[i].nota_np1);
        printf("Nota NP2: %.2f\n", alunos[i].nota_np2);
        printf("Nota PIM: %.2f\n", alunos[i].nota_pim);
        printf("--------------------------------\n");
    }
    
    // Exibe estatística total
    printf("\nTotal de alunos: %d\n", total_alunos);
    printf("Pressione Enter para continuar...");
    getchar();
}

/*
 * Salva todos os dados dos alunos em arquivo CSV
 * Formato: NOME,NP1,NP2,PIM
 */
void salvar_dados() {
    FILE *arquivo = fopen(ARQUIVO_DADOS, "w"); // Abre arquivo para escrita
    
    // Verifica se arquivo foi aberto com sucesso
    if(arquivo == NULL) {
        printf("\nErro ao abrir arquivo para escrita!\n");
        return;
    }
    
    // Escreve cabeçalho do CSV
    fprintf(arquivo, "NOME,NP1,NP2,PIM\n");
    
    // Escreve dados de cada aluno (uma linha por aluno)
    for(int i = 0; i < total_alunos; i++) {
        fprintf(arquivo, "%s,%.2f,%.2f,%.2f\n",
                alunos[i].nome,
                alunos[i].nota_np1,
                alunos[i].nota_np2,
                alunos[i].nota_pim);
    }
    
    fclose(arquivo); // Fecha arquivo e salva dados
}

/*
 * Carrega dados de alunos do arquivo CSV (se existir)
 * Executada automaticamente ao iniciar o programa
 */
void carregar_dados() {
    FILE *arquivo = fopen(ARQUIVO_DADOS, "r"); // Abre arquivo para leitura
    char linha[200]; // Buffer para armazenar cada linha lida
    
    // Se arquivo não existe, não há dados para carregar
    if(arquivo == NULL) {
        return; // Não é erro, arquivo será criado no primeiro salvamento
    }
    
    // Pula primeira linha (cabeçalho do CSV)
    if(fgets(linha, sizeof(linha), arquivo) == NULL) {
        fclose(arquivo);
        return;
    }
    
    // Lê dados dos alunos linha por linha
    total_alunos = 0;
    while(fgets(linha, sizeof(linha), arquivo) != NULL && total_alunos < MAX_ALUNOS) {
        // Remove quebra de linha do final
        linha[strcspn(linha, "\n")] = 0;
        
        // Faz parsing da linha CSV usando vírgula como separador
        char *token = strtok(linha, ",");
        if(token != NULL) {
            // Nome do aluno
            strcpy(alunos[total_alunos].nome, token);
            
            // Nota NP1
            token = strtok(NULL, ",");
            if(token != NULL) alunos[total_alunos].nota_np1 = atof(token);
            
            // Nota NP2
            token = strtok(NULL, ",");
            if(token != NULL) alunos[total_alunos].nota_np2 = atof(token);
            
            // Nota PIM
            token = strtok(NULL, ",");
            if(token != NULL) alunos[total_alunos].nota_pim = atof(token);
            
            total_alunos++; // Incrementa contador de alunos carregados
        }
    }
    
    fclose(arquivo); // Fecha arquivo após leitura
    printf("Dados carregados: %d alunos encontrados.\n\n", total_alunos);
}

/*
 * Remove caracteres extras do buffer de entrada
 * Evita problemas na leitura de dados subsequentes
 */
void limpar_buffer() {
    int c;
    while((c = getchar()) != '\n' && c != EOF); // Lê até encontrar nova linha ou fim
}

/*
 * Valida se a nota está dentro do intervalo permitido (0.0 a 10.0)
 * Retorna: 1 se válida, 0 se inválida
 */
int validar_nota(float nota) {
    return (nota >= 0.0 && nota <= 10.0); // Verifica intervalo válido
}
