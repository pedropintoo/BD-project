# Scripts para Inicializar a Base de Dados

O nosso script de inserção de dados na base de dados está localizado em `src/tables/full_data/download.py`. Este script é responsável por transferir os dados reais da API Semantic Scholar para a nossa base de dados.

Para acessar os dados fornecidos pela API Semantic Scholar, é necessário obter uma chave de acesso (API key). Isso pode ser feito na seção "Request a Semantic Scholar API Key" disponível neste [link](https://www.semanticscholar.org/product/api). 

**Uma grande quantidade de dados já está atualmente inserida na base de dados.**

Para além da API key para executar este script devem ser instaladas as seguintes dependências:

```
pip install semanticscholar
```

## Executar o script
Dentro do diretório `src`:
```
python3 full_data/download.py
```

