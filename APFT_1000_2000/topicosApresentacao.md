-- Primeiramente, definimos IDs como chaves primárias em todas as tabelas, garantindo que cada registo numa tabela fosse único, evitando duplicação de dados, por exemplo: AuthorID, ArticleID, etc.

-- Primeiramente, na tabela "Topic" além de definirmos o atributo "TopicID" como chave primária, definimos o atributo "Name" como sendo único, evitando duplicações de tópicos com o mesmo nome. De forma semelhante, definimos na tabela "Institution" o nome da instituição como único. 

-- Relativamente aos volumes de um determinado jornal, como este pode ter múltiplos volumes, definimos uma chave primária composta (JournalID, Volume) na tabela "JournalVolume" para garantir a unicidade de cada volume. Isso assegura que cada volume seja único dentro do contexto de cada jornal.


-------------
Author:
Dr. John Smith
http://www.johnsmithauthor.com
http://www.johnsmithauthor.com
University of Oxford

Institution:
Imperial College London
South Kensington Campus, London SW7 2AZ, United Kingdom

Article:
Advanced Machine Learning Techniques for Predictive Analytics in Healthcare
This study explores the application of advanced machine learning techniques.
10.1234/abcd.2024.56789
International Journal of Healthcare Data Science
15
102
118

Topic:
Machine Learning
Machine Learning is a subset of artificial intelligence that focuses on developing algorithms and statistical models that enable computers to perform tasks without explicit instructions

Journal:
Journal of Artificial Intelligence Research
http://www.jair.org
1076-9757
1943-5037
AI Access Foundation
-------------

1. Introdução (30 segundos)

Olá, nós somos o João e Pedro. Este trabalho consistiu no desenvolvimento de um sistema de gestão de artigos científicos. Para atingir esse objetivo, foi criada uma base de dados que armazena diversas entidades inter-relacionadas, tais como autores, instituições, artigos, tópicos e jornais, como podemos ver no Diagrama Entidade-Relacionamento apresentado. 

Um dos nossos principais objetivos foi utilizar dados reais para este trabalho. Para isso, recorremos à API Semantic Scholar.

O sistema foi projetado para ser utilizado através de um website, onde os utilizadores interagem com a base de dados por meio de formulários. Estes formulários permitem operações como listar, ordenar, atualizar e eliminar, entre outras, registos de diferentes entidades. 

Além disso, são fornecidas estatísticas ao utilizador, como, por exemplo, os tópicos mais populares por ano ou os autores mais produtivos numa determinada área de investigação.

2. (1 minuto)
Vamos agora ver o nosso esquema relacional (ER) e discutir as escolhas que fizemos para normalizar a base de dados e minimizar a duplicação de dados.

Primeiramente, na tabela "Article", evitámos a duplicação de dados não incluindo atributos como "PublicationDate" e "TopicName" diretamente. Em vez disso, criámos as tabelas "JournalVolume" e "Topic" para armazenar essas informações que são comuns a vários artigos. Utilizámos uma chave estrangeira composta (JournalID, Volume) para manter a dependência correta com "JournalVolume". Para garantir uma associação eficiente entre tópicos e artigos, críamos a tabela "Belongs_to".
Gostávamos de salientar que a informação comum a múltiplos volumes de um mesmo jornal é mantida na tabela "Journal".

Ainda relativamente à tabela "Article" para evitar incluir a informação de todos os artigos que citaram uma publicação, criámos a tabela "Cited_by" com uma chave primária composta (CitedArticleID, CitingArticleID).

Para evitar que um artigo tivesse uma lista de todos os seus autores, o que violaria a 1NF, criámos a tabela "Wrote_by". Utilizámos a mesma abordagem para as relações "Has_keywords", "Favorite_Journal", "Interested_in", "Favorite_Article" e "Read_by".

(Normalização ??)

3. Elementos Importantes (3 minuto e 30 segundos)

-- Basico SP e UDF
Agora vamos apresentar alguns dos elementos mais importantes do nosso sistema. Utilizamos Stored Procedures (SPs) para realizar várias operações. Vamos começar com um exemplo básico, onde usamos um SP para listar os autores por número de artigos publicados.

