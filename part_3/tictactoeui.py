# -*- coding: utf-8 -*-
import math
import pygame
import sys

SIZE = WIDTH, HEIGHT = 400, 550
WHITE = pygame.Color("white")

class Game():
    START, WAIT, TURN, CONTINUE = 0, 1, 2, 3

    def __init__(self):
        self.status = self.START
        self.player = Block.AVAILABLE
        self.screen = pygame.display.set_mode(SIZE)
        # Main Page
        self.btn_start = MySprite("start.png", [50,225])
        self._draw_main()
        # Stuff
        self.board = [
            None,
            Block(1, [55,405]),
            Block(2, [155,405]),
            Block(3, [255,405]),
            Block(4, [55,305]),
            Block(5, [155,305]),
            Block(6, [255,305]),
            Block(7, [55,205]),
            Block(8, [155,205]),
            Block(9, [255,205]),
        ]
        self.btn_restart = MySprite("revanche.png", [75,100])
        self.btn_leave = MySprite("sair.png", [225,100])
        self.txt_win = MySprite("ganhou.png", [50,50])
        self.txt_draw = MySprite("empatou.png", [50,50])
        self.txt_lose = MySprite("perdeu.png", [50,50])
        self.txt_turn = MySprite("suavez.png", [50,50])
        self.txt_wait = MySprite("aguardando.png", [50,50])
        # Accept Input
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP: self._handle_click(event)
                elif event.type == pygame.USEREVENT: self._handle_userevent(event)
                elif event.type == pygame.QUIT: self.exit_safely()

    def _clean_board(self):
        # Draw black board
        self.screen.fill( (0,0,0) )

    def _draw_board(self):
        self._clean_board()
        # Draw lines
        pygame.draw.line(self.screen, WHITE, (50,300), (350,300), 9)  # Top line
        pygame.draw.line(self.screen, WHITE, (50,400), (350,400), 9)  # Bottom line
        pygame.draw.line(self.screen, WHITE, (150,200), (150,500), 9)  # Left line
        pygame.draw.line(self.screen, WHITE, (250,200), (250,500), 9)  # Right line
        # Draw blocks
        for block in self.get_blocks():
            self._draw_sprite(block)
        # Messages
        if self.may_move():
            self._draw_sprite(self.txt_turn)
        elif self.may_continue():
            pass
        else:
            self._draw_sprite(self.txt_wait)

        pygame.display.flip()

    def _draw_main(self):
        self._clean_board()
        self._draw_sprite(self.btn_start)
        pygame.display.flip()

    def _draw_result(self, winner):
        self._clean_board()
        if self.player == winner:
            self._draw_sprite(self.txt_win)
        elif self.player == 0:
            self._draw_sprite(self.txt_draw)
        else:
            self._draw_sprite(self.txt_lose)
        self._draw_sprite(self.btn_restart)
        self._draw_sprite(self.btn_leave)
        self._draw_board()

    def _draw_sprite(self, sprite):
        self.screen.blit(sprite.image, sprite.rect)

    def _handle_click(self, event):
        if event.button == 1:
            if self.may_start():
                print("COMEÇOU")
                # Começa o jogo
                self.set_status(self.WAIT)
                self._draw_board()
                self.subscribe()
            elif self.may_move():
                print("TENTOU JOGAR")
                # Jogadas
                for block in self.get_blocks():
                    if block.click_collided(event.pos) and block.update(self.player):
                        print("JOGOU")
                        self.set_status(self.WAIT)
                        self._draw_board()
                        self.check_winner(self.player)
            elif self.may_continue():
                print("GAME OVER")
                pass
        elif event.button == 3:
            print("DEBUG:")
            import pdb; pdb.set_trace()

    def _handle_userevent(self, event):
        if event.mode == "init":
            self.player = event.player
            if self.player == 1:
                self.set_status(self.TURN)
        elif event.mode == "sync":
            pass
        elif event.mode == "move":
            pass
        elif event.mode == "invalid":
            self.exit_safely()
        self._draw_board()

    def check_draw(self):
        for block in self.get_blocks():
            if block.status == 0:
                return False
        return True

    def check_winner(self, player):
        # Checks if player won the game
        if ((self.board[7].marked_by(player) and self.board[8].marked_by(player) and self.board[9].marked_by(player)) or  # across the top
            (self.board[4].marked_by(player) and self.board[5].marked_by(player) and self.board[6].marked_by(player)) or  # across the middle
            (self.board[1].marked_by(player) and self.board[2].marked_by(player) and self.board[3].marked_by(player)) or  # across the bottom
            (self.board[7].marked_by(player) and self.board[4].marked_by(player) and self.board[1].marked_by(player)) or  # down the left side
            (self.board[8].marked_by(player) and self.board[5].marked_by(player) and self.board[2].marked_by(player)) or  # down the middle
            (self.board[9].marked_by(player) and self.board[6].marked_by(player) and self.board[3].marked_by(player)) or  # down the right side
            (self.board[7].marked_by(player) and self.board[5].marked_by(player) and self.board[3].marked_by(player)) or  # diagonal
            (self.board[9].marked_by(player) and self.board[5].marked_by(player) and self.board[1].marked_by(player))  # diagonal
                ):
            self.set_status(self.CONTINUE)
            self._draw_result(player)
        elif (self.check_draw()):
            self.set_status(self.CONTINUE)
            self._draw_result(0)

    def exit_safely(self):
        sys.exit()

    def get_foe_num(self):
        return (self.player % 2) + 1

    def get_blocks(self):
        for block in self.board:
            if block is not None:
                yield block

    def may_continue(self):
        return self.status == self.CONTINUE

    def may_move(self):
        return self.status == self.TURN

    def may_start(self):
        return self.status == self.START

    def set_status(self, status):
        self.status = status

    def subscribe(self):
        print("UDP confiavel pro servidor: Quero jogar")
        event = pygame.event.Event(
            pygame.USEREVENT,
            {
                "mode": "init",
                "player": 1,
            }
        )
        pygame.event.post(event)


class MySprite(pygame.sprite.Sprite):
    def __init__(self, name, shift):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(name)
        self.rect = self.image.get_rect().move(shift)
    
    def click_collided(self, pos):
        x,y = pos
        return self.rect.collidepoint(x,y)


class Block(MySprite):
    AVAILABLE = 0
    PLAYER1 = 1
    PLAYER2 = 2

    def __init__(self, id_, shift):
        MySprite.__init__(self, "player0.png", shift)
        self.id = id_
        self.status = self.AVAILABLE

    def marked_by(self, player):
        return self.status == player

    def update(self, player):
        if self.status == self.AVAILABLE:
            self.status = player
            self.image = pygame.image.load("player{}.png".format(player))
            return True
        return False


if __name__ == "__main__":
    Game()
