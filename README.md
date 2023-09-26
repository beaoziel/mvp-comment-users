<h1><i>COMMENT!</i> - Users </h1>

![GitHub Org's stars](https://img.shields.io/github/stars/beaoziel?style=social) ![Badge](https://img.shields.io/badge/Pós%20Graduação-purple) ![Badge Status](https://img.shields.io/badge/STATUS-Finalizado-blue)
# Índice 
* [Índice](#índice)
* [Descrição do Projeto](#descrição-do-projeto)
* [Arquitetura escolhida](#arquitetura-escolhida)
* [Acesso ao projeto](#acesso-ao-projeto)
* [Tecnologias utilizadas](#tecnologias-utilizadas)
* [Funcionalidades](#funcionalidades)
* [Pessoas Desenvolvedoras do Projeto](#autores)

## 📃 Descrição do projeto
<p>
  Desenvolvido para anotar recados, ou deixar aquele espaço para lembretes o <i> COMMENT! </i> vem como um sistema pronto para ajudar - e personalizar do jeitinho que você gosta!
  Deixe o seu mural repleto de personalidade com uma seleção completa de Emojis e jogo de cores!
</p>

## 📜 Funcionalidades
- ``Faz a busca de todos os usuários cadastrados``
- ``Faz a busca de um usuário pelo nome``
- ``Faz a busca do ID do usuário, pelo nome``
- ``Faz a busca de um usuário pelo ID``
- ``Adiciona um novo usuário à base de dados``
- ``Faz a edição do usuário`` 

## 📐 Arquitetura escolhida
<p>
  Para garantir uma melhor experiência do usuário, foi decido separar em 4 componentes independentes:
</p>

![Desenho da solução](https://github.com/beaoziel/mvp-comment-front/assets/61751794/b0531533-7898-4cd4-9bec-9e59db59d3f5)

- `Front-end`: Para interação do usuário e visualização dos comentários, um front irá receber todas as informações, condumindo as 3 APIS
- `API Externa`: Evitando o trabalho de ter uma base única, consumimos de uma API que garante a variedade dos emojis, já separados em categorias
- `Comments`: Componente para gerenciar todos os comentários e armazená-los em um banco do próprio componente
- `Users`: Componente para gerenciar os usuários, também com seu prórpio banco.

Com o uso de containers, foi possível melhor gerenciar o desenvolvimento já que apresentam diversas vantagens como isolamento de aplicações, portabilidade, escalabilidade, atualizações e implatações contínuas, entre outros.

## 📁 Acesso ao projeto
<p>
  Para acessar, será necessário a inicialização dos componentes <i>Users</i> e <i>Comments</i>. Depois, baixe o código fonte do componente de front end e abra o html "index".
  Não é necessário iniciar o front-end, visto que o mesmo consome de outras APIs.
</p>

## 🖥️ Tecnologias Utilizadas
- ``Python 3.11.2``
- ``JavaScript``
- ``CSS``
- ``Vscode``

# 🙋‍♀️ Autores

| Beatriz Lima (https://github.com/beaoziel) 
