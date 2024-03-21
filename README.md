Movies - backend challenge
===

# Requisitos
## Docker
Este projeto esta Dockerizado portanto tendo o docker instalado não deve haver muita dificuldade em executar.

## Make
Também é feito o uso do Make como uma maneira de automatizar agnóstica à linguagem de programação.
Há arquivo na raiz chamado `Makefile` que comanda essas tarefas.


# Como rodar
## Passo 1 - construir imagem
```shell
make build-image
```

## Passo 2 - rodar a aplicação
```shell
make run-image
```

Também estão automatizadas os exemplos de uso da API
```shell
# para fazer a importação dos filmes
make import-movies  # essa endpoint é indempotente, não vai duplicar registros.
# consome o endpoint para retornar todos os piores produtores de filmes
make get_worst_producers 
```

## Passo 3 - rodar os testes
Os testes também podem ser rodados dentro de container. Este procedimento facilita o CI/CD pois a imagem encerra um ambiente com todas as dependências necessárias.

```shell
make run-tests-in-image
```

**Observação 1:** O ideal para produção seria uma imagem baseada em uma distribuição Alpine.

**Observação 2:** O projeto foi desenvolvido num Mac M1, que possui uma arquitetura arm64, portanto a imagem que eu construi e rodei localmente será diferente e incompatível com uma construída em uma ou para uma arquitetura x64.

**Observação 3:** O projeto foi desenvolvido num Mac M1, que possui uma arquitetura arm64, onde podem haver mudanças em bibliotecas que precisem de uma etapa de `build wheel`.

**Observação 4:** Podem haver algumas dependências não mapeadas no caso deste projeto rodar em ambiente Windows. Dependências que são comuns em ambientes Unix Like como Curl e Make não são comuns em Windows.