# play_search_movie
Ferramenta desenvolvida com Python, para buscar novos lançamentos de filmes em algumas regiões na plataforma [Google Play](https://play.google.com/store/movies).

## Descrição:
Esse projeto tem como finalidade TENTAR e FACILITAR a busca por novos filmes na Google Play,
e verificar quais idiomas de áudios e legendas estão disponíveis para o filme desejado, 
e em qual região o mesmo está disponível.

## Instalação:

0. Certifique-se de ter o Python 3 instalado antes de usar esse projeto.
1. Clone o projeto usando `git clone https://github.com/MateusTars/play_search_movie` ou baixe o código-fonte como um zip e descompacte-o em qualquer local.
2. Instale as bibliotecas exigidas pelo projeto usando `pip install -r requirements.txt`

## Uso:

Para usar este projeto, forneça um nome de um filme.

```
> python playsm.py "Dune"
Iniciando a busca pelo filme: Dune
...
```

## Saída:
[playsm - Filme: Dune](https://gist.github.com/MateusTars/bba75dbe3c4e5be352436fd588cd19d4)

## Observação:

Como está ferramenta é um PROJETO ANTIGO não existe garantias que sempre estará em funcionamento,
pelo simples motivo das buscas serem análisadas em páginas html utilizando regex.
