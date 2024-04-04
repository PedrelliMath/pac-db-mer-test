import sqlite3
import os

from models import *
from utils import input_comprehension
from config import options, database_file_path
from errors import EmprestimoFailure

def init_dabase(init_sql_file):

    try:
        with open(init_sql_file, 'r') as init_file:
            sql = init_file.read()
    except FileNotFoundError:
        print("O arquivo init.sql nao foi encontrado")
    except IOError:
        print("Erro ao ler o arquivo init.sql")

    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            cursor.executescript(sql)
            conn.commit()
            print("Init.sql foi executado sem erros")
    except sqlite3.Error as e:
        print(f"Erro ao iniciar o banco de dados: {e}")

def make_login(user: str, password: str):

    sql_login = """
        SELECT COUNT(*) FROM Login WHERE usuario = ? AND senha = ?
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_login, (user, password))
            user = cursor.fetchone()[0]
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

    return user == 1
    
def db_book_register(livro: Livro):

    print(f'Tentando inserir o livro:\n{str(livro)}')

    sql_book_register = """
        INSERT INTO Livro (titulo, edicao, ISBN, categoria, ano_de_publicacao, id_editora)
        VALUES (
            ?, ?, ?, ?, ?, ?
        )
    """

    sql_book_autor = """
        INSERT INTO LivroAutor(id_autor, codigo_livro)
        VALUES (?, ?)
    """

    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            conn.execute('BEGIN')

            cursor.execute(sql_book_register, (
                livro.titulo,
                livro.edicao,
                livro.ISBN,
                livro.categoria,
                livro.ano_de_publicacao,
                livro.id_editora,
            ))

            codigo_livro = cursor.lastrowid

            for autor in livro.autores:
                cursor.execute(sql_book_autor, (autor.id_autor, codigo_livro))

            try:
                conn.execute('COMMIT')
                print(f"Sucesso ao inserir o livro {livro.titulo}")
            except sqlite3.IntegrityError as e:
                print(f"Erro de integridade ao inserir os dados: {e}")
            except sqlite3.OperationalError as e:
                print(f"Os parametros de insercao sao invalidos: {e}")
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_all_books_query():

    print(f'Buscando todos os livros no banco')

    sql_all_books_query = """
        SELECT Livro.codigo_livro, Livro.titulo, Livro.edicao, Livro.ISBN, Livro.categoria, 
            Livro.ano_de_publicacao, Editora.nome AS editora, 
            Livro.quantidade_exemplares, GROUP_CONCAT(Autor.nome, ', ') AS autores
        FROM Livro
        INNER JOIN Editora ON Livro.id_editora = Editora.id
        LEFT JOIN LivroAutor ON Livro.codigo_livro = LivroAutor.codigo_livro
        LEFT JOIN Autor ON LivroAutor.id_autor = Autor.id
        GROUP BY Livro.codigo_livro;
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_all_books_query)
                return cursor.fetchall()
            except sqlite3.OperationalError as e:
                print(f'Os parametros da consulta sao invalidos: {e}')
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_book_by_title_query(book_title: str):

    print(f'Buscando livro {book_title}')

    sql_book_by_title_query = """
        SELECT Livro.codigo_livro, Livro.titulo, Livro.edicao, Livro.ISBN, Livro.categoria, 
            Livro.ano_de_publicacao, Editora.nome AS editora, 
            Livro.quantidade_exemplares, GROUP_CONCAT(Autor.nome, ', ') AS autores
        FROM Livro
        INNER JOIN Editora ON Livro.id_editora = Editora.id
        LEFT JOIN LivroAutor ON Livro.codigo_livro = LivroAutor.codigo_livro
        LEFT JOIN Autor ON LivroAutor.id_autor = Autor.id
        WHERE Livro.titulo = ?
        GROUP BY Livro.codigo_livro;
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_book_by_title_query, (book_title,))
                return cursor.fetchall()
            except sqlite3.OperationalError as e:
                print(f'Os parametros da consulta sao invalidos: {e}')
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_book_by_ISBN_query(ISBN: str):

    print(f'Buscando livro com ISBN: {ISBN}')

    sql_book_by_ISBN_query = """
        SELECT Livro.codigo_livro, Livro.titulo, Livro.edicao, Livro.ISBN, Livro.categoria, 
            Livro.ano_de_publicacao, Editora.nome AS editora, 
            Livro.quantidade_exemplares, GROUP_CONCAT(Autor.nome, ', ') AS autores
        FROM Livro
        INNER JOIN Editora ON Livro.id_editora = Editora.id
        LEFT JOIN LivroAutor ON Livro.codigo_livro = LivroAutor.codigo_livro
        LEFT JOIN Autor ON LivroAutor.id_autor = Autor.id
        WHERE Livro.ISBN = ?
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_book_by_ISBN_query, (ISBN,))
                return cursor.fetchone()
            except sqlite3.OperationalError as e:
                print(f'Os parametros da consulta sao invalidos: {e}')
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_book_by_ID_query(ID: int):

    print(f'Buscando livro com id: {ID}')

    sql_book_by_title_query = """
        SELECT Livro.codigo_livro, Livro.titulo, Livro.edicao, Livro.ISBN, Livro.categoria, 
            Livro.ano_de_publicacao, Editora.nome AS editora, 
            Livro.quantidade_exemplares, GROUP_CONCAT(Autor.nome, ', ') AS autores
        FROM Livro
        INNER JOIN Editora ON Livro.id_editora = Editora.id
        LEFT JOIN LivroAutor ON Livro.codigo_livro = LivroAutor.codigo_livro
        LEFT JOIN Autor ON LivroAutor.id_autor = Autor.id
        WHERE Livro.codigo_livro = ?
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_book_by_title_query, (ID,))
                return cursor.fetchone()
            except sqlite3.OperationalError as e:
                print(f'Os parametros da consulta sao invalidos: {e}')
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_books_by_autor_name_query(autor_name: str):

    print(f'Buscando livros do autor: {autor_name}')

    sql_book_by_autor_name_query = """
        SELECT Livro.codigo_livro, Livro.titulo, Livro.edicao, Livro.ISBN, Livro.categoria, 
            Livro.ano_de_publicacao, Editora.nome AS editora, 
            Livro.quantidade_exemplares, GROUP_CONCAT(Autor.nome, ', ') AS autores
        FROM Livro
        INNER JOIN Editora ON Livro.id_editora = Editora.id
        LEFT JOIN LivroAutor ON Livro.codigo_livro = LivroAutor.codigo_livro
        LEFT JOIN Autor ON LivroAutor.id_autor = Autor.id
        WHERE Livro.codigo_livro IN (
            SELECT LivroAutor.codigo_livro
            FROM LivroAutor
            INNER JOIN Autor ON LivroAutor.id_autor = Autor.id
            WHERE Autor.nome = ?
        )
        GROUP BY Livro.codigo_livro;
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_book_by_autor_name_query, (autor_name,))
                return cursor.fetchall()
            except sqlite3.OperationalError as e:
                print(f'Os parametros da consulta sao invalidos: {e}')
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_books_by_author_id_query(autor_id: str):

    print(f'Buscando livros pelo id do autor: {autor_id}')

    sql_book_by_autor_id_query = """
        SELECT Livro.codigo_livro, Livro.titulo, Livro.edicao, Livro.ISBN, Livro.categoria, 
            Livro.ano_de_publicacao, Editora.nome AS editora, 
            Livro.quantidade_exemplares, GROUP_CONCAT(Autor.nome, ', ') AS autores
        FROM Livro
        INNER JOIN Editora ON Livro.id_editora = Editora.id
        LEFT JOIN LivroAutor ON Livro.codigo_livro = LivroAutor.codigo_livro
        LEFT JOIN Autor ON LivroAutor.id_autor = Autor.id
        WHERE Livro.codigo_livro IN (
            SELECT LivroAutor.codigo_livro
            FROM LivroAutor
            WHERE LivroAutor.id_autor = ?
        )
        GROUP BY Livro.codigo_livro;
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_book_by_autor_id_query, (autor_id,))
                return cursor.fetchall()
            except sqlite3.OperationalError as e:
                print(f'Os parametros da consulta sao invalidos: {e}')
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_publisher_register(editora: Editora):

    print(f'Tentando inserir a editora: {str(editora)}')

    sql_publisher_check = """
        SELECT id FROM Editora WHERE nome = ?
    """

    sql_publisher_register = """
        INSERT INTO Editora (nome)
        VALUES (?)
    """

    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()

            cursor.execute(sql_publisher_check, (editora.nome,))
            existing_publisher = cursor.fetchone()

            if existing_publisher:
                print(f"Editora '{editora.nome}' já existe no banco de dados. Não será inserido novamente.")
                return existing_publisher[0]

            cursor.execute(sql_publisher_register, (
                editora.nome,
            ))

            id_editora = cursor.lastrowid

            try:
                conn.commit()
                print(f"Sucesso ao inserir a editora {editora.nome}")
                return id_editora
            except sqlite3.IntegrityError as e:
                print(f"Erro de integridade ao inserir os dados: {e}")
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_book_by_publisher_name_query(nome_editora: str):

    print(f'Buscando livros da editora: {nome_editora}')

    sql_book_by_publisher_name_query = """
        SELECT Livro.codigo_livro, Livro.titulo, Livro.edicao, Livro.ISBN, Livro.categoria, 
            Livro.ano_de_publicacao, Editora.nome AS editora, 
            Livro.quantidade_exemplares, GROUP_CONCAT(Autor.nome, ', ') AS autores
        FROM Livro
        INNER JOIN Editora ON Livro.id_editora = Editora.id
        LEFT JOIN LivroAutor ON Livro.codigo_livro = LivroAutor.codigo_livro
        LEFT JOIN Autor ON LivroAutor.id_autor = Autor.id
        WHERE Editora.nome = ?
        GROUP BY Livro.codigo_livro;
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_book_by_publisher_name_query, (nome_editora,))
                return cursor.fetchall()
            except sqlite3.OperationalError as e:
                print(f'Os parametros da consulta sao invalidos: {e}')
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_book_by_publisher_id_query(id_editora: str):

    print(f'Buscando livros pelo id da editora: {id_editora}')

    sql_book_by_editora_id_query = """
        SELECT Livro.codigo_livro, Livro.titulo, Livro.edicao, Livro.ISBN, Livro.categoria, 
            Livro.ano_de_publicacao, Editora.nome AS editora, 
            Livro.quantidade_exemplares, GROUP_CONCAT(Autor.nome, ', ') AS autores
        FROM Livro
        INNER JOIN Editora ON Livro.id_editora = Editora.id
        LEFT JOIN LivroAutor ON Livro.codigo_livro = LivroAutor.codigo_livro
        LEFT JOIN Autor ON LivroAutor.id_autor = Autor.id
        WHERE Livro.id_editora = ?
        GROUP BY Livro.codigo_livro;
    """

    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_book_by_editora_id_query, (id_editora,))
                return cursor.fetchall()
            except sqlite3.OperationalError as e:
                print(f'Os parametros da consulta sao invalidos: {e}')
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_book_by_category_query(category: str):

    print(f'Buscando livros pela categoria: {category}')

    sql_book_by_category_query = """
        SELECT Livro.codigo_livro, Livro.titulo, Livro.edicao, Livro.ISBN, Livro.categoria, 
            Livro.ano_de_publicacao, Editora.nome AS editora, 
            Livro.quantidade_exemplares, GROUP_CONCAT(Autor.nome, ', ') AS autores
        FROM Livro
        INNER JOIN Editora ON Livro.id_editora = Editora.id
        LEFT JOIN LivroAutor ON Livro.codigo_livro = LivroAutor.codigo_livro
        LEFT JOIN Autor ON LivroAutor.id_autor = Autor.id
        WHERE Livro.categoria = ?
        GROUP BY Livro.codigo_livro;
    """

    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_book_by_category_query, (category,))
                return cursor.fetchall()
            except sqlite3.OperationalError as e:
                print(f'Os parametros da consulta sao invalidos: {e}')
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_register_exemplar(livro: LivroDB):

    print(f'Tentando criar exemplar do livro: {livro.titulo}')

    sql_exemplar_register = """
        INSERT INTO Exemplar(codigo_livro, situacao) VALUES (
            ?, ?
        )
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_exemplar_register, (
                livro.codigo_livro,
                "em_stock"
            ))

            try:
                conn.commit()
                print(f"Sucesso ao inserir o exemplar do livro {livro.titulo}")
            except sqlite3.IntegrityError as e:
                print(f"Erro de integridade ao inserir os dados: {e}")
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_exemplar_book_id_query(book_id: int):

    print(f'Buscando exemplares com id do livro {book_id}')

    sql_exemplar_by_book_id = """
        SELECT Livro.codigo_livro, Livro.titulo, Livro.edicao, Livro.ISBN, Livro.categoria, 
            Livro.ano_de_publicacao, Editora.nome AS nome_editora, 
            Livro.quantidade_exemplares, GROUP_CONCAT(Autor.nome, ', ') AS autores,
            Exemplar.codigo_exemplar, Exemplar.situacao
        FROM Livro
        INNER JOIN Editora ON Livro.id_editora = Editora.id
        LEFT JOIN LivroAutor ON Livro.codigo_livro = LivroAutor.codigo_livro
        LEFT JOIN Autor ON LivroAutor.id_autor = Autor.id
        LEFT JOIN Exemplar ON Livro.codigo_livro = Exemplar.codigo_livro
        WHERE Livro.codigo_livro = ?
        GROUP BY Livro.codigo_livro, Exemplar.codigo_exemplar;
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_exemplar_by_book_id, (book_id,))
                return cursor.fetchall()
            except sqlite3.OperationalError as e:
                print(f'Os parametros da consulta sao invalidos: {e}')
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_exemplar_book_title_query(book_title: str):

    print(f'Buscando exemplares do livro {book_title}')
    
    sql_exemplar_by_book_title = """
        SELECT 
            Livro.codigo_livro, 
            Livro.titulo, 
            Livro.edicao, 
            Livro.ISBN, 
            Livro.categoria, 
            Livro.ano_de_publicacao, 
            Editora.nome AS nome_editora, 
            Livro.quantidade_exemplares, 
            GROUP_CONCAT(Autor.nome, ', ') AS autores,
            Exemplar.codigo_exemplar, 
            Exemplar.situacao
        FROM 
            Livro
        INNER JOIN 
            Editora ON Livro.id_editora = Editora.id
        LEFT JOIN 
            LivroAutor ON Livro.codigo_livro = LivroAutor.codigo_livro
        LEFT JOIN 
            Autor ON LivroAutor.id_autor = Autor.id
        LEFT JOIN 
            Exemplar ON Livro.codigo_livro = Exemplar.codigo_livro
        WHERE 
            Livro.titulo = ?
        GROUP BY 
            Livro.codigo_livro, 
            Exemplar.codigo_exemplar;
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_exemplar_by_book_title, (book_title,))
                return cursor.fetchall()
            except sqlite3.OperationalError as e:
                print(f'Os parametros da consulta sao invalidos: {e}')
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_exemplar_by_id_query(exemplar_id: int):

    print(f'Buscando exemplares pelo id{exemplar_id}')
    
    sql_exemplar_by_id = """
        SELECT 
            Livro.codigo_livro, 
            Livro.titulo, 
            Livro.edicao, 
            Livro.ISBN, 
            Livro.categoria, 
            Livro.ano_de_publicacao, 
            Editora.nome AS nome_editora, 
            Livro.quantidade_exemplares, 
            GROUP_CONCAT(Autor.nome, ', ') AS autores,
            Exemplar.codigo_exemplar, 
            Exemplar.situacao
        FROM 
            Livro
        INNER JOIN 
            Editora ON Livro.id_editora = Editora.id
        LEFT JOIN 
            LivroAutor ON Livro.codigo_livro = LivroAutor.codigo_livro
        LEFT JOIN 
            Autor ON LivroAutor.id_autor = Autor.id
        LEFT JOIN 
            Exemplar ON Livro.codigo_livro = Exemplar.codigo_livro
        WHERE 
            Exemplar.codigo_exemplar = ?
        GROUP BY 
            Livro.codigo_livro, 
            Exemplar.codigo_exemplar;
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_exemplar_by_id, (exemplar_id,))
                return cursor.fetchone()
            except sqlite3.OperationalError as e:
                print(f'Os parametros da consulta sao invalidos: {e}')
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_exemplar_by_autor_name_query(autor_name: str):

    print(f'Buscando exemplares do livro {autor_name}')
    
    sql_exemplar_by_autor_name = """
        SELECT 
            Livro.codigo_livro, 
            Livro.titulo, 
            Livro.edicao, 
            Livro.ISBN, 
            Livro.categoria, 
            Livro.ano_de_publicacao, 
            Editora.nome AS nome_editora, 
            Livro.quantidade_exemplares, 
            GROUP_CONCAT(Autor.nome, ', ') AS autores,
            Exemplar.codigo_exemplar, 
            Exemplar.situacao
        FROM 
            Livro
        INNER JOIN 
            Editora ON Livro.id_editora = Editora.id
        LEFT JOIN 
            LivroAutor ON Livro.codigo_livro = LivroAutor.codigo_livro
        LEFT JOIN 
            Autor ON LivroAutor.id_autor = Autor.id
        LEFT JOIN 
            Exemplar ON Livro.codigo_livro = Exemplar.codigo_livro
        WHERE 
            Livro.codigo_livro IN (SELECT codigo_livro FROM LivroAutor WHERE id_autor IN (SELECT id FROM Autor WHERE nome = ?))
        GROUP BY 
            Livro.codigo_livro, 
            Exemplar.codigo_exemplar;
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_exemplar_by_autor_name, (autor_name,))
                return cursor.fetchall()
            except sqlite3.OperationalError as e:
                print(f'Os parametros da consulta sao invalidos: {e}')
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_exemplar_by_autor_id_query(autor_id: int):

    print(f'Buscando exemplares pelo autor id {autor_id}')
    
    sql_exemplar_by_autor_id = """
        SELECT 
            Livro.codigo_livro, 
            Livro.titulo, 
            Livro.edicao, 
            Livro.ISBN, 
            Livro.categoria, 
            Livro.ano_de_publicacao, 
            Editora.nome AS nome_editora, 
            Livro.quantidade_exemplares, 
            GROUP_CONCAT(Autor.nome, ', ') AS autores,
            Exemplar.codigo_exemplar, 
            Exemplar.situacao
        FROM 
            Livro
        INNER JOIN 
            Editora ON Livro.id_editora = Editora.id
        LEFT JOIN 
            LivroAutor ON Livro.codigo_livro = LivroAutor.codigo_livro
        LEFT JOIN 
            Autor ON LivroAutor.id_autor = Autor.id
        LEFT JOIN 
            Exemplar ON Livro.codigo_livro = Exemplar.codigo_livro
        WHERE 
            Livro.codigo_livro IN (SELECT codigo_livro FROM LivroAutor WHERE id_autor IN (SELECT id FROM Autor WHERE id = ?))
        GROUP BY 
            Livro.codigo_livro, 
            Exemplar.codigo_exemplar;
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_exemplar_by_autor_id, (autor_id,))
                return cursor.fetchall()
            except sqlite3.OperationalError as e:
                print(f'Os parametros da consulta sao invalidos: {e}')
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_exemplar_by_publisher_name_query(nome_editora: str):

    print(f'Buscando exemplares pelo nome da editora {nome_editora}')
    
    sql_exemplar_by_publisher_name = """
        SELECT 
            Livro.codigo_livro, 
            Livro.titulo, 
            Livro.edicao, 
            Livro.ISBN, 
            Livro.categoria, 
            Livro.ano_de_publicacao, 
            Editora.nome AS nome_editora, 
            Livro.quantidade_exemplares, 
            GROUP_CONCAT(Autor.nome, ', ') AS autores,
            Exemplar.codigo_exemplar, 
            Exemplar.situacao
        FROM 
            Livro
        INNER JOIN 
            Editora ON Livro.id_editora = Editora.id
        LEFT JOIN 
            LivroAutor ON Livro.codigo_livro = LivroAutor.codigo_livro
        LEFT JOIN 
            Autor ON LivroAutor.id_autor = Autor.id
        LEFT JOIN 
            Exemplar ON Livro.codigo_livro = Exemplar.codigo_livro
        WHERE 
            Editora.nome = ?
        GROUP BY 
            Livro.codigo_livro, 
            Exemplar.codigo_exemplar;
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_exemplar_by_publisher_name, (nome_editora,))
                return cursor.fetchall()
            except sqlite3.OperationalError as e:
                print(f'Os parametros da consulta sao invalidos: {e}')
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_exemplar_by_publisher_id_query(id_editora: int):

    print(f'Buscando exemplares pelo nome da editora {id_editora}')
    
    sql_exemplar_by_publisher_id = """
        SELECT 
            Livro.codigo_livro, 
            Livro.titulo, 
            Livro.edicao, 
            Livro.ISBN, 
            Livro.categoria, 
            Livro.ano_de_publicacao, 
            Editora.nome AS nome_editora, 
            Livro.quantidade_exemplares, 
            GROUP_CONCAT(Autor.nome, ', ') AS autores,
            Exemplar.codigo_exemplar, 
            Exemplar.situacao
        FROM 
            Livro
        INNER JOIN 
            Editora ON Livro.id_editora = Editora.id
        LEFT JOIN 
            LivroAutor ON Livro.codigo_livro = LivroAutor.codigo_livro
        LEFT JOIN 
            Autor ON LivroAutor.id_autor = Autor.id
        LEFT JOIN 
            Exemplar ON Livro.codigo_livro = Exemplar.codigo_livro
        WHERE 
            Editora.id = ?
        GROUP BY 
            Livro.codigo_livro, 
            Exemplar.codigo_exemplar;
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_exemplar_by_publisher_id, (id_editora,))
                return cursor.fetchall()
            except sqlite3.OperationalError as e:
                print(f'Os parametros da consulta sao invalidos: {e}')
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_exemplar_by_category_query(category: str):

    print(f'Buscando exemplares pela categoria {category}')
    
    sql_exemplar_by_category = """
        SELECT 
            Livro.codigo_livro, 
            Livro.titulo, 
            Livro.edicao, 
            Livro.ISBN, 
            Livro.categoria, 
            Livro.ano_de_publicacao, 
            Editora.nome AS nome_editora, 
            Livro.quantidade_exemplares, 
            GROUP_CONCAT(Autor.nome, ', ') AS autores,
            Exemplar.codigo_exemplar, 
            Exemplar.situacao
        FROM 
            Livro
        INNER JOIN 
            Editora ON Livro.id_editora = Editora.id
        LEFT JOIN 
            LivroAutor ON Livro.codigo_livro = LivroAutor.codigo_livro
        LEFT JOIN 
            Autor ON LivroAutor.id_autor = Autor.id
        LEFT JOIN 
            Exemplar ON Livro.codigo_livro = Exemplar.codigo_livro
        WHERE 
            Livro.categoria = ?
        GROUP BY 
            Livro.codigo_livro, 
            Exemplar.codigo_exemplar;
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_exemplar_by_category, (category,))
                return cursor.fetchall()
            except sqlite3.OperationalError as e:
                print(f'Os parametros da consulta sao invalidos: {e}')
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_exemplar_by_ISBN_query(ISBN):

    print(f'Buscando exemplares pelo ISBN {ISBN}')
    
    sql_exemplar_by_ISBN = """
        SELECT 
            Livro.codigo_livro, 
            Livro.titulo, 
            Livro.edicao, 
            Livro.ISBN, 
            Livro.categoria, 
            Livro.ano_de_publicacao, 
            Editora.nome AS nome_editora, 
            Livro.quantidade_exemplares, 
            GROUP_CONCAT(Autor.nome, ', ') AS autores,
            Exemplar.codigo_exemplar, 
            Exemplar.situacao
        FROM 
            Livro
        INNER JOIN 
            Editora ON Livro.id_editora = Editora.id
        LEFT JOIN 
            LivroAutor ON Livro.codigo_livro = LivroAutor.codigo_livro
        LEFT JOIN 
            Autor ON LivroAutor.id_autor = Autor.id
        LEFT JOIN 
            Exemplar ON Livro.codigo_livro = Exemplar.codigo_livro
        WHERE 
            Livro.ISBN = ?
        GROUP BY 
            Livro.codigo_livro, 
            Exemplar.codigo_exemplar;
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_exemplar_by_ISBN, (ISBN,))
                return cursor.fetchall()
            except sqlite3.OperationalError as e:
                print(f'Os parametros da consulta sao invalidos: {e}')
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_all_exemplars_query():

    print(f'Buscando todos os exemplares do banco')
    
    sql_all_exemplars = """
        SELECT 
            Livro.codigo_livro, 
            Livro.titulo, 
            Livro.edicao, 
            Livro.ISBN, 
            Livro.categoria, 
            Livro.ano_de_publicacao, 
            Editora.nome AS nome_editora, 
            Livro.quantidade_exemplares, 
            GROUP_CONCAT(Autor.nome, ', ') AS autores,
            Exemplar.codigo_exemplar, 
            Exemplar.situacao
        FROM 
            Livro
        INNER JOIN 
            Editora ON Livro.id_editora = Editora.id
        LEFT JOIN 
            LivroAutor ON Livro.codigo_livro = LivroAutor.codigo_livro
        LEFT JOIN 
            Autor ON LivroAutor.id_autor = Autor.id
        LEFT JOIN 
            Exemplar ON Livro.codigo_livro = Exemplar.codigo_livro
        GROUP BY 
            Livro.codigo_livro, 
            Exemplar.codigo_exemplar;
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_all_exemplars)
                return cursor.fetchall()
            except sqlite3.OperationalError as e:
                print(f'Os parametros da consulta sao invalidos: {e}')
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_register_author(autor: Autor):

    print(f'Tentando inserir o autor: {str(autor)}')
    
    sql_autor_check = """
        SELECT id FROM Autor WHERE nome = ?
    """

    sql_autor_register = """
        INSERT INTO Autor(nome) VALUES (?)
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()

            cursor.execute(sql_autor_check, (autor.nome,))
            existing_author = cursor.fetchone()

            if existing_author:
                print(f"Autor '{autor.nome}' já existe no banco de dados. Não será inserido novamente.")
                return existing_author[0]

            cursor.execute(sql_autor_register, (autor.nome,))

            id_autor = cursor.lastrowid

            try:
                conn.commit()
                print(f"Sucesso ao inserir o autor {autor.nome}")
                return id_autor
            except sqlite3.IntegrityError as e:
                print(f"Erro de integridade ao inserir os dados: {e}")
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_register_employee(cadastro: Cadastro, funcionario: Funcionario):

    user = input("Crie um usuario: ")
    password = input("Crie uma senha: ")

    sql_user_data= """
        INSERT INTO Cadastro (logradouro, numero, complemento, bairro, UF, CEP, email, telefone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    sql_employee_register = """
        INSERT INTO Funcionario (nome, sobrenome, id_cadastro)
        VALUES (?, ?, ?)
    """

    sql_employee_login = """
        INSERT INTO Login(usuario, senha, id_cadastro)
        VALUES (?, ?, ?)
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            conn.execute('BEGIN')
            cursor.execute(sql_user_data, (
                cadastro.logradouro,
                cadastro.numero,
                cadastro.complemento,
                cadastro.bairro,
                cadastro.UF,
                cadastro.CEP,
                cadastro.email,
                cadastro.telefone
            ))

            id_cadastro = cursor.lastrowid

            cursor.execute(sql_employee_register, (
                funcionario.nome,
                funcionario.sobrenome,
                id_cadastro
            ))

            cursor.execute(sql_employee_login, (
                user,
                password,
                id_cadastro
            ))

            try:
                conn.execute('COMMIT')
                print(f'Sucesso ao realizar o cadastro de funcionario')
            except sqlite3.IntegrityError as e:
                print(f"Erro de integridade ao inserir os dados: {e}")

    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_search_employee_by_name(nome_funcionario):

    sql_search_employee_by_name= """
        SELECT id, nome, sobrenome, id_cadastro FROM Funcionario
        WHERE Funcionario.nome = ?
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_search_employee_by_name, (nome_funcionario,))
                return cursor.fetchone()
            except sqlite3.OperationalError as e:
                print(f'Os parametros da consulta sao invalidos: {e}')
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_search_user_by_name(nome_leitor):

    sql_search_user_by_name = """
        SELECT id, nome, sobrenome, id_cadastro FROM Leitor
        WHERE Leitor.nome = ?
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_search_user_by_name, (nome_leitor,))
                return cursor.fetchone()
            except sqlite3.OperationalError as e:
                print(f'Os parametros da consulta sao invalidos: {e}')
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_register_user(cadastro: Cadastro, leitor: Leitor):

    user = input("Crie um usuario: ")
    password = input("Crie uma senha: ")

    sql_user_data= """
        INSERT INTO Cadastro (logradouro, numero, complemento, bairro, UF, CEP, email, telefone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    sql_user_register = """
        INSERT INTO Funcionario (nome, sobrenome, id_cadastro)
        VALUES (?, ?, ?)
    """
    sql_user_login = """
        INSERT INTO Login(usuario, senha, id_cadastro)
        VALUES (?, ?, ?)
    """

    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            conn.execute('BEGIN')
            cursor.execute(sql_user_data, (
                cadastro.logradouro,
                cadastro.numero,
                cadastro.complemento,
                cadastro.bairro,
                cadastro.UF,
                cadastro.CEP,
                cadastro.email,
                cadastro.telefone
            ))

            id_cadastro = cursor.lastrowid

            cursor.execute(sql_user_register, (
                leitor.nome,
                leitor.sobrenome,
                id_cadastro
            ))

            cursor.execute(sql_user_login, (
                user,
                password,
                id_cadastro
            ))

            try:
                conn.execute('COMMIT')
                print(f'Sucesso ao realizar cadastro de usuario')
            except sqlite3.IntegrityError as e:
                print(f"Erro de integridade ao inserir os dados: {e}")

    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_make_emprestimo(exemplares: list, leitor: Leitor, funcionario: Funcionario):

    sql_emprestimo_register= """
        INSERT INTO Emprestimo (id_leitor, data_emprestimo, data_devolucao, id_funcionario)
        VALUES (?, ?, ?, ?)
    """

    sql_emprestimo_exemplar = """
        INSERT INTO Emprestimo_Exemplar (id_emprestimo, codigo_exemplar)
        VALUES (?, ?)
    """

    sql_update_exemplar_situation = """
        UPDATE Exemplar
        SET situacao = ?
        WHERE codigo_exemplar = ?
    """

    emprestimo = Emprestimo(
        leitor.id_leitor,
        data_emprestimo = datetime.now(),
        data_devolucao = datetime.now() + timedelta(days=15),
        id_funcionario = funcionario.id_funcionario
    )

    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            conn.execute('BEGIN')
            cursor.execute(sql_emprestimo_register, (
                emprestimo.id_leitor,
                emprestimo.data_emprestimo,
                emprestimo.data_devolucao, 
                emprestimo.id_funcionario
            ))

            id_emprestimo = cursor.lastrowid

            print(exemplares)
            for exemplar in exemplares:
                print(exemplar)
                cursor.execute(sql_emprestimo_exemplar, (
                    id_emprestimo,
                    exemplar[9]
                ))
                cursor.execute(sql_update_exemplar_situation, (
                    "emprestado",
                    exemplar[9]
                ))
            try:
                conn.execute('COMMIT')
            except sqlite3.IntegrityError as e:
                print(f"Erro de integridade ao inserir os dados: {e}")
                raise EmprestimoFailure

    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")
        raise EmprestimoFailure

def db_make_devolucao(emprestimo: Emprestimo, funcionario: Funcionario):

    sql_devolucao_register = """
        INSERT INTO Devolucao (id_emprestimo, id_funcionario, data_devolucao)
        VALUES (?, ?, ?)
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_devolucao_register, (
                emprestimo.id_emprestimo,
                funcionario.id_funcionario,
                datetime.datetime.now()
            ))

            try:
                conn.commit()
                print(f"Devolucao realizada pelo funcionario: {funcionario.nome}")
            except sqlite3.IntegrityError as e:
                print(f"Erro de integridade ao inserir os dados: {e}")
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def receive_book_inputs():
    LIVRO_INPUTS = (
        'titulo', 'edicao',
        'ISBN', 'categoria', 
        'ano_de_publicacao', 'editora', 
    )

    livro_inputs = [input(f"Digite o {input_name} do livro: ") for input_name in LIVRO_INPUTS]

    res = input('Este livro possui mais de um autor?[S/N]')
    autores = []
    if 'S' in res or 's' in res:
        while True:
            autor = input('Digite o nome do autor: ')
            if autor in autores:
                print(f'Voce nao pode colocar autores iguais no mesmo livro')
                continue
            autores.append(autor)
            r = input('Digitar mais um? [S/N]')
            if 'N' in r or 'n' in r:
                break
    else:
        autor = input('Digite o nome do autor: ')
        autores.append(autor)

    return livro_inputs, autores

