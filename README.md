# Sistema de Gerenciamento de Alunos

Este é um sistema CRUD completo para cadastro, edição, exclusão e gerenciamento de alunos e suas notas escolares, desenvolvido em Python com interface gráfica Tkinter e banco de dados PostgreSQL.

## Funcionalidades

- **Cadastrar Aluno:** Adicione alunos com nome, data de nascimento, responsável, contato e turma.
- **Editar Aluno:** Atualize os dados dos alunos já cadastrados.
- **Excluir Aluno:** Remova alunos e todas as suas notas, com confirmação antes da exclusão.
- **Gerenciar Notas:** Visualize e edite as notas de cada matéria para cada aluno.
- **Interface Gráfica Amigável:** Todas as operações são realizadas por meio de janelas intuitivas.

## Pré-requisitos

- Python 3.8 ou superior
- PostgreSQL
- Bibliotecas Python: `psycopg2`, `tkinter`

## Instalação das dependências

No terminal, execute:
```bash
pip install psycopg2
```
> O Tkinter já vem instalado na maioria das distribuições Python.

## Configuração do Banco de Dados

1. **Crie um banco de dados no PostgreSQL** (exemplo: `banco_escola_X`).
2. **Crie um usuário e senha** (ou utilize o padrão do seu PostgreSQL).
3. **Altere os dados de conexão no início do arquivo `programa.py`:**

```python
connection = conectar_banco(
    "banco_escola_X",   # Nome do seu banco de dados
    "postgres",         # Usuário do banco
    "root",             # Senha do banco
    "localhost",        # Host do banco
    "5432"              # Porta do banco
)
```
Troque `"banco_escola_X"`, `"postgres"`, `"root"`, `"localhost"` e `"5432"` pelos dados do seu ambiente.

## Como executar

No terminal, dentro da pasta do projeto, rode:
```bash
python programa.py
```

## Observações

- O programa cria automaticamente as tabelas necessárias na primeira execução.
- As mensagens de erro e sucesso aparecem na interface gráfica.
- Para cadastrar um aluno, todos os campos são obrigatórios.
- Ao excluir um aluno, todas as notas dele também são removidas.
