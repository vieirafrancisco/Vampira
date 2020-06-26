# Vampira

Um jogo feito em pygame com o tema de Vampira

## How to run?
**Windows:**

run virtualenv:
````powershell
    cd venv/Scripts/
    activate
````
run the game:
````powershell
    python run.py
````

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
    - [x] Codar algoritmo de movimentação (implementar dijkstra)
- [x] Adicionar sprite de paredes
    - [x] Algoritmo de colisão
- [x] Mudar mapas
    - [x] Criar porta para o próximo mapa (fase)
- [x] Contador de turnos
- [x] Criar classe para controlar os mapas e as entidades
- [ ] Criar uma classe para spritesheets, para poder acessar as tiles
- [ ] Criar um timer

### Animation:
- [x] Mudar o desenho dos quadrados verdes de movimentação do player para algo mais intuitivo
    - [x] Colocar pegadas brancas no lugar dos espaços verdes (uma ideia)
    - [x] Adicionar um desenho de caveira em blocos exatamente atrás dos mobs
- [x] Criar um range de visualização dos mobs (sinalizar com quadrados vermelhos com opacidade baixa)
- [ ] Criar animação para apontar para as escadas, para sinalizar o objetivo do jogador
- [ ] Criar animação do player e dos mobs quando estão parados

### Refactoring:
- [ ] Replace lists to pygame vectors
- [ ] Mudar o algoritmo de dijkstra para o A* pathfiding algorithm e ver como fica
- [ ] Refatorar a função loop da classe Game, porque para atualizar o player está atualizando todas as outras sprites
- [x] (**) Resolver bug de mudança de mapas
- [x] (**) Resolver colisão do player com os mobs e dos mobs para o player

(**) Importantes!

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