def receive_editor_inputs():
    EDITORA_INPUTS = ('nome')
    editora_inputs = input_comprehension(EDITORA_INPUTS)

    return editora_inputs

def receive_login_inputs():
    LOGIN_INPUTS = ('usuario', 'senha')
    login_inputs = input_comprehension(LOGIN_INPUTS)
    return login_inputs

def receive_cadastro_inputs():
    CADASTRO_INPUTS = (
        'logradouro', 'numero', 
        'complemento', 'bairro', 
        'UF', 'CEP', 'email', 'telefone'
    )
    cadastro_inputs = input_comprehension(CADASTRO_INPUTS)

    return cadastro_inputs

def receive_employee_inputs():
    FUNCIONARIO_INPUTS = (
        'nome', 'sobrenome',
        'id_cadatro'
    )
    funcionario_inputs = input_comprehension(FUNCIONARIO_INPUTS)

    return funcionario_inputs

def receive_user_inputs():
    LEITOR_INPUTS = (
        'nome', 'sobrenome',
        'id_cadastro'
    )
    leitor_inputs = input_comprehension(LEITOR_INPUTS)

    return leitor_inputs

def _book_register():

    print("CADASTRO DE LIVRO")

    livro_inputs, autores = receive_book_inputs()

    autor_list = []

    for autor in autores:
        autor_to_insert = Autor(autor)
        id_autor = db_register_author(autor_to_insert)
        autor_list.append(AutorDB(id_autor, autor))

    titulo = livro_inputs[0]
    edicao = livro_inputs[1]
    ISBN = livro_inputs[2]
    categoria = livro_inputs[3]
    ano_publicacao = livro_inputs[4]
    editora = livro_inputs[5]

    id_editora = db_publisher_register(Editora(editora))

    livro = Livro(
        titulo=titulo, edicao=edicao, 
        ISBN=ISBN, categoria=categoria, 
        ano_de_publicacao=ano_publicacao, 
        id_editora=id_editora, autores=autor_list
    )

    db_book_register(livro)

