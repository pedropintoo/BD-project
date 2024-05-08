# import json

# # Simulando o buffer com uma linha como exemplo
# buffer = [
#     '{"s2fieldsofstudy":[{"category":"Geography","source":"s2-fos-model"},{"category":"Computer Science","source":"s2-fos-model"},{"category":"Computer Science","source":"external"}]}'
# ]

# for line in buffer:
#     # Carregar cada linha como um objeto JSON
#     article_data = json.loads(line)
    
#     # Inicializa a lista para armazenar os nomes dos tópicos
#     topics_names = []
    
#     # Percorrer cada item na lista 's2fieldsofstudy'
#     for item in article_data["s2fieldsofstudy"]:
#         # Adicionar o valor da categoria à lista de tópicos
#         if item["category"] not in topics_names:  # Evitar duplicatas
#             topics_names.append(item["category"])

#     print(topics_names)  # Imprimir a lista de tópicos/categorias


import json

# Simulando o buffer com uma linha como exemplo
buffer = [
    '{"journal":{"name":"Differential Equations and Dynamical Systems","pages":" \\n 215-234 \n","volume":null}}'
]

for line in buffer:
    cleaned_line = line.replace('\n', '').replace('\\n', '').strip()

    # Carregar cada linha como um objeto JSON
    article_data = json.loads(cleaned_line)
    
    # Extrair informações do campo 'journal'
    journal_info = article_data["journal"]
    
    StartPage = EndPage = 0

    # Extrair as páginas e volume
    pages = journal_info["pages"]
    volume = journal_info["volume"]
    
    if pages and isinstance(pages, str) and '-' in pages:
        # Limpar espaços em branco e quebras de linha
        pages = pages.strip()
        
        # Verificar se o formato é 'Number1-Number2' após a limpeza
        if pages.count('-') == 1 and all(part.isdigit() for part in pages.split('-')):
            StartPage, EndPage = map(int, pages.split('-'))
    
    if volume and isinstance(volume, str) and volume.isdigit():
        volume = int(volume)
    else:
        volume = 0

    print("Start Page:", StartPage)
    print("End Page:", EndPage)
    print("Volume:", volume)
