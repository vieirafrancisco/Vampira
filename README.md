# Vampira

Um jogo feito em pygame com o tema de Vampira

## ToDo Stuff:

### Setup:
- [x] Criar virtualenv
- [x] Intalar dependências
    - [x] python3
    - [x] pygame
- [x] Criar código básico do pygame
    - [x] Arquivo de configurações (settings)
    - [x] Criar janela com tamanho semelhante a de um celular
- [x] Upar para o github
- [x] Escrever sobre como o jogo vai funcionar

### Features:
- [x] Criar grid de tiles
- [x] Adicionar sprite de jogador
    - [x] Criar movimentação com click
    - [ ] Codar algoritmo de movimentação
- [x] Adicionar sprite de paredes
    - [ ] Algoritmo de colisão

## Sobre o jogo:

**Descrição:**  
É um jogo tilebased de turno para celular, cujo objetivo é atravessar um percurso com o personagem de uma extremidade para a outra.
O personagem principal é uma vampira em seu habitat natural, onde muitos mortais aparecem como forma de turismo. O objetivo da vampira é atravessar sua sala sem ser percebida, podendo matar guardas neste percurso.
Irão haver guardas protegendo os turistas, então tem que tomar cuidado para não ser vista.

**Caracteristicas:**
- É um jogo de turno, em que cada turno o jogador faz um movimento e os inimigos também fazem seu movimento
- O jogador terá uma quantidade limitada de passos (tiles) que pode se movimentar, podendo ser aumentada com algum powerup que ganhar no caminho
- Matar os turistas garantem powerups
- Só poderá matar os guardas quando não está sendo vista, então tem que atacar pelas costas do guarda
- As fases serão níveis, e cada fim de uma fase o jogador poderar optar por ir para a próxima fase ou voltar para o menu
- Powerups:
    - Aumentar a quantidade de passos
    - Ficar furtivo (se transformar em morcego ou ficar invisível) até se mover novamente ou por uma quantidade limitada de turnos
    - Especial (sempre vai ter). Só poderá usar a cada 30 min e ele durará por uma quantidade limitada de turnos. O especial consiste em ganhar invensibilidade, ou seja, o jogador pode ser visto pelos guardas sem morrer e matar eles em qualquer ângulo. OBS: Animação da vampira ganha olhos vermelhos