def _exemplar_register(titulo_livro = None):

    print('CADASTRO DE EXEMPLAR')

    if not titulo_livro:
        titulo_livro = input(f'Digite o titulo do livro que deseja criar o exemplar: ')
    
    livro_db = db_book_by_title_query(titulo_livro)
    print(livro_db)

    if not livro_db:
        print(f'Nao existe nenhum livro com esse titulo')
        return
    
    livro = LivroDB(
        codigo_livro=livro_db[0][0],
        titulo=livro_db[0][1],
        edicao=livro_db[0][2],
        ISBN=livro_db[0][3],
        categoria=livro_db[0][4],
        ano_de_publicacao=livro_db[0][5],
        id_editora=livro_db[0][6],
        quantidade_exemplares=livro_db[0][7]
    )

    db_register_exemplar(livro)
        
def _search_all_books():
    
    print('BUSCA DE LIVROS')

    livros = db_all_books_query()

    if livros:
        for livro in livros:
            print(livro)
    else:
        print('Nao existe nenhum livro cadastrado')

def _search_book_by_title(book_title):

    print('BUSCA DE LIVRO POR TITULO')

    livros = db_book_by_title_query(book_title)

    if livros:
        for livro in livros:
            print(livro)
    else:
        print(f'Nao foram encontrados livros com o titulo {book_title}')

