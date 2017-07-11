# -*- coding: utf-8 -*-
import json
import pygame
import queue
import sys
import socket
import threading
from datetime import datetime, timedelta

SIZE = WIDTH, HEIGHT = 400, 550
WHITE = pygame.Color("white")

class Game():
    START, WAIT, TURN, CONTINUE = 0, 1, 2, 3

    def __init__(self):
        self.screen = pygame.display.set_mode(SIZE)
        # Sockets
        self.send_queue = queue.Queue()
        self.sender = Sender(self.send_queue)
        self.receiver = Receiver(self)
        self.sender.start()
        self.receiver.start()
        # Main Page
        self.set_main()
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
        self.sync = MySprite("sync.png", [10,10])
        self.last_sync = datetime.now()
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
        self._draw_sprite(self.sync)

        pygame.display.flip()

    def _draw_main(self):
        self._clean_board()
        self._draw_sprite(self.btn_start)
        pygame.display.flip()

    def _draw_result(self, winner):
        self._clean_board()
        self.winner = winner
        if winner == self.player:
            self._draw_sprite(self.txt_win)
        elif winner == 0:
            self._draw_sprite(self.txt_draw)
        else:
            self._draw_sprite(self.txt_lose)
        if self.restart:
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
                self.restart = True
                self.rematch = False
                self.set_status(self.WAIT)
                self.draw_board()
                self.receiver.resume()
            else:
                if self.sync.click_collided(event.pos): self.request_sync()
                if self.may_move():
                    print("TENTOU JOGAR")
                    # Jogadas
                    for block in self.get_blocks():
                        if block.click_collided(event.pos) and block.update(self.player):
                            print("JOGOU")
                            self.queue_put({
                                "mode": "move",
                                "block": block.id
                            })
                            self.set_status(self.WAIT)
                            self.check_winner(self.player)
                elif self.may_continue():
                    if self.btn_leave.click_collided(event.pos):
                        print("RECOMEÇOU")
                        self.queue_put({
                            "mode": "quit"
                        })
                        self.set_main()
                        self.receiver.pause()
                    if self.restart and self.btn_restart.click_collided(event.pos):
                        print("REVANCHE")
                        self.queue_put({
                            "mode": "rematch"
                        })
                        self.reinit()

        elif event.button == 3:
            print("DEBUG:")
            import pdb; pdb.set_trace()

    def _handle_userevent(self, event):
        # Unsafe
        if event.mode == "init":
            self.player = event.player
            self.foe = (self.player % 2) + 1
            self.foe_addr = tuple(event.addr)
            if self.player == 1:
                self.set_status(self.TURN)
            self.draw_board()
        elif event.mode == "move":
            self.board[event.block].update(self.foe)
            self.set_status(self.TURN)
            self.check_winner(self.foe)
        elif event.mode == "rematch":
            self.do_rematch(self.CONTINUE)
            if not self.rematch:
                self.draw_board()
        elif event.mode == "quit":
            if self.rematch:
                self.set_main()
            else:
                self.restart = False
                self.foe_addr = None
                self.finish(self.winner)
            self.receiver.pause()
        elif event.mode == "syn":
            foe_board_sum = sum(event.board)
            my_board_sum = sum([block.status for block in self.get_blocks()])
            if my_board_sum > foe_board_sum:
                # Meu jogo está avançado
                self.do_sync()
            elif foe_board_sum > my_board_sum:
                # Ele jogou e eu não recebi
                for block in self.get_blocks():
                    block.update(event.board[block.id - 1], True)
                self.set_status(self.TURN)
                self.check_winner(self.foe)
        elif event.mode == "synack":
            for block in self.get_blocks():
                block.update(event.board[block.id - 1], True)
            self.set_status(self.TURN)
            self.check_winner(self.foe)
        else:
            self.exit_safely()

    def check_draw(self):
        for block in self.get_blocks():
            if block.status == Block.AVAILABLE:
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
            self.finish(player)
        elif self.check_draw():
            self.finish(Block.AVAILABLE)
        else:
            self.draw_board()            

    def do_rematch(self, false_status):
        if self.rematch:
            self.set_status(self.foe)
            self.rematch = False
        else:
            self.set_status(false_status)
            self.rematch = True

    def do_sync(self):
        self.queue_put({
            "mode": "synack",
            "board": [block.status for block in self.get_blocks()]
        })

    def draw_board(self):
        self._clean_board()
        self._draw_board()

    def exit_safely(self):
        self.thread_stop()
        sys.exit()

    def finish(self, player):
        self.set_status(self.CONTINUE)
        self._draw_result(player)

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

    def post_event(self, dict_):
        event = pygame.event.Event(
            pygame.USEREVENT,
            dict_
        )
        pygame.event.post(event)

    def queue_put(self, obj):
        if self.foe_addr is not None:
            self.send_queue.put({
                "addr": self.foe_addr,
                "data": json.dumps(obj)
            })
        else:
            print("OPONENTE NAO ENCONTRADO")

    def reinit(self):
        for block in self.get_blocks():
            block.update(Block.AVAILABLE, True)
        temp = self.player
        self.player = self.foe
        self.foe = temp

        self.do_rematch(self.WAIT)

        self.draw_board()

    def request_sync(self):
        now = datetime.now()
        if self.last_sync + timedelta(seconds=30) < now:
            self.last_sync = now
            self.queue_put({
                "mode": "syn",
                "board": [block.status for block in self.get_blocks()]
            })

    def set_main(self):
        self.foe_addr = None
        self.set_status(self.START)
        self.player = Block.AVAILABLE
        self.foe = Block.AVAILABLE
        self.btn_start = MySprite("start.png", [50,225])
        self._draw_main()

        if hasattr(self, "board"):
            for block in self.get_blocks():
                block.update(Block.AVAILABLE, True)

    def set_status(self, status):
        self.status = status

    def thread_stop(self):
        self.receiver.stop()
        self.sender.stop()


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

    def update(self, player, force=False):
        if force:
            self.status = player
            self.image = pygame.image.load("player{}.png".format(player))
        elif self.status == self.AVAILABLE:
            self.status = player
            self.image = pygame.image.load("player{}.png".format(player))
            return True
        return False


class Sender(threading.Thread):
    def __init__(self, to_send):
        self.queue = to_send
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        threading.Thread.__init__(self)

    def stop(self):
        self.runninng = 0

    def run(self):
        self.runninng = 1
        while self.runninng:
            try: 
                obj = self.queue.get(True, 10)
                self.sock.sendto(obj["data"].encode(), obj["addr"])
            except queue.Empty:
                pass

        self.sock.close()


class Receiver(threading.Thread):
    def __init__(self, game):
        self.game = game
        self.state = threading.Condition()
        self.paused = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        threading.Thread.__init__(self)

    def stop(self):
        self.runninng = 0

    def run(self):
        self.runninng = 1       
        while self.runninng:
            with self.state:
                if self.paused:
                    print("PAUSOU")
                    self.state.wait()
                    print("VOLTOU")

            data, addr = self.sock.recvfrom(4096)
            print(data.decode())
            self.game.post_event(json.loads(data.decode()))

        self.sock.close()

    def _subscribe(self):
        self.sock.sendto("{}".encode(), ("localhost", 7777))

    def resume(self):
        with self.state:
            self.paused = False
            self._subscribe()
            self.state.notify()  # unblock self if waiting

    def pause(self):
        with self.state:
            self.paused = True  # make self block and wait


if __name__ == "__main__":
    Game()
