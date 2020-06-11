from src.game import Game

if __name__ == '__main__':
    g = Game()
    while True:
        g.new()
        g.execute()
        g.game_over_screen()