def _search_books_by_publisher_name(nome_editora):

    print('BUSCA DE LIVRO POR EDITORA')

    livros = db_book_by_publisher_name_query(nome_editora)

    if livros:
        for livro in livros:
            print(livro)
    else:
        print(f'Nao foram encontrados livros da editora {nome_editora}')

def _search_book_by_ISBN(ISBN):

    print('BUSCA DE LIVRO POR ISBN')

    livro = db_book_by_ISBN_query(ISBN)

    if livro:
        print(livro)
    else:
        print(f'Nao foi encontrado livro para o ISBN: {ISBN}')

def _search_book_by_id(id):

    print('BUSCA DE LIVRO POR ID')

    livro = db_book_by_ID_query(id)

    if livro:
        print(livro)
    else:
        print(f'Nao existe livro cadastrado para o id: {id}')

def _search_books_by_autor_name(autor_name):

    print('BUSCA DE LIVRO POR AUTOR')

    livros = db_books_by_autor_name_query(autor_name)

    if livros:
        for livro in livros:
            print(livro)
    else:
        print(f'Nao foi encontrado livros do autor: {autor_name}')

def _search_books_by_autor_id(autor_id):

    print('BUSCA DE LIVROS POR ID DO AUTOR')

    livros = db_books_by_author_id_query(autor_id)

    if livros:
        for livro in livros:
            print(livro)
    else:
        print(f'Nao foi encontrados livros pelo id do autor {autor_id}')

