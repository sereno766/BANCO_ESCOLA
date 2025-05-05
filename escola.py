import psycopg2
import tkinter as tk
from tkinter import ttk
import os
from dotenv import load_dotenv

load_dotenv()

DB_host = os.getenv("DB_host")
DB_user=os.getenv('DB_user')
DB_password=os.getenv('DB_password')
DB_database=os.getenv('DB_database')
DB_port=os.getenv('DB_port')

def criar_janela():
    # Criação da janela principal
    janela = tk.Tk()
    janela.title("BANCO DOS ALUNOS")
    janela.geometry("800x400")

    conexao = psycopg2.connect(
        host=DB_host,
        user=DB_user,
        password=DB_password,
        database=DB_database,
        port=DB_port
    )
    print("✅ Conexão com Tembo Cloud estabelecida com sucesso!")

    nome_aluno = 'Ana Pereira'
    id = ''



    # pega o nome e retorna suas notas
    def RETORNAR_MATERIA():
        with conexao.cursor() as cursor:
            cursor.execute('''
                SELECT ALUNO.NOME, MATERIA.materia, MATERIA.NOTA 
                FROM ALUNO 
                LEFT JOIN MATERIA ON ALUNO.ID_ALUNO = MATERIA.ID_ALUNO 
                WHERE ALUNO.NOME = %s
            ''', (nome_aluno,))
            
            resultado = cursor.fetchall()
            for linha in resultado:
                print(f"Nome: {linha[0]}, Matéria: {linha[1]}, Nota: {linha[2]}")
                
                
    def CRIAR_ALUNO(nome):
        
        global nome_aluno
        nome_aluno = nome
        with conexao.cursor() as cursor:
            cursor.execute('INSERT INTO ALUNO (nome) VALUES (%s)', (nome_aluno,))
            conexao.commit()
            
            
        # preciso solicitar o id atraves do nome   / nome deve ser guardado antes de add uma nota  
    def ADCIONAR_NOTA(materia,nota):
        global id
        with conexao.cursor() as cursor:
            cursor.execute('SELECT id_aluno FROM aluno WHERE nome = (%s);', (nome_aluno))
            id=cursor.fetchall()
        with conexao.cursor() as cursor:
            cursor.execute('INSERT INTO MATERIA (materia,nota,id_aluno)VALUES (%s,%s,%s)',(materia,nota,id))
            conexao.commit()

    botao = ttk.Button(
    janela,
    text="Clique Aqui",
    command=RETORNAR_MATERIA
    )
    botao.pack(pady=10)
    # Executar o teste
    # Inicia o loop principal
    janela.mainloop()











# Chama a função para criar a janela
criar_janela()