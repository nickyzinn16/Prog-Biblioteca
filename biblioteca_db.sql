CREATE DATABASE biblioteca_db;

USE biblioteca_db;

CREATE TABLE livro (
    id_livro        INT AUTO_INCREMENT PRIMARY KEY,
    titulo          VARCHAR(100)    NOT NULL,
    autor           VARCHAR(100)    NOT NULL,
    editora         VARCHAR(100)    DEFAULT NULL,
    ano_publicacao  INT(4)          DEFAULT NULL,
    categoria       VARCHAR(50)     DEFAULT NULL,
    quantidade      INT(10)         NOT NULL DEFAULT 1
);

CREATE TABLE utilizador (
    id_utilizador   INT AUTO_INCREMENT PRIMARY KEY,
    nome            VARCHAR(100)    NOT NULL,
    idade           INT(10)         NOT NULL,
    email           VARCHAR(50)     NOT NULL UNIQUE,
    password        VARCHAR(255)    NOT NULL,
    tipo_utilizador VARCHAR(20)     NOT NULL DEFAULT 'cliente',
    data_registo    DATE            DEFAULT NULL,
    telefone        VARCHAR(20)     DEFAULT NULL UNIQUE
);

CREATE TABLE emprestimos (
    id_emprestimo   INT AUTO_INCREMENT PRIMARY KEY,
    data_emprestimo DATE            NOT NULL,
    data_devolucao  DATE            DEFAULT NULL,
    estado          VARCHAR(20)     NOT NULL DEFAULT 'ativo',
    id_livro        INT             NOT NULL,
    id_utilizador   INT             NOT NULL,
    FOREIGN KEY (id_livro)      REFERENCES livro(id_livro),
    FOREIGN KEY (id_utilizador) REFERENCES utilizador(id_utilizador)
);

INSERT INTO utilizador (nome, idade, email, password, tipo_utilizador, data_registo, telefone)
VALUES ('admin', 18, 'adminbiblioteca@gmail.com', '123456789', 'funcionario', '2026-05-17', '5920986');