def _search_books_by_publisher_id(editora_id):

    print('BUSCA DE LIVRO PELO ID DA EDITORA')

    livros = db_book_by_publisher_id_query(editora_id)

    if livros:
        for livro in livros:
            print(livro)
    else:
        print(f'Nao foram encontrados livros pelo id da editora: {editora_id}')

def _search_book_by_category(category):
    
    print('BUSCA DE LIVROS PELA CATEGORIA')

    livros = db_book_by_category_query(category)

    if livros:
        for livro in livros:
            print(livro)
    else:
        print(f'Nao foram encontrados livros da categoria {category}')

def _search_exemplar_by_book_id(book_id):

    print('BUSCA DE EXEMPLARES PELO BOOK ID')

    livros = db_exemplar_book_id_query(book_id)

    if livros:
        for livro in livros:
            print(livro)
    else:
        print(f'Nao foram encontrados exemplares pelo book id {book_id}')

def _search_exemplar_by_book_title(book_title):

    print('BUSCA DE EXEMPLARES PELO TITULO DO LIVRO')

    livros = db_exemplar_book_title_query(book_title)

    if livros:
        for livro in livros:
            print(livro)
    else:
        print(f'Nao foram encontrados exemplares pelo titulo do livro {book_title}')

def _search_exemplar_by_ISBN(ISBN):

    print('BUSCA DE EXEMPLARES POR ISBN')