Este SP, OrderByArticlesCount, faz uso de uma UDF chamada ListAllAuthors(), que é mostrada do lado direito do slide. Esta UDF que retorna uma tabela com informações dos autores.
A utilização desta UDF tem que como vantagem evitar a duplicação de código, pois é utiizada em diferentes contextos em diferentes SPs, usamo-la para ordenar por nome de autor.

-- Query Complexa
Agora queriamos mostrar uma querie que consideramos ser mais complexa.

O exemplo ilustrado, é um SP que tem a finalidade de calcular os tópicos de investigação mais populares nos últimos anos.

A query conta o número de artigos publicados por ano de um determinado tópico.
Utilizamos a função RANK() para classificar os tópicos dentro de cada ano com base na contagem de publicações. Os tópicos são ordenados de forma decrescente, selecionando apenas os três tópicos mais populares para cada ano. Finalmente, os resultados são ordenados por ano de publicação e pelo número de publicações daquele tópico.

-- Triggers

Outro elemento importante utilizado no nosso sistema são os triggers. Usámos triggers para garantir que a base de dados mantivesse consistência sempre que ocorre uma modificação na base de dados, como inserções, eliminações e atualizações. Aqui estão dois exemplos de triggers que utilizamos para manter o contador de artigos atualizados na tabela de autores:

(Confirmar isto com POS)
Este trigger é acionado após uma inserção na tabela Wrote_by. Ele atualiza o campo ArticlesCount na tabela Author, contando o número de artigos associados ao autor recém-inserido.

Este trigger por sua vez é acionado após uma eliminação na tabela Wrote_by. Ele atualiza o campo ArticlesCount na tabela Author, contando o número de artigos associados ao autor que teve um artigo eliminando.

-- Indexes

Foram ainda criados índices para melhorar a performance das consultas. Para isso, criámos índices focados em atributos-chave como nomes, número de artigos e número de autores, como podemos ver nos exemplos apresentados.

Esses índices são especialmente úteis quando os utilizadores do website ordenam resultados com base na quantidade de artigos ou autores, proporcionando uma experiência de procura mais rápida e eficiente, como verificámos no Execution Plan do SQL Server (Imagem do ??).

-- Cursor
Utilizamos ainda outro elemento, que foi um cursor, para mostrar uma estatística das citações acumulativas por tópico. Esta estatística permite ao utilizador ver os tópicos mais citados e perceber a discrepância entre diferentes tópicos. O cursor foi utilizado dentro de um Stored Procedure (SP), como podemos ver no slide.

O cursor é utilizado para percorrer os resultados de uma query linha a linha, o que nos permite calcular uma soma acumulativa das citações por tópico. Este procedimento não seria tão simples de obter com uma query SQL padrão.

( ?? SE CALHAR ISTO JÁ É INFO A MAIS)
Este SP faz o seguinte:
1) Declara variáveis para armazenar o nome do tópico, a contagem de citações e a soma acumulativa das citações.

2) Cria uma tabela temporária #CitationsSummary para armazenar os resultados intermédios.

3) Declara um cursor para percorrer os tópicos e suas contagens de citações, ordenando pelos tópicos com mais citações.

4) Utiliza um loop para processar cada linha retornada pelo cursor, atualizando a soma acumulativa das citações e inserindo os dados na tabela temporária.

5) Fecha e desaloca o cursor, e retorna os resultados da tabela temporária antes de descartá-la.
)

Agora vamos proceder ao vídeo demonstrativo, onde mostraremos como o utilizador interage com a base de dados através de formulários.

Na seção dos Autores, podemos realizar diferentes operações. Podemos eliminar um autor. Os triggers que definimos serão responsáveis por atualizar os dados relacionados nas restantes tabelas automaticamente.

É possível ordenar por ordem alfabética ou por número de artigos publicados, como podemos ver ao (CLICAR NO BOTÃO CORRESPONDENTE). Neste caso, no topo temos o autor com mais publicações e podemos ver os detalhes deste autor clicando em "Ver Detalhes". Aqui, podemos visualizar a lista de artigos publicados por este autor, bem como outras informações úteis.


