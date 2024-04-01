import sqlite3
import os

from models import *
from utils import input_comprehension
from config import options, database_file_path

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
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_publisher_register(editora: Editora):

    print(f'Tentando inserir a editora: {str(editora)}')

    sql_publisher_register = """
        INSERT INTO Editora (nome)
        VALUES (?)
    """

    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
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

def db_register_exemplar(livro: Livro):

    sql_exemplar_register = """
        INSERT INTO Exemplar VALUES (
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
                print(f"Sucesso ao inserir o exemplar do livro {livro.nome}")
            except sqlite3.IntegrityError as e:
                print(f"Erro de integridade ao inserir os dados: {e}")
    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

def db_register_author(autor: Autor):

    print(f'Tentando inserir o autor: {str(autor)}')

    sql_autor_register = """
        INSERT INTO Autor(nome) VALUES (?)
    """
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
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
        VALUES (?, ?, ?, ?, ?)
    """

    sql_emprestimo_exemplar = """
        INSERT INTO Emprestimo_Exemplar (id_emprestimo, codigo_exemplar)
        VALUES (?, ?)
    """

    sql_update_exemplar_situation = """
        UPDATE Exemplar
        SET situacao_exemplar = ?
    """

    emprestimo = Emprestimo(
        leitor.id_leitor,
        data_emprestimo = datetime.datetime.now(),
        data_devolucao = datetime.datetime.now() + datetime.timedelta(days=15),
        id_funcionario = funcionario.id
    )

    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            conn.execute('BEGIN')
            cursor.execute(sql_emprestimo_register, (
                emprestimo.codigo_exemplar,
                emprestimo.id_leitor,
                emprestimo.data_emprestimo,
                emprestimo.data_devolucao, 
                emprestimo.id_funcionario
            ))

            id_emprestimo = cursor.lastrowid

            for exemplar in exemplares:
                cursor.execute(sql_emprestimo_exemplar, (
                    id_emprestimo,
                    exemplar.codigo_exemplar
                ))
                cursor.execute(sql_update_exemplar_situation, (
                    "emprestado"
                ))
            try:
                conn.execute('COMMIT')
            except sqlite3.IntegrityError as e:
                print(f"Erro de integridade ao inserir os dados: {e}")

    except sqlite3.Error as e:
        print(f"Falha ao conectar com o banco: {e}")

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
            autores.append(autor)
            r = input('Digitar mais um? [S/N]')
            if 'N' in r or 'n' in r:
                break
    else:
        autor = input('Digite o nome do autor: ')

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
            continue

    _book_register()
    


        

    

