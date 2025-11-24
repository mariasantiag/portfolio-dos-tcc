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
    titulo VARCHAR(2000) NOT NULL,
    autor VARCHAR(2000) NOT NULL,
    cod_curso INT,
    descricao VARCHAR(6000) NOT NULL,
    data VARCHAR(10),
    palavrachave1 VARCHAR(200),
    palavrachave2 VARCHAR(200),
    palavrachave3 VARCHAR(200),
	palavrachave4 VARCHAR(200),
	palavrachave5 VARCHAR(200),
    destaque VARCHAR(3),
    pdf_nome VARCHAR(255),
    FOREIGN KEY (cod_curso) REFERENCES tbCurso(cod_curso)
    
);

-- TABELA DE ORIENTADORES (ligada ao curso)
CREATE TABLE tbOrientador (
cod_orientador INT AUTO_INCREMENT PRIMARY KEY,
nome_orientador VARCHAR(200) NOT NULL,
cod_curso INT,
FOREIGN KEY (cod_curso) REFERENCES tbCurso(cod_curso)
);
ALTER TABLE tbOrientador ADD COLUMN contratado TINYINT(1) DEFAULT 1;


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
    codigo INT primary key AUTO_INCREMENT
);


CREATE TABLE tbHistorico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_nome VARCHAR(100) NOT NULL,
    acao VARCHAR(100) NOT NULL,
    detalhes VARCHAR(255)
);



INSERT INTO tbCurso (nome_curso) VALUES
('Desenvolvimento de Sistemas'),
('Logística'),
('Administração'),
('Enfermagem'),
('Marketing');


INSERT INTO tbOrientador (nome_orientador, cod_curso) VALUES
('Alex', 1),
('Ivo', 1);


INSERT INTO tbOrientador (nome_orientador, cod_curso) VALUES
('Lucas', 2),
('Mariana', 2);


INSERT INTO tbOrientador (nome_orientador, cod_curso) VALUES
('Eduardo', 3),
('Renata', 3);

INSERT INTO tbOrientador (nome_orientador, cod_curso) VALUES
('Carla', 4),
('Roberto', 4);


INSERT INTO tbOrientador (nome_orientador, cod_curso) VALUES
('Thiago', 5),
('Fernanda', 5);

INSERT INTO tbCurso (nome_curso) VALUES
('Ciência de Dados'),
('Engenharia de Software'),
('Redes de Computadores');

INSERT INTO tbOrientador (nome_orientador, cod_curso) VALUES
('Bruno', 6),
('Camila', 6),
('Sérgio', 6);

INSERT INTO tbOrientador (nome_orientador, cod_curso) VALUES
('Patrícia', 7),
('Daniel', 7),
('Gustavo', 7),
('Helena', 7);

INSERT INTO tbOrientador (nome_orientador, cod_curso) VALUES
('Rafael', 8),
('Juliana', 8),
('Marcos', 8);


INSERT INTO tbTcc (
    titulo, autor, cod_curso, descricao, data,
    palavrachave1, palavrachave2, palavrachave3, palavrachave4, palavrachave5,
    destaque, pdf_nome
) VALUES (
    'Cantina Virtual',
    'Gabriel Carlos De Almeida, Guilherme Lopes Lourenço, Kauan Oliveira Da Silva, Kelvyn Neris De Sena Silva, Matheus Souza de Mattos, Vitor Hugo De Melo',
    1,
    'O presente trabalho teve como objetivo o desenvolvimento do sistema Cantina Virtual, uma plataforma voltada para a otimização do processo de pedidos na cantina escolar.',
    '2024-12-10',
    'Sistema',
    'Cantina',
    'Otimização',
    'Funcionalidade',
    'Gestão',
    'nao',
    'CantinaVirtual.pdf'
);

INSERT INTO tbTcc_Orientador (cod_tcc, cod_orientador) VALUES (1, 1);
INSERT INTO tbTcc_Orientador (cod_tcc, cod_orientador) VALUES (1, 2);


INSERT INTO tbTcc (
    titulo, autor, cod_curso, descricao, data,
    palavrachave1, palavrachave2, palavrachave3, palavrachave4,
    destaque, pdf_nome
) VALUES (
    'Easy Request',
    'Ana Beatriz Camassuti Franciscatto Da Silva, Bianca Simonato Scupin, Gabriel Chagas Fernandes De Moraes, Guilherme Mitsuyuki, Julia De Barros Ribeiro',
    1,
    'O EASY REQUEST promete contribuir para a melhoria do ambiente escolar, fortalecendo a organização e a gestão de serviços de manutenção.',
    '2024-12-10',
    'Manutenção',
    'Organização',
    'Sistema',
    'Eficiência',
    'sim',
    'EasyRequest.pdf'
);