def _search_exemplar_by_id(exemplar_id):

    print('BUSCA DE EXEMPLARES PELO ID')

    livro = db_exemplar_by_id_query(exemplar_id)

    if livro:
        print(livro)
    else:
        print(f'Nao foi encontrado exemplar com id {exemplar_id}')

def _search_exemplar_by_autor_name(autor_name):

    print('BUSCA DE EXEMPLARES PELO NOME DO AUTOR')

    livros = db_exemplar_by_autor_name_query(autor_name)

    if livros:
        for livro in livros:
            print(livro)
    else:
        print(f'Nao foram encontrados exemplares pelo autor {autor_name}')

def _search_exemplar_by_autor_id(autor_id):

    print('BUSCA DE EXEMPLARES PELO ID DO AUTOR')

    livros = db_exemplar_by_autor_id_query(autor_id)

    if livros:
        for livro in livros:
            print(livro)
    else:
        print(f'Nao foram encontrados exemplares pelo id autor {autor_id}')

def _search_exemplar_by_publisher_name(nome_editora):

    print('BUSCA DE EXEMPLARES PELO NOME DA EDITORA')

    livros = db_exemplar_by_publisher_name_query(nome_editora)

    if livros:
        for livro in livros:
            print(livro)
    else:
        print(f'Nao foram encontrados exemplares da editora {nome_editora}')

