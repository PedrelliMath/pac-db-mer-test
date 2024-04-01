CREATE TABLE IF NOT EXISTS `Livro` (
  `codigo_livro` INTEGER UNIQUE PRIMARY KEY NOT NULL,
  `titulo` TEXT NOT NULL,
  `edicao` INTEGER NOT NULL,
  `ISBN` VARCHAR(20) UNIQUE NOT NULL,
  `categoria` TEXT NOT NULL,
  `ano_de_publicacao` DATE NOT NULL,
  `id_editora` INTEGER NOT NULL,
  `quantidade_exemplares` INTEGER DEFAULT 0,
  FOREIGN KEY (`id_editora`) REFERENCES `Editora` (`id`)
);

CREATE TABLE IF NOT EXISTS `Autor` (
  `id` INTEGER UNIQUE PRIMARY KEY NOT NULL,
  `nome` TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS `LivroAutor` (
  `id_autor` INTEGER,
  `codigo_livro` INTEGER NOT NULL,
  FOREIGN KEY (`id_autor`) REFERENCES `Autor` (`id`),
  FOREIGN KEY (`codigo_livro`) REFERENCES `Livro` (`codigo_livro`)
);

CREATE TABLE IF NOT EXISTS `Exemplar` (
  `codigo_exemplar` INTEGER UNIQUE PRIMARY KEY NOT NULL,
  `codigo_livro` INTEGER NOT NULL,
  `situacao` TEXT NOT NULL CHECK (situacao IN ('emprestado', 'em_stock')),
  FOREIGN KEY (`codigo_livro`) REFERENCES `Livro` (`codigo_livro`)
);

CREATE TABLE IF NOT EXISTS `Editora` (
  `id` INTEGER UNIQUE PRIMARY KEY NOT NULL,
  `nome` TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS `Funcionario` (
  `id` INTEGER UNIQUE PRIMARY KEY NOT NULL,
  `nome` TEXT NOT NULL,
  `sobrenome` TEXT NOT NULL,
  `id_cadastro` INTEGER NOT NULL,
  FOREIGN KEY (`id_cadastro`) REFERENCES `Cadastro` (`id`)
);

CREATE TABLE IF NOT EXISTS `Leitor` (
  `id` INTEGER UNIQUE PRIMARY KEY NOT NULL,
  `nome` TEXT NOT NULL,
  `sobrenome` TEXT NOT NULL,
  `id_cadastro` INTEGER NOT NULL,
  FOREIGN KEY (`id_cadastro`) REFERENCES `Cadastro` (`id`)
);

CREATE TABLE IF NOT EXISTS `Cadastro` (
  `id` INTEGER UNIQUE PRIMARY KEY NOT NULL,
  `logradouro` TEXT NOT NULL,
  `numero` INTEGER NOT NULL,
  `complemento` TEXT NOT NULL,
  `bairro` TEXT NOT NULL,
  `UF` VARCHAR(2) NOT NULL,
  `CEP` VARCHAR(8) NOT NULL,
  `email` TEXT NOT NULL,
  `telefone` TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS `Emprestimo` (
  `id` INTEGER UNIQUE PRIMARY KEY NOT NULL,
  `id_leitor` INTEGER NOT NULL,
  `data_emprestimo` DATE NOT NULL,
  `data_devolucao` DATE NOT NULL,
  `id_funcionario` INTEGER NOT NULL,
  FOREIGN KEY (`id_leitor`) REFERENCES `Leitor` (`id`),
  FOREIGN KEY (`id_funcionario`) REFERENCES `Funcionario` (`id`)
);

CREATE TABLE IF NOT EXISTS `Emprestimo_Exemplar` (
  `id_emprestimo` INTEGER,
  `codigo_exemplar` INTEGER,
  PRIMARY KEY (`id_emprestimo`, `codigo_exemplar`),
  FOREIGN KEY (`id_emprestimo`) REFERENCES `Emprestimo` (`id`)
);

CREATE TABLE IF NOT EXISTS `Devolucao` (
  `id_emprestimo` INTEGER UNIQUE PRIMARY KEY NOT NULL,
  `id_funcionario` INTEGER NOT NULL,
  `data_devolucao` DATE NOT NULL,
  FOREIGN KEY (`id_emprestimo`) REFERENCES `Emprestimo` (`id`),
  FOREIGN KEY (`id_funcionario`) REFERENCES `Funcionario` (`id`)
);

CREATE TABLE IF NOT EXISTS `Relatorio` (
  `id` INTEGER UNIQUE PRIMARY KEY NOT NULL,
  `id_funcionario` INTEGER NOT NULL,
  `id_emprestimo` INTEGER NOT NULL,
  `descricao` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
  FOREIGN KEY (`id_funcionario`) REFERENCES `Funcionario` (`id`),
  FOREIGN KEY (`id_emprestimo`) REFERENCES `Emprestimo` (`id`)
);

CREATE TABLE IF NOT EXISTS `Login` (
  `id_cadastro` INTEGER UNIQUE PRIMARY KEY NOT NULL,
  `usuario` TEXT NOT NULL,
  `senha` TEXT NOT NULL,
  FOREIGN KEY (`id_cadastro`) REFERENCES `Cadastro` (`id`)
);

CREATE TABLE IF NOT EXISTS `Autor_LivroAutor` (
  `Autor_id` INTEGER,
  `LivroAutor_id_autor` INTEGER,
  PRIMARY KEY (`Autor_id`, `LivroAutor_id_autor`),
  FOREIGN KEY (`Autor_id`) REFERENCES `Autor` (`id`),
  FOREIGN KEY (`LivroAutor_id_autor`) REFERENCES `LivroAutor` (`id_autor`)
);

CREATE TABLE IF NOT EXISTS `Livro_LivroAutor` (
  `Livro_codigo_livro` INTEGER,
  `LivroAutor_codigo_livro` INTEGER,
  PRIMARY KEY (`Livro_codigo_livro`, `LivroAutor_codigo_livro`),
  FOREIGN KEY (`Livro_codigo_livro`) REFERENCES `Livro` (`codigo_livro`),
  FOREIGN KEY (`LivroAutor_codigo_livro`) REFERENCES `LivroAutor` (`codigo_livro`)
);

CREATE TABLE IF NOT EXISTS `Exemplar_Emprestimo_Exemplar` (
  `Exemplar_codigo_exemplar` INTEGER,
  `Emprestimo_Exemplar_codigo_exemplar` INTEGER,
  PRIMARY KEY (`Exemplar_codigo_exemplar`, `Emprestimo_Exemplar_codigo_exemplar`),
  FOREIGN KEY (`Exemplar_codigo_exemplar`) REFERENCES `Exemplar` (`codigo_exemplar`),
  FOREIGN KEY (`Emprestimo_Exemplar_codigo_exemplar`) REFERENCES `Emprestimo_Exemplar` (`codigo_exemplar`)
);

CREATE TRIGGER incrementar_quantidade_exemplar
AFTER INSERT ON Exemplar
BEGIN
    UPDATE Livro
    SET quantidade_exemplares = quantidade_exemplares + 1
    WHERE id = NEW.codigo_livro;
END;

INSERT INTO Cadastro (id, logradouro, numero, complemento, bairro, UF, CEP, email, telefone) VALUES
(1, 'Rua das Flores', 123, 'Apto 101', 'Centro', 'SP', '12345678', 'joao@example.com', '(11) 98765-4321'),
(2, 'Avenida dos Pássaros', 456, 'Casa', 'Jardim América', 'RJ', '87654321', 'maria@example.com', '(21) 12345-6789'),
(3, 'Rua das Pedras', 789, 'Sala 203', 'Centro', 'MG', '54321678', 'carlos@example.com', '(31) 67890-1234');

INSERT INTO Funcionario (nome, sobrenome, id_cadastro) VALUES
('matheus', 'mauricio', 1);

INSERT INTO Login (id_cadastro, usuario, senha) VALUES
(1, 'matheus', '123');