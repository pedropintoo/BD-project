-- Introducao
Olá, nós somos o João e Pedro, vamos dar início à nossa apresentação. Este trabalho consistiu no desenvolvimento de um sistema de gestão de artigos científicos. Para atingir esse objetivo, foi criada uma base de dados que armazena diversas entidades inter-relacionadas, tais como autores, instituições, artigos, tópicos e jornais.

Um dos nossos principais objetivos foi utilizar dados reais para este trabalho. Para isso, recorremos à API Semantic Scholar.

O sistema foi projetado para ser utilizado através de um website, onde os utilizadores interagem com a base de dados por meio de formulários. Estes formulários permitem operações como listar, ordenar, atualizar e eliminar, entre outras, registos de diferentes entidades. 

Além disso, são fornecidas estatísticas ao utilizador, como, por exemplo, os tópicos mais populares por ano ou os autores mais produtivos numa determinada área de investigação.

-- DER
Para adaptar o nosso trabalho aos dados reais fornecidos pela API, fizemos as modificações no Diagrama Entidade-Relacionamento (DER), assinaladas a vermelho, relativamente à entrega anterior. Por exemplo:
- Na entidade "Journal" o atributo "Frequency" foi substituído pelo atributo "Url". 


Além disso, devido às especificações dos dados fornecidos pela API, alterámos a relação "belongs to" entre "Topic" e "Journal" para uma nova relação entre "Topic" e "Article".

-- ER
Pela mesma razão, o Esquema Relacional (ER) também sofreu as mesmas alterações.

Relativamente às escolhas que fizemos para normalizar a base de dados e minimizar a duplicação de dados, podemos olhar para a tabela "Article" onde optámos por não incluir atributos como "PublicationDate" e "TopicName" diretamente. Em vez disso, criámos as tabelas "JournalVolume" e "Topic" para armazenar essas informações que são comuns a vários artigos.

Ainda relativamente à tabela "Article" para evitar incluir a informação de todos os artigos que citaram uma publicação, criámos a tabela "Cited_by".

Utilizámos a mesma abordagem para as restantes relações.


-- Indexes

Foram ainda criados índices para melhorar a performance das consultas. Para isso, criámos índices focados em atributos-chave como nomes, número de artigos e número de autores, como podemos ver nos exemplos apresentados.

Esses índices são especialmente úteis quando os utilizadores do website ordenam resultados com base na quantidade de artigos ou autores, proporcionando uma experiência de procura mais rápida e eficiente, como verificámos no Execution Plan do SQL Server (Imagem do ??).


-- Estatísticas
Agora queriamos mostrar algumas queries que consideramos ser mais complexa.

Como mencionado, são fornecidas estatísticas ao utilizador.

Neste slide podemos observar os autores mais produtivos numa determinada área de investigação.
Para isso foi utilizado um SP que por sua vez faz uso de uma UDF.

No slide seguinte, apresentamos uma estatística diferente. Neste caso temos os tópicos mais populares por ano, tendo sido usado este SP e UDF.