def _search_exemplar_by_publisher_id(id_editora):

    print('BUSCA DE EXEMPLARES PELO ID DA EDITORA')

    livros = db_exemplar_by_publisher_id_query(id_editora)

    if livros:
        for livro in livros:
            print(livro)
    else:
        print(f'Nao foram encontrados exemplares pelo id editora {id_editora}')

def _search_exemplar_by_category(category):

    print('BUSCA DE EXEMPLARES POR CATEGORIA')

    livros = db_exemplar_by_category_query(category)

    if livros:
        for livro in livros:
            print(livro)
    else:
        print(f'Nao foram encontrados exemplares da categoria {category}')

def _search_all_exemplares():

    print('BUSCA DE TODOS OS EXEMPLARES')

    livros = db_all_exemplars_query()

    if livros:
        for livro in livros:
            print(livro)
    else:
        print(f'Nao existe nenhum exemplar cadastrado no banco')

def _make_emprestimo():

    print('REALIZACAO DE EMPRESTIMO')

    exemplares = []
    funcionario = ''
    leitor = ''

    while True:

        exemplar_id = input('Digite o codigo do exemplar: ')
        exemplar_db = db_exemplar_by_id_query(exemplar_id)

        if exemplar_db:
            exemplares.append(exemplar_db)
        else:
            print(f'Esse livro nao existe')
            continue

        res = input('Deseja emprestar mais um exemplar? [S/N]')
        if 'N' in res or 'n' in res:
            break
    
    while True:

        nome_funcionario = input('Digite o nome do funcionario: ')
        funcionario_db = db_search_employee_by_name(nome_funcionario)

        if funcionario_db:
            funcionario = Funcionario(
                funcionario_db[0],
                funcionario_db[1],
                funcionario_db[2],
                funcionario_db[3],
            )
            break
        else:
            print('Esse funcionario nao existe')
    
    while True:
        
        nome_leitor = input('Digite o nome do leitor: ')
        leitor_db = db_search_user_by_name(nome_leitor)

        if leitor_db:
            leitor = Leitor(
                leitor_db[0],
                leitor_db[1],
                leitor_db[2],
                leitor_db[3],
            )
            break
        else:
            print('Esse usuario nao existe')

    try:

        db_make_emprestimo(exemplares, leitor, funcionario)

        print('Emprestimo realizado com sucesso, detalhes: ')
        print('Exemplares: {}'.format(', '.join(str(exemplar) for exemplar in exemplares)))
        print(f'Leitor: {leitor.nome}')
        print(f'Realizado pelo funcionario: {funcionario.nome}')

    except EmprestimoFailure:
        print(f'O emprestimo nao pode ser realizado')

