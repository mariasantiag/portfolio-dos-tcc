create database dbTcc;
use dbTcc;


create table tbOrientador (
	nome_orientador VARCHAR(80) not null,
    cod_curso INT,
    cod_orientador INT auto_increment primary key
);


create table tbCurso (
	nome_curso VARCHAR(80) not null,
    cod_curso INT auto_increment primary key,
    cod_orientador INT,
    FOREIGN KEY (cod_orientador) REFERENCES tbOrientador(cod_orientador)
);





create table tbTcc (
	titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(2000) NOT NULL,
    cod_orientador INT,
    descricao VARCHAR(1200) NOT NULL,
    data VARCHAR(8),
    palavrachave1 varchar (20),
    palavrachave2 varchar (20),
    palavrachave3 varchar (20),
    destaque varchar (3),
    pdf_nome VARCHAR(255),
    codigo INT auto_increment primary key,
    cod_curso int,
    FOREIGN KEY (cod_curso) REFERENCES tbCurso(cod_curso),
    FOREIGN KEY (cod_orientador) REFERENCES tbOrientador(cod_orientador)
);


create table tbAdmin (
	login VARCHAR(80) NOT NULL,
    senha VARCHAR(100) NOT NULL,
    nome VARCHAR(80) NOT NULL,
    codigo INT primary key auto_increment
);

SELECT 
    tcc.titulo,
    tcc.autor,
    tcc.descricao,
    tcc.data,
    tcc.palavrachave1,
    tcc.palavrachave2,
    tcc.palavrachave3,
    tcc.codigo AS tcc_codigo,
    orientador.nome_orientador ,
    curso.nome_curso
FROM 
    tbTcc tcc
INNER JOIN 
    tbOrientador orientador ON tcc.cod_orientador = orientador.cod_orientador
INNER JOIN 
    tbCurso curso ON tcc.cod_curso = curso.cod_curso;


SELECT 
    curso.nome_curso,
    orientador.nome_orientador
FROM 
    tbCurso curso
INNER JOIN 
    tbOrientador orientador ON curso.cod_orientador = orientador.cod_orientador;
    
    
