# ============================================================
# Sistema de Gerenciamento de Alunos - Python + Tkinter + PostgreSQL
#
# INSTRUÇÕES PARA CONEXÃO COM O BANCO DE DADOS:
#
# 1. Crie um banco de dados no PostgreSQL (exemplo: banco_escola_X).
# 2. Crie um usuário e senha, ou utilize o padrão do seu PostgreSQL.
# 3. Altere os dados de conexão abaixo conforme o seu ambiente:
#
#    connection = conectar_banco(
#        "NOME_DO_BANCO",   # Nome do seu banco de dados
#        "USUARIO",         # Usuário do banco
#        "SENHA",           # Senha do banco
#        "localhost",       # Host do banco
#        "5432"             # Porta do banco
#    )
#
# 4. Execute este programa normalmente.
#
#   **Desenvolvido por:**  
#       acalu sereno 20230330188
#
# ============================================================

import tkinter as tk
from tkinter import ttk
import psycopg2
from psycopg2 import OperationalError
from tkinter import messagebox
from tkinter import simpledialog

def conectar_banco(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Conexão com o PostgreSQL bem-sucedida")
    except OperationalError as e:
        messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao banco de dados: {e}")
        print(f"O erro '{e}' ocorreu")
    return connection

# Conexão com o banco de dados
connection = conectar_banco(
    "banco_escola_X", 
    "postgres", 
    "root", 
    "localhost", 
    "5432"
)

def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executada com sucesso")
    except OperationalError as e:
        print(f"O erro '{e}' ocorreu")

# criar as tabelas
create_users_table = """
CREATE TABLE IF NOT EXISTS aluno (
    id_aluno serial not null,
    nome varchar(120) not null,
    data_nc date not null,
    contato varchar(15) not null,
    nome_responsavel varchar(120) not null,
    turma varchar(12) not null,
    primary key (id_aluno)
);

CREATE TABLE IF NOT EXISTS notas (
    id_nota serial not null,
    materia varchar(20) not null,
    valor_nota decimal(5,2),
    id_aluno int not null,
    primary key (id_nota),
    foreign key (id_aluno) references aluno (id_aluno)
);
"""
#
execute_query(connection, create_users_table)



janela_principal= tk.Tk()
janela_principal.title("sistemas alunos")
janela_principal.geometry("400x300")
# janela de cadastro
def abrir_janela_cadastro():
    janela_cadastro = tk.Toplevel()
    janela_cadastro.title("Cadastrar Aluno")
    janela_cadastro.geometry("400x600")
    
    # Frame principal para organização
    frame_principal = ttk.Frame(janela_cadastro, padding=20)
    frame_principal.pack(expand=True, fill='both')
    
    # Função para criar campos com labels
    def criar_campo(texto, row, frame):
        ttk.Label(frame, text=texto, font=('Arial', 10)).grid(row=row, column=0, sticky='w', pady=(10, 0))
        entry = ttk.Entry(frame, font=('Arial', 11))
        entry.grid(row=row+1, column=0, sticky='ew', pady=(0, 10))
        return entry
    
    # salvar aluno
    def salvar_aluno():
        nome = entry_nome.get().strip()
        nascimento = entry_nascimento.get().strip()
        responsavel = entry_responsavel.get().strip()
        contato = entry_contato.get().strip()
        turma = entry_turma.get().strip()

        # Verificação dos campos obrigatórios
        if not nome or not nascimento or not responsavel or not contato or not turma:
            messagebox.showerror("Erro", "Preencha todos os campos antes de salvar.", parent=janela_cadastro)
            return

        from datetime import datetime
        try:
            nascimento_sql = datetime.strptime(nascimento, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erro", "Data de nascimento inválida! Use DD/MM/AAAA.", parent=janela_cadastro)
            return

        #  Inserir aluno e pegar o id gerado
        insert_query = f"""
        INSERT INTO aluno (nome, data_nc, nome_responsavel, contato, turma)
        VALUES ('{nome}', '{nascimento_sql}', '{responsavel}', '{contato}', '{turma}')
        RETURNING id_aluno;
        """
        cursor = connection.cursor()
        try:
            cursor.execute(insert_query)
            id_aluno = cursor.fetchone()[0]
            connection.commit()
            messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!", parent=janela_cadastro)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar aluno: {e}", parent=janela_cadastro)
            return

        #  Inserir matérias padrão para o aluno
        materias = ["geografia", "matematica", "portugues", "historia", "ciencias", "educacao_fisica", "ingles", "arte", "musica", "tecnologia", "filosofia", "sociologia"]
        for materia in materias:
            insert_nota = f"""
            INSERT INTO notas (materia, valor_nota, id_aluno)
            VALUES ('{materia}', 0.00, {id_aluno});
            """
            try:
                cursor.execute(insert_nota)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao inserir matéria {materia}: {e}", parent=janela_cadastro)
        connection.commit()
        cursor.close()

        # Limpar campos após salvar
        entry_nome.delete(0, tk.END)
        entry_nascimento.delete(0, tk.END)
        entry_responsavel.delete(0, tk.END)
        entry_contato.delete(0, tk.END)
        entry_turma.delete(0, tk.END)
        print("Aluno e matérias cadastrados com sucesso!")

    # Campos do formulário
    entry_nome = criar_campo("NOME COMPLETO:", 0, frame_principal)
    entry_nascimento = criar_campo("DATA DE NASCIMENTO (DD/MM/AAAA):", 2, frame_principal)
    entry_responsavel = criar_campo("NOME DO RESPONSÁVEL:", 4, frame_principal)
    entry_contato = criar_campo("CONTATO (TELEFONE):", 6, frame_principal)
    entry_turma = criar_campo("TURMA:", 8, frame_principal)
    
    # Frame para os botões
    frame_botoes = ttk.Frame(frame_principal)
    frame_botoes.grid(row=11, column=0, pady=20, sticky='ew')
    
    # Botão Salvar
    btn_salvar = ttk.Button(
        frame_botoes,
        text="SALVAR CADASTRO",
        style='Accent.TButton',  # Estilo especial (opcional)
        command=salvar_aluno
    )
    btn_salvar.pack(side='right', padx=5)
    
    # Botão Sair
    btn_sair = ttk.Button(
        frame_botoes,
        text="SAIR",
        command=janela_cadastro.destroy
    )
    btn_sair.pack(side='left', padx=5)
    
    # Configuração de colunas
    frame_principal.columnconfigure(0, weight=1)
    


# janela de edição
# Função para abrir a janela de edição
def abrir_editar_aluno():
    janela_atualizar_aluno = tk.Toplevel()
    janela_atualizar_aluno.title("Editar Aluno")
    janela_atualizar_aluno.geometry("500x600")

    frame_principal = ttk.Frame(janela_atualizar_aluno, padding=20)
    frame_principal.pack(expand=True, fill='both')
    # Função para criar campos com labels
    def criar_campo(texto, row, frame):
        ttk.Label(frame, text=texto, font=('Arial', 10)).grid(row=row, column=0, sticky='w', pady=(10, 0))
        entry = ttk.Entry(frame, font=('Arial', 11))
        entry.grid(row=row+1, column=0, sticky='ew', pady=(0, 10))
        return entry
    # Buscar alunos
    alunos = buscar_alunos()
    nomes_alunos = [f"{a[1]} (ID: {a[0]})" for a in alunos]

    ttk.Label(frame_principal, text="Selecione o aluno:", font=('Arial', 10)).grid(row=0, column=0, sticky='w')
    combo_alunos = ttk.Combobox(frame_principal, values=nomes_alunos, state="readonly")
    combo_alunos.grid(row=1, column=0, sticky='ew', pady=(0, 10))

    # Campos do formulário
    entry_nome = criar_campo("NOME COMPLETO:", 2, frame_principal)
    entry_nascimento = criar_campo("DATA DE NASCIMENTO (DD/MM/AAAA):", 4, frame_principal)
    entry_responsavel = criar_campo("NOME DO RESPONSÁVEL:", 6, frame_principal)
    entry_contato = criar_campo("CONTATO (TELEFONE):", 8, frame_principal)
    entry_turma = criar_campo("TURMA:", 10, frame_principal)

    def salvar_edicao():
        idx = combo_alunos.current()
        if idx == -1:
            messagebox.showwarning("Atenção", "Selecione um aluno para editar.", parent=janela_atualizar_aluno)
            return
        id_aluno = alunos[idx][0]
        nome = entry_nome.get()
        nascimento = entry_nascimento.get()
        responsavel = entry_responsavel.get()
        contato = entry_contato.get()
        turma = entry_turma.get()
        from datetime import datetime
        try:
            nascimento_sql = datetime.strptime(nascimento, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erro", "Data de nascimento inválida! Use DD/MM/AAAA.", parent=janela_atualizar_aluno)
            return

        cursor = connection.cursor()  
        try:
            cursor.execute("""
                UPDATE aluno SET nome=%s, data_nc=%s, nome_responsavel=%s, contato=%s, turma=%s
                WHERE id_aluno=%s
            """, (nome, nascimento_sql, responsavel, contato, turma, id_aluno))
            connection.commit()
            messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!", parent=janela_atualizar_aluno)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar aluno: {e}", parent=janela_atualizar_aluno)
        cursor.close()

    # Frame para os botões
    frame_botoes = ttk.Frame(frame_principal)
    frame_botoes.grid(row=12, column=0, pady=20, sticky='ew')

    btn_salvar = ttk.Button(
        frame_botoes,
        text="SALVAR ALTERAÇÕES",
        style='Accent.TButton',
        command=salvar_edicao
    )
    btn_salvar.pack(side='right', padx=5)

    btn_sair = ttk.Button(
        frame_botoes,
        text="SAIR",
        command=janela_atualizar_aluno.destroy
    )
    btn_sair.pack(side='left', padx=5)

    frame_principal.columnconfigure(0, weight=1)

    def preencher_campos(event):
        idx = combo_alunos.current()
        if idx == -1:
            return
        id_aluno = alunos[idx][0]
        cursor = connection.cursor()
        cursor.execute("SELECT nome, data_nc, nome_responsavel, contato, turma FROM aluno WHERE id_aluno = %s", (id_aluno,))
        dados = cursor.fetchone()
        cursor.close()
        if dados:
            entry_nome.delete(0, tk.END)
            entry_nome.insert(0, dados[0])
            entry_nascimento.delete(0, tk.END)
            entry_nascimento.insert(0, dados[1].strftime("%d/%m/%Y"))
            entry_responsavel.delete(0, tk.END)
            entry_responsavel.insert(0, dados[2])
            entry_contato.delete(0, tk.END)
            entry_contato.insert(0, dados[3])
            entry_turma.delete(0, tk.END)
            entry_turma.insert(0, dados[4])

    combo_alunos.bind("<<ComboboxSelected>>", preencher_campos)

    def deletar_aluno():
        idx = combo_alunos.current()
        if idx == -1:
            messagebox.showwarning("Atenção", "Selecione um aluno para deletar.", parent=janela_atualizar_aluno)
            return
        id_aluno = alunos[idx][0]
        nome_aluno = entry_nome.get()
        resposta = messagebox.askyesno(
            "Confirmação",
            f"Tem certeza que deseja deletar o aluno '{nome_aluno}'?\nTodas as notas desse aluno também serão removidas.",
            parent=janela_atualizar_aluno
        )
        if not resposta:
            return
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM notas WHERE id_aluno = %s", (id_aluno,))
            cursor.execute("DELETE FROM aluno WHERE id_aluno = %s", (id_aluno,))
            connection.commit()
            cursor.close()
            messagebox.showinfo("Sucesso", f"Aluno '{nome_aluno}' deletado com sucesso!", parent=janela_atualizar_aluno)
            janela_atualizar_aluno.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao deletar aluno: {e}", parent=janela_atualizar_aluno)

    # Botão Deletar
    btn_deletar = ttk.Button(
        frame_botoes,
        text="DELETAR ALUNO",
        style='Accent.TButton',
        command=deletar_aluno
    )
    btn_deletar.pack(side='left', padx=5)

def abrir_editar_notas():
    janela_notas = tk.Toplevel()
    janela_notas.title("Editar Notas do Aluno")
    janela_notas.geometry("500x500")

    frame_principal = ttk.Frame(janela_notas, padding=20)
    frame_principal.pack(expand=True, fill='both')

    # Buscar alunos
    alunos = buscar_alunos()
    nomes_alunos = [f"{a[1]} (ID: {a[0]})" for a in alunos]

    ttk.Label(frame_principal, text="Selecione o aluno:", font=('Arial', 10)).grid(row=0, column=0, sticky='w')
    combo_alunos = ttk.Combobox(frame_principal, values=nomes_alunos, state="readonly")
    combo_alunos.grid(row=1, column=0, sticky='ew', pady=(0, 10))

    # Treeview para mostrar matérias e notas
    tree = ttk.Treeview(frame_principal, columns=("Materia", "Nota"), show="headings")
    tree.heading("Materia", text="Matéria")
    tree.heading("Nota", text="Nota")
    tree.grid(row=2, column=0, sticky='nsew', pady=(10, 10))
    frame_principal.rowconfigure(2, weight=1)

    # Dicionário para armazenar entradas de notas
    entradas_nota = {}

    def carregar_notas(event):
        tree.delete(*tree.get_children())
        entradas_nota.clear()
        idx = combo_alunos.current()
        if idx == -1:
            return
        id_aluno = alunos[idx][0]
        cursor = connection.cursor()
        cursor.execute("SELECT id_nota, materia, valor_nota FROM notas WHERE id_aluno = %s ORDER BY materia", (id_aluno,))
        notas = cursor.fetchall()
        cursor.close()
        for id_nota, materia, valor_nota in notas:
            tree.insert("", "end", iid=id_nota, values=(materia, valor_nota))

    combo_alunos.bind("<<ComboboxSelected>>", carregar_notas)

    def editar_nota():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione uma matéria para editar.", parent=janela_notas)
            return
        id_nota = selected[0]
        materia, nota_atual = tree.item(id_nota, "values")
        nova_nota = simpledialog.askfloat("Editar Nota", f"Nova nota para {materia}:", initialvalue=float(nota_atual), parent=janela_notas)
        if nova_nota is None:
            return
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE notas SET valor_nota = %s WHERE id_nota = %s", (nova_nota, id_nota))
            connection.commit()
            cursor.close()
            tree.set(id_nota, "Nota", nova_nota)
            messagebox.showinfo("Sucesso", f"Nota de {materia} atualizada!", parent=janela_notas)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar nota: {e}", parent=janela_notas)

    btn_editar = ttk.Button(frame_principal, text="Editar Nota Selecionada", command=editar_nota)
    btn_editar.grid(row=3, column=0, pady=(10, 0), sticky='ew')

    btn_sair = ttk.Button(frame_principal, text="Sair", command=janela_notas.destroy)
    btn_sair.grid(row=4, column=0, pady=(10, 0), sticky='ew')


btn_abrir_cadastro = ttk.Button(
    janela_principal,
    text="cadastrar aluno",
    command=abrir_janela_cadastro,
    padding=(32,10)
)
btn_abrir_cadastro.pack(pady=(20,0))

btn_editar_aluno = ttk.Button(
    janela_principal,
    text="esditar aluno",
    command=abrir_editar_aluno,
    padding=(40,10)
)
btn_editar_aluno.pack(pady=(20,0))

btn_abrir_notas = ttk.Button(
    janela_principal,
    text="notas aluno",
    command=abrir_editar_notas,
    padding=(40,10)
)
btn_abrir_notas.pack(pady=(20,0))

btn_sair = ttk.Button(
    janela_principal,
    text="sair",
    command=janela_principal.destroy,
    padding=(40,10)
)
btn_sair.pack(pady=(20,0))


def buscar_alunos():
    cursor = connection.cursor()
    cursor.execute("SELECT id_aluno, nome FROM aluno ORDER BY nome;")
    alunos = cursor.fetchall()
    cursor.close()
    return alunos

# Iniciar a janela principal
janela_principal.mainloop()
