CREATE DATABASE biblioteca_db;

USE biblioteca_db;

CREATE TABLE livro (
    id_livro        INT AUTO_INCREMENT PRIMARY KEY,
    titulo          VARCHAR(100)    NOT NULL,
    autor           VARCHAR(100)    NOT NULL,
    editora         VARCHAR(100)    DEFAULT NULL,
    ano_publicacao  INT(4)          DEFAULT NULL,
    categoria       VARCHAR(50)     DEFAULT NULL,
    quantidade      INT(10)         NOT NULL DEFAULT 1,
    promocao        TINYINT(1)      DEFAULT 0,
    desconto        INT(3)          DEFAULT 0,
    preco           INT             DEFAULT 0
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

CREATE TABLE catalogo (
    id_catalogo     INT AUTO_INCREMENT PRIMARY KEY,
    nome            VARCHAR(50)     NOT NULL,
    descricao       VARCHAR(255)    DEFAULT NULL,
    imagem          VARCHAR(100)    DEFAULT NULL
);

CREATE TABLE emprestimos_pedidos (
    id_emprestimo       INT AUTO_INCREMENT PRIMARY KEY,
    id_livro            INT NOT NULL,
    nome_cliente        VARCHAR(100) NOT NULL,
    email_cliente       VARCHAR(100) NOT NULL,
    telefone_cliente    VARCHAR(20) DEFAULT NULL,
    data_pedido         DATE NOT NULL,
    data_devolucao      DATE DEFAULT NULL,
    FOREIGN KEY (id_livro) REFERENCES livro(id_livro)
);

CREATE TABLE compras (
    id_compra           INT AUTO_INCREMENT PRIMARY KEY,
    id_livro            INT NOT NULL,
    nome_cliente        VARCHAR(100) NOT NULL,
    email_cliente       VARCHAR(100) NOT NULL,
    telefone_cliente    VARCHAR(20) DEFAULT NULL,
    data_compra         DATE NOT NULL,
    FOREIGN KEY (id_livro) REFERENCES livro(id_livro)
);

CREATE TABLE perguntas (
    id_pergunta     INT AUTO_INCREMENT PRIMARY KEY,
    pergunta        VARCHAR(500)    NOT NULL,
    resposta        TEXT            NOT NULL
);

CREATE TABLE favoritos (
    id_favorito     INT AUTO_INCREMENT PRIMARY KEY,
    id_utilizador   INT NOT NULL,
    id_livro        INT NOT NULL,
    data_adicao     DATE DEFAULT NULL,
    FOREIGN KEY (id_utilizador) REFERENCES utilizador(id_utilizador),
    FOREIGN KEY (id_livro) REFERENCES livro(id_livro)
);

INSERT INTO utilizador (nome, idade, email, password, data_registo, telefone)
VALUES ('admin', 18, 'adminbiblioteca@gmail.com', '123456789', '2026-05-17', '5920986');

INSERT INTO catalogo (nome, descricao, imagem) VALUES
('comedia',  'Histórias leves e divertidas que vão fazer-te rir do início ao fim.', 'comedia.jpg'),
('drama',    'Narrativas intensas e emocionantes que exploram a vida e os seus desafios.', 'drama.jpg'),
('fantasia', 'Mundos mágicos e aventuras épicas além da realidade.', 'fantasia.webp'),
('ficcao',   'Histórias criativas que te levam a realidades imaginárias e surpreendentes.', 'ficcao.jpg'),
('romance',  'Histórias de amor, emoções e relações que tocam o coração.', 'romance.webp'),
('terror',   'Histórias assustadoras que vão pôr os teus nervos à prova.', 'terror.jpg'),
('thriller', 'Suspense e mistério que te mantêm preso até à última página.', 'thriller.webp'),
('aventura', 'Histórias cheias de ação, exploração e desafios emocionantes.', 'aventura.jpg'),
('misterio', 'Enigmas e segredos que te fazem pensar até ao último detalhe.', 'misterio.jpg');

INSERT INTO perguntas (pergunta, resposta) VALUES
('Como faço para emprestar um livro?', 'Para emprestar um livro, basta dirigir-se à biblioteca com o seu cartão de leitor e solicitar o livro ao funcionário.'),
('Qual é o prazo de devolução?', 'O prazo de devolução é de 15 dias a partir da data do empréstimo.'),
('Posso renovar o empréstimo?', 'Sim, pode renovar o empréstimo uma vez, desde que não haja reservas para o mesmo livro.');