create database dbTcc;
use dbTcc;


create table tbOrientador (
	nome VARCHAR(80) not null,
    cod_curso INT,
    cod_orientador INT auto_increment primary key
);


create table tbCurso (
	nome VARCHAR(80) not null,
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
    codigo INT auto_increment primary key,
    cod_curso int,
    FOREIGN KEY (cod_curso) REFERENCES tbCurso(cod_curso),
    FOREIGN KEY (cod_orientador) REFERENCES tbOrientador(cod_orientador)
);


create table tbAdmin (
	login VARCHAR(80) NOT NULL,
    senha INT NOT NULL,
    nome VARCHAR(80) NOT NULL,
    codigo INT primary key
);