É possível criar um novo autor. Se a instituição não estiver na base de dados, o sistema exibirá uma mensagem de erro e não permitirá a inserção.
IEEE Transactions on Power Delivery
(VÍDEO :
Dr. John Smith
http://www.johnsmithauthor.com
0000-0002-1825-0097
University of Porto
NASA Ames Res. Center, Moffett Field, CA, USA
)

Podemos também filtrar pelo nome do autor, através da barra de pesquisa (procurar o autor inserido), e veremos os autores correspondentes. Podemos (clicar em "Ver Mais") e vemos os detalhes.

Passamos agora para a seção das Instituições. Podemos ordenar por nome ou pelo número de autores associados a cada instituição. As operações permitidas continuam as mesmas. Vamos pesquisar "Department of Electronic" e clicar em "Ver Mais" na primeira instituição listada.

Na seção de Artigos, podemos consultar quais foram os artigos com o maior número de autores envolvidos (CLICAR). (Vamos clicar em "AuthorCount" e em "Ver Mais" no primeiro artigo listado.) Podemos ver que informações úteis de um artigo como o Abstract e que foi escrito por 10 autores. Podemos ainda constatar que um artigo pode pertencer a mais do que um tópico.

Passando para os tópicos podemos fazer as mesmas operações básicas.  
Podemos editar um tópico e adicionar uma descrição por exemplo:

(
Art is not only a reflection of the artist's inner world but also a mirror to society, capturing the essence of humanity in its myriad forms. It is an essential part of the human experience, continually evolving and influencing every aspect of our lives.
)
Por exemplo, ao clicar no primeiro tópico podemos ver os artigos publicados. Podemos também ordenar por número de artigos publicados, ao (clicar em "Economia" e em "Ver Mais"), podemos ver que foram publicados 38 artigos na área de Economia. Podemos voltar a ordenar por nome e eliminar um tópico (Ordenar por Nome) e (Eliminar Art)

Em relação aos Jornais, eles podem ter mais de um volume, e em cada volume é publicado um conjunto de artigos. Vamos mostrar o jornal com o maior número de artigos publicados e a informação dos respetivos volumes. Como podemos ver, cada volume foi publicado numa data diferente e contém diferentes artigos.

Assim como nas outras seções, podemos criar um novo jornal. Vamos adicionar um jornal de Inteligencia Artificial por exemplo "Journal of Artificial Intelligence Research":

(Adicionar o Jornal de baixo no Forms: )
Journal of Artificial Intelligence Research
http://www.jair.org
1076-9757
1943-5037
AI Access Foundation

Podemos procurar na barra de pesquisas o Journal inserido e ver os detalhes (clicando em Ver mais.)

Em seguida vamos mostrar as estatísticas fornecidas ao utilizador, presentes na página principal, que resultam das queries que explicámos antes.

O primeiro gráfico mostra os autores mais produtivos numa determinada área de investigação, com os tópicos identificados na legenda e o número de artigos indicado nas barras.

O gráfico seguinte apresenta a soma cumulativa de citações por tópico. Utilizámos cursores para calcular esta estatística, conforme mencionado anteriormente. Esta estatística permite ao utilizador ver os tópicos mais citados e perceber a discrepância entre diferentes tópicos. Por exemplo, Economia tem claramente um maior número de artigos citados.

Por último, apresentamos os tópicos mais populares por ano. Os resultados são ordenados por ano de publicação e pelo número de publicações de cada tópico. Os utilizadores podem visualizar a evolução das áreas de maior interesse ao longo do tempo. Segundo os nossos dados, estes foram os tópicos mais populares em 2023, mas se recuarmos no tempo (mover o cursor até 30 anos atrás), observamos que os tópicos populares eram diferentes, por exemplo, em 2000.

Com este vídeo acabamos a apresentação do nosso sistema de gestão de artigos científicos. Esperamos que tenham gostado. 