<h1 align="center">Vampira</h1>

<p align="center">
    Um jogo feito em pygame com o tema de Vampira
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/34426662/168539390-15a33a6f-cab5-496e-90b6-de3a59133785.png" />
</p>

<h2 align="center">Sobre o jogo</h2>

É um jogo tilebased de turno "para celular". O objetivo do jogo é atravessar um percurso com a personagem de uma extremidade para a outra do mapa.
A protagonista é uma vampira que vive normalmente sua vida sombria em seu castelo. Por ser um território misterioso e com muitas histórias intrigantes muitos humanos são tentados pela curiosidade de desvendar estes misterios que envolvem o lugar. Mas não sabem o que ou quem vive por lá.
O objetivo da vampira é atravessar sua sala sem ser percebida, podendo atacar visitantes indesejados no caminho.
Guardas irão proteger os turistas, então é preciso sempre ter cuidado para não ser vista!

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

## How to run?
Install dependencies:
````bash
poetry install
````

Run game:
````bash
poetry run python run.py
````

## TODO:

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
