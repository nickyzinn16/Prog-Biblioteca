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
    data_registo    DATE            DEFAULT NULL,
    telefone        VARCHAR(20)     DEFAULT NULL UNIQUE
);

INSERT INTO utilizador (nome, idade, email, password, data_registo, telefone)
VALUES ('admin', 18, 'adminbiblioteca@gmail.com', '123456789', '2026-05-17', '5920986');