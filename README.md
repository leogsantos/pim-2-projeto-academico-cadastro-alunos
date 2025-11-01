# Sistema de Cadastro de Alunos

Este projeto é composto por dois módulos principais:
- **cadastro_alunos.c**: Software em C para cadastro de alunos via terminal, salvando os dados em um arquivo CSV.
- **interface_alunos.py**: Interface gráfica em Python (Tkinter) para visualizar e gerenciar os alunos cadastrados.

## Funcionalidades

### 1. Cadastro de Alunos (Terminal)
- Cadastro de nome, nota NP1, nota NP2 e nota PIM.
- Validação das notas (0.0 a 10.0).
- Dados salvos em `output/alunos.csv` no formato:
  ```csv
  NOME,NP1,NP2,PIM
  Leonardo Gomes dos Santos,10.00,7.00,6.00
  teste877,3.00,5.00,9.00
  testando8745,9.00,5.00,8.00
  ```
- Menu interativo para cadastrar, listar, salvar e sair.

### 2. Interface Gráfica (Tkinter)
- Visualização dos alunos cadastrados em frames individuais.
- Exibição das notas e média calculada automaticamente.
- Status de aprovação/reprovação por cor e texto.
- Botão para abrir o cadastro de alunos (executa o programa C).
- Botão para atualizar os dados da interface.
- Layout responsivo e moderno.

## Como funciona

1. **Cadastro de alunos**:
   - Execute o programa `cadastro_alunos.exe` (gerado a partir do código C).
   - Cadastre os alunos pelo terminal.
   - Os dados são salvos automaticamente em `output/alunos.csv`.

2. **Interface gráfica**:
   - Execute o arquivo `interface_alunos.py`.
   - Visualize todos os alunos cadastrados, suas notas, média e status.
   - Use o botão "Abrir Cadastro de Alunos" para adicionar novos alunos sem sair da interface.
   - Use o botão "Atualizar Dados" para recarregar as informações do CSV.

## Requisitos

- Windows (testado)
- Python 3.x (com Tkinter)
- Compilador C (MinGW recomendado)

## Estrutura do Projeto
```
cadastro_alunos.c
interface_alunos.py
output/
  ├─ cadastro_alunos.exe
  └─ alunos.csv
README.md
```

## Observações
- O arquivo CSV é gerado automaticamente após o cadastro.
- A interface gráfica pode ser executada diretamente (duplo clique ou via terminal).
- O projeto não requer instalação de dependências externas para o Python (Tkinter já vem na instalação padrão).

---
**Desenvolvido para fins acadêmicos.**
