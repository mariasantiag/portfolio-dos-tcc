DROP DATABASE IF EXISTS dbTcc;
CREATE DATABASE dbTcc;
USE dbTcc;

-- TABELA DE CURSOS
CREATE TABLE tbCurso (
    cod_curso INT AUTO_INCREMENT PRIMARY KEY,
    nome_curso VARCHAR(80) NOT NULL
);


-- REMOVA cod_orientador da tbTcc!
CREATE TABLE tbTcc (
    codigo INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(2000) NOT NULL,
    cod_curso INT,
    descricao VARCHAR(1200) NOT NULL,
    data VARCHAR(10),
    palavrachave1 VARCHAR(20),
    palavrachave2 VARCHAR(20),
    palavrachave3 VARCHAR(20),
    destaque VARCHAR(3),
    pdf_nome VARCHAR(255),
    FOREIGN KEY (cod_curso) REFERENCES tbCurso(cod_curso)
    
);

-- TABELA DE ORIENTADORES (ligada ao curso)
CREATE TABLE tbOrientador (
cod_orientador INT AUTO_INCREMENT PRIMARY KEY,
nome_orientador VARCHAR(80) NOT NULL,
cod_curso INT,
FOREIGN KEY (cod_curso) REFERENCES tbCurso(cod_curso)
);

-- NOVA TABELA PARA RELACIONAMENTO MUITOS-PARA-MUITOS
CREATE TABLE tbTcc_Orientador (
    cod_tcc INT,
    cod_orientador INT,
    PRIMARY KEY (cod_tcc, cod_orientador),
    FOREIGN KEY (cod_tcc) REFERENCES tbTcc(codigo),
    FOREIGN KEY (cod_orientador) REFERENCES tbOrientador(cod_orientador)
);

-- ... tbAdmin permanece igual



-- TABELA DE ADMINS
CREATE TABLE tbAdmin (
    login VARCHAR(80) NOT NULL,
    senha VARCHAR(100) NOT NULL,
    nome VARCHAR(80) NOT NULL,
    codigo INT PRIMARY KEY AUTO_INCREMENT
);

-- DADOS DE EXEMPLO