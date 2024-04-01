from datetime import datetime
from enum import Enum

class SituacaoExemplar(Enum):
    emprestado = "emprestado"
    em_stock = "em_stock"

class LivroDB:
    def __init__(self, codigo_livro, titulo, edicao, ISBN, categoria, ano_de_publicacao, id_editora, quantidade_exemplares=0):
        self.codigo_livro = codigo_livro
        self.titulo = titulo
        self.edicao = edicao
        self.ISBN = ISBN
        self.categoria = categoria
        self.ano_de_publicacao = ano_de_publicacao
        self.id_editora = id_editora
        self.quantidade_exemplares = quantidade_exemplares
    
    def __init__(self):
        return( 
            f'codigo livro: {self.codigo_livro}'
            + f'titulo: {self.titulo}, edicao: {self.edicao}'
            + f'ISBN: {self.ISBN}, categoria: {self.categoria}'
            + f'ano de publicacao: {self.ano_de_publicacao}'
            + f'id_editora: {self.id_editora}'
            + f'quantidade de exemplares: {self.quantidade_exemplares}'
        )

class Livro:
    def __init__(self, titulo, edicao, ISBN, categoria, ano_de_publicacao, id_editora, autores, quantidade_exemplares=0):
        self.titulo = titulo
        self.edicao = edicao
        self.ISBN = ISBN
        self.categoria = categoria
        self.ano_de_publicacao = ano_de_publicacao
        self.id_editora = id_editora
        self.quantidade_exemplares = quantidade_exemplares
        self.autores = autores
    
    def __str__(self):
        autores_str = [str(autor) for autor in self.autores]
        return (
            f'titulo: {self.titulo}, edicao: {self.edicao}, '
            + f'ISBN: {self.ISBN}, categoria: {self.categoria}, '
            + f'ano de publicacao: {self.ano_de_publicacao}, '
            + f'id_editora: {self.id_editora}, '
            + f'quantidade de exemplares: {self.quantidade_exemplares}, '
            + f'autores: {autores_str}'
        )
    
class AutorDB:
    def __init__(self, id_autor, nome):
        self.id_autor = id_autor
        self.nome = nome

    def __str__(self):
        return (
            f'id autor: {self.id_autor}, '
            + f'nome: {self.nome}'
        )
class Autor:
    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return f'nome: {self.nome}'

class Exemplar:
    def __init__(self, codigo_exemplar, codigo_livro, situacao):
        self.codigo_exemplar = codigo_exemplar
        self.codigo_livro = codigo_livro
        self.situacao = situacao

    def __str__(self):
        return f'codigo exemplar: {self.codigo_exemplar} \
            codigo livro: {self.codigo_livro} \
            situacao: {self.situacao}'

class EditoraDB:
    def __init__(self, id_editora, nome):
        self.id_editora = id_editora
        self.nome = nome
    
    def __str__(self):
        return f'id: {self.id}, nome: {self.nome}'

class Editora:
    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return f'nome: {self.nome}'

class Funcionario:
    def __init__(self, id_funcionario, nome, sobrenome, id_cadastro):
        self.id_funcionario = id_funcionario
        self.nome = nome
        self.sobrenome = sobrenome
        self.id_cadastro = id_cadastro

class Leitor:
    def __init__(self, id_leitor, nome, sobrenome, id_cadastro):
        self.id_leitor = id_leitor
        self.nome = nome
        self.sobrenome = sobrenome
        self.id_cadastro = id_cadastro

class Cadastro:
    def __init__(self, id_cadastro, logradouro, numero, complemento, bairro, UF, CEP, email, telefone):
        self.id_cadastro = id_cadastro
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.UF = UF
        self.CEP = CEP
        self.email = email
        self.telefone = telefone

class Emprestimo:
    def __init__(self, id_emprestimo, codigo_exemplar, id_leitor, data_emprestimo, data_devolucao, id_funcionario):
        self.id_emprestimo = id_emprestimo
        self.codigo_exemplar = codigo_exemplar
        self.id_leitor = id_leitor
        self.data_emprestimo = data_emprestimo
        self.data_devolucao = data_devolucao
        self.id_funcionario = id_funcionario

class Emprestimo_Exemplar:
    def __init__(self, id_emprestimo, codigo_exemplar):
        self.id_emprestimo = id_emprestimo
        self.codigo_exemplar = codigo_exemplar

class Devolucao:
    def __init__(self, id_emprestimo, id_funcionario, data_devolucao):
        self.id_emprestimo = id_emprestimo
        self.id_funcionario = id_funcionario
        self.data_devolucao = data_devolucao

class Relatorio:
    def __init__(self, id_relatorio, id_funcionario, id_emprestimo, descricao, created_at=None):
        self.id_relatorio = id_relatorio
        self.id_funcionario = id_funcionario
        self.id_emprestimo = id_emprestimo
        self.descricao = descricao
        self.created_at = created_at if created_at else datetime.now()

class Login:
    def __init__(self, id_cadastro, usuario, senha):
        self.id_cadastro = id_cadastro
        self.usuario = usuario
        self.senha = senha