INSERT INTO tbTcc_Orientador (cod_tcc, cod_orientador) VALUES (2, 1);
INSERT INTO tbTcc_Orientador (cod_tcc, cod_orientador) VALUES (2, 2);

INSERT INTO tbTcc (
    titulo, autor, cod_curso, descricao, data,
    palavrachave1, palavrachave2, palavrachave3, palavrachave4, palavrachave5,
    destaque, pdf_nome
) VALUES (
    'Jardim dos Livros',
    'Allicia Tondato Morete, Giovana Mazzone Varussa, Leticia Gabriely Moraes, Yasmin de Moura Morgado Silva',
    1,
    'Este trabalho apresenta o desenvolvimento de uma plataforma intuitiva para o gerenciamento de livros em bibliotecas, integrando funcionalidades como cadastro, busca, reserva e monitoramento de exemplares.',
    '2024-12-12',
    'Gerenciamento de livros',
    'Automatização',
    'Reservas',
    'Banco de dados',
    'Plataforma web',
    'sim',
    'JardimdosLivros.pdf'
);

INSERT INTO tbTcc_Orientador (cod_tcc, cod_orientador) VALUES (3, 1);
INSERT INTO tbTcc_Orientador (cod_tcc, cod_orientador) VALUES (3, 2);



INSERT INTO tbTcc (
    titulo, autor, cod_curso, descricao, data,
    palavrachave1, palavrachave2, palavrachave3, 
    destaque, pdf_nome
) VALUES (
    'MoveBR',
    'André Turquiai Bido, Caio Hiroshi Ferreira, Jessica Pichinin da Costa, Leticia Rodrigues Lemes, Vinicius Amâncio da Silva',
    1,
    'O sistema proposto é uma solução integrada e automatizada para gestão do transporte escolar, projetada para atender às principais demandas dos motoristas de vans escolares.',
    '2024-12-09',
    'Escolar',
    'Van',
    'Transporte',
    'sim',
    'MoveBR.pdf'
);

INSERT INTO tbTcc_Orientador (cod_tcc, cod_orientador) VALUES (4, 1);
INSERT INTO tbTcc_Orientador (cod_tcc, cod_orientador) VALUES (4, 2);

INSERT INTO tbTcc (
    titulo, autor, cod_curso, descricao, data,
    palavrachave1, palavrachave2, palavrachave3, palavrachave4, palavrachave5,
    destaque, pdf_nome
) VALUES (
    'LogClass',
    'Ana Julia Firmiano Da Silva, Ana Livia Rosa Couto, Isabelle Eloise Rugno Ferreira, Jheniffer Rayane de Andrade, Maria Cecília Zaccaro Thomé',
    1,
    'O processo logístico é um conjunto de atividades essenciais que envolve a movimentação, armazenamento e gestão de materiais, desde a aquisição de matérias-primas até a entrega final dos produtos ao consumidor.',
    '2024-12-14',
    'Logística',
    'Sistema',
    'Otimização',
    'Aprendizagem',
    'Simulação',
    'nao',
    'LogClass.pdf'
);

INSERT INTO tbTcc_Orientador (cod_tcc, cod_orientador) VALUES (5, 1);
INSERT INTO tbTcc_Orientador (cod_tcc, cod_orientador) VALUES (5, 2);

INSERT INTO tbTcc (
    titulo, autor, cod_curso, descricao, data,
    palavrachave1, palavrachave2, palavrachave3,
    destaque, pdf_nome
) VALUES (
    'Remover',
    'Teste para Remover',
    2,
    'Remover',
    '2024-12-08',
    'Remover',
    'Excluir',
    'Apagar',
    'nao',
    'Invent+.pdf'
);

INSERT INTO tbTcc_Orientador (cod_tcc, cod_orientador) VALUES (6, 3);
INSERT INTO tbTcc_Orientador (cod_tcc, cod_orientador) VALUES (6, 4);

INSERT INTO tbTcc (
    titulo, autor, cod_curso, descricao, data,
    palavrachave1, palavrachave2, palavrachave3,
    destaque, pdf_nome
) VALUES (
    'Exemplo',
    'Teste para Exemplo',
    2,
    'Exemplo',
    '2024-12-08',
    'Exemplar',
    'Teste',
    'Exemplo',
    'nao',
    'Invent+.pdf'
);

INSERT INTO tbTcc_Orientador (cod_tcc, cod_orientador) VALUES (7, 3);








