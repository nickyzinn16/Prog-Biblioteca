-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 29-Maio-2026 às 16:13
-- Versão do servidor: 10.4.32-MariaDB
-- versão do PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `biblioteca_db`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `catalogo`
--

CREATE TABLE `catalogo` (
  `id_catalogo` int(11) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `descricao` varchar(255) DEFAULT NULL,
  `imagem` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `catalogo`
--

INSERT INTO `catalogo` (`id_catalogo`, `nome`, `descricao`, `imagem`) VALUES
(1, 'comedia', 'Histórias leves e divertidas que vão fazer-te rir do início ao fim.', 'Catalogo - Comedia.png'),
(2, 'drama', 'Narrativas intensas e emocionantes que exploram a vida e os seus desafios.', 'Catalogo - Drama.png'),
(3, 'fantasia', 'Mundos mágicos e aventuras épicas além da realidade.', 'Catalogo - Fantasia.png'),
(4, 'ficcao', 'Histórias criativas que te levam a realidades imaginárias e surpreendentes.', 'Catalogo - Ficcao.png'),
(5, 'romance', 'Histórias de amor, emoções e relações que tocam o coração.', 'Catalogo - Romance.png'),
(6, 'terror', 'Histórias assustadoras que vão pôr os teus nervos à prova.', 'Catalogo - Terror.png'),
(7, 'thriller', 'Suspense e mistério que te mantêm preso até à última página.', 'Catalogo - Thriller.png'),
(8, 'aventura', 'Histórias cheias de ação, exploração e desafios emocionantes.', 'Catalogo - Aventura.png'),
(10, 'misterio', 'Enigmas e segredos que te fazem pensar até ao último detalhe.', 'Catalogo - Misterio.png');

-- --------------------------------------------------------

--
-- Estrutura da tabela `compras`
--

CREATE TABLE `compras` (
  `id_compra` int(11) NOT NULL,
  `id_livro` int(11) NOT NULL,
  `nome_cliente` varchar(100) NOT NULL,
  `email_cliente` varchar(100) NOT NULL,
  `telefone_cliente` varchar(20) DEFAULT NULL,
  `data_compra` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `compras`
--

INSERT INTO `compras` (`id_compra`, `id_livro`, `nome_cliente`, `email_cliente`, `telefone_cliente`, `data_compra`) VALUES
(2, 15, 'Ricardo David', 'rickydavidbans27@gmail.com', '5920986', '2026-05-29');

-- --------------------------------------------------------

--
-- Estrutura da tabela `emprestimos`
--

CREATE TABLE `emprestimos` (
  `id_emprestimo` int(11) NOT NULL,
  `data_emprestimo` date NOT NULL,
  `data_devolucao` date DEFAULT NULL,
  `estado` varchar(20) NOT NULL DEFAULT 'ativo',
  `id_livro` int(11) NOT NULL,
  `id_utilizador` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `emprestimos_pedidos`
--

CREATE TABLE `emprestimos_pedidos` (
  `id_emprestimo` int(11) NOT NULL,
  `id_livro` int(11) NOT NULL,
  `nome_cliente` varchar(100) NOT NULL,
  `email_cliente` varchar(100) NOT NULL,
  `telefone_cliente` varchar(20) DEFAULT NULL,
  `data_pedido` date NOT NULL,
  `data_devolucao` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `emprestimos_pedidos`
--

INSERT INTO `emprestimos_pedidos` (`id_emprestimo`, `id_livro`, `nome_cliente`, `email_cliente`, `telefone_cliente`, `data_pedido`, `data_devolucao`) VALUES
(4, 15, 'Ricardo David', 'rickydavidbans27@gmail.com', '5920986', '2026-05-29', '2026-05-28');

-- --------------------------------------------------------

--
-- Estrutura da tabela `favoritos`
--

CREATE TABLE `favoritos` (
  `id_favorito` int(11) NOT NULL,
  `id_utilizador` int(11) NOT NULL,
  `id_livro` int(11) NOT NULL,
  `data_adicao` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `livro`
--

CREATE TABLE `livro` (
  `id_livro` int(11) NOT NULL,
  `titulo` varchar(100) NOT NULL,
  `autor` varchar(100) NOT NULL,
  `editora` varchar(100) DEFAULT NULL,
  `ano_publicacao` int(4) DEFAULT NULL,
  `categoria` varchar(50) DEFAULT NULL,
  `quantidade` int(10) NOT NULL DEFAULT 1,
  `promocao` tinyint(1) DEFAULT 0,
  `desconto` int(3) DEFAULT 0,
  `preco` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `livro`
--

INSERT INTO `livro` (`id_livro`, `titulo`, `autor`, `editora`, `ano_publicacao`, `categoria`, `quantidade`, `promocao`, `desconto`, `preco`) VALUES
(15, 'Venha Rir', 'Ricardo Santos', 'CV edita', 2024, 'comedia', 10, 1, 50, 1000),
(16, 'O palhaço da cidade', 'Kvicha Kvaratselia', 'Edition Georgia', 2026, 'comedia', 4, 0, 0, 6000);

-- --------------------------------------------------------

--
-- Estrutura da tabela `perguntas`
--

CREATE TABLE `perguntas` (
  `id_pergunta` int(11) NOT NULL,
  `pergunta` varchar(500) NOT NULL,
  `resposta` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `perguntas`
--

INSERT INTO `perguntas` (`id_pergunta`, `pergunta`, `resposta`) VALUES
(5, 'Posso fazer empréstimos de um livro?', 'Sim, podes fazer emprestimo de qualquer livro disponivel nos catalogos.');

-- --------------------------------------------------------

--
-- Estrutura da tabela `utilizador`
--

CREATE TABLE `utilizador` (
  `id_utilizador` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `idade` int(10) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `tipo_utilizador` varchar(20) NOT NULL DEFAULT 'cliente',
  `data_registo` date DEFAULT NULL,
  `telefone` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `utilizador`
--

INSERT INTO `utilizador` (`id_utilizador`, `nome`, `idade`, `email`, `password`, `tipo_utilizador`, `data_registo`, `telefone`) VALUES
(1, 'admin', 18, 'adminbiblioteca@gmail.com', '123456789', 'funcionario', '2026-05-17', '5920986');

--
-- Índices para tabelas despejadas
--

--
-- Índices para tabela `catalogo`
--
ALTER TABLE `catalogo`
  ADD PRIMARY KEY (`id_catalogo`);

--
-- Índices para tabela `compras`
--
ALTER TABLE `compras`
  ADD PRIMARY KEY (`id_compra`),
  ADD KEY `id_livro` (`id_livro`);

--
-- Índices para tabela `emprestimos`
--
ALTER TABLE `emprestimos`
  ADD PRIMARY KEY (`id_emprestimo`),
  ADD KEY `id_livro` (`id_livro`),
  ADD KEY `id_utilizador` (`id_utilizador`);

--
-- Índices para tabela `emprestimos_pedidos`
--
ALTER TABLE `emprestimos_pedidos`
  ADD PRIMARY KEY (`id_emprestimo`),
  ADD KEY `id_livro` (`id_livro`);

--
-- Índices para tabela `favoritos`
--
ALTER TABLE `favoritos`
  ADD PRIMARY KEY (`id_favorito`),
  ADD KEY `id_utilizador` (`id_utilizador`),
  ADD KEY `id_livro` (`id_livro`);

--
-- Índices para tabela `livro`
--
ALTER TABLE `livro`
  ADD PRIMARY KEY (`id_livro`);

--
-- Índices para tabela `perguntas`
--
ALTER TABLE `perguntas`
  ADD PRIMARY KEY (`id_pergunta`);

--
-- Índices para tabela `utilizador`
--
ALTER TABLE `utilizador`
  ADD PRIMARY KEY (`id_utilizador`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `telefone` (`telefone`);

--
-- AUTO_INCREMENT de tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `catalogo`
--
ALTER TABLE `catalogo`
  MODIFY `id_catalogo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de tabela `compras`
--
ALTER TABLE `compras`
  MODIFY `id_compra` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `emprestimos`
--
ALTER TABLE `emprestimos`
  MODIFY `id_emprestimo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `emprestimos_pedidos`
--
ALTER TABLE `emprestimos_pedidos`
  MODIFY `id_emprestimo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de tabela `favoritos`
--
ALTER TABLE `favoritos`
  MODIFY `id_favorito` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `livro`
--
ALTER TABLE `livro`
  MODIFY `id_livro` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de tabela `perguntas`
--
ALTER TABLE `perguntas`
  MODIFY `id_pergunta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de tabela `utilizador`
--
ALTER TABLE `utilizador`
  MODIFY `id_utilizador` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restrições para despejos de tabelas
--

--
-- Limitadores para a tabela `compras`
--
ALTER TABLE `compras`
  ADD CONSTRAINT `compras_ibfk_1` FOREIGN KEY (`id_livro`) REFERENCES `livro` (`id_livro`);

--
-- Limitadores para a tabela `emprestimos`
--
ALTER TABLE `emprestimos`
  ADD CONSTRAINT `emprestimos_ibfk_1` FOREIGN KEY (`id_livro`) REFERENCES `livro` (`id_livro`),
  ADD CONSTRAINT `emprestimos_ibfk_2` FOREIGN KEY (`id_utilizador`) REFERENCES `utilizador` (`id_utilizador`);

--
-- Limitadores para a tabela `emprestimos_pedidos`
--
ALTER TABLE `emprestimos_pedidos`
  ADD CONSTRAINT `emprestimos_pedidos_ibfk_1` FOREIGN KEY (`id_livro`) REFERENCES `livro` (`id_livro`);

--
-- Limitadores para a tabela `favoritos`
--
ALTER TABLE `favoritos`
  ADD CONSTRAINT `favoritos_ibfk_1` FOREIGN KEY (`id_utilizador`) REFERENCES `utilizador` (`id_utilizador`),
  ADD CONSTRAINT `favoritos_ibfk_2` FOREIGN KEY (`id_livro`) REFERENCES `livro` (`id_livro`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