if __name__=='__main__':

    if not os.path.exists(database_file_path):
        init_dabase('./init.sql')

    session = {}

    print("Você deve estar logado para acessar o sistema")

    while True:
        login = receive_login_inputs()
        if make_login(login[0], login[1]):
            session['user'] = login[0]
            session['password'] = login[1]
            print(f"Funcionaro {session['user']} logado com sucesso!")
            break
        else:
            print("Usuario ou senha incorretos")
    
    ##_book_register()
    ##_exemplar_register()
    _search_all_books()
    _search_book_by_title('math')
    _search_book_by_id(2)
    _search_books_by_publisher_name('cobra')
    _search_books_by_publisher_id(1)
    _search_book_by_ISBN(432432)
    _search_books_by_autor_name('pedrelli')
    _search_books_by_autor_id(2)
    _search_book_by_category('pijama')
    _search_exemplar_by_book_id(1)
    _search_exemplar_by_book_title('pijama')
    _search_exemplar_by_ISBN(432432)
    _search_exemplar_by_id(1)
    _search_exemplar_by_autor_name('lucas')
    _search_exemplar_by_autor_id(1)
    _search_exemplar_by_publisher_name('ed_pijama')
    _search_exemplar_by_publisher_id(1)
    _search_exemplar_by_category('pijama')
    _search_all_exemplares()
    _make_emprestimo()



        

    

