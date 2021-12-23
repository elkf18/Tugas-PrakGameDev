# mengimport library
import sys
import settings
from collections import deque
from typing import Deque
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task
from panda3d.core import Point2
from helpers import gen_label_text
from helpers import load_object
from snake import Snake


class World(ShowBase):
    def __init__(self):
        super().__init__()

        self.disable_mouse() #fungsi untuk menghidupkan mouse
        self._background = load_object( #mengeload background
            "background",
            pos=Point2(0, 0),
            scale=9000,
            depth=200,
            transparency=False
        )
        self._gameboard = load_object( #mengeload gameboard
            "background",
            pos=Point2(0, 0),
            scale=39.5,
            depth=100,
            transparency=False
        )
        # petunjuknya
        gen_label_text("ESC  : Quit", 0)
        gen_label_text("SPACE: Pause", 1)
        gen_label_text("R    : Restart", 2)
        gen_label_text("ELYA KUMALA FAUZIYAH/V3920020", 3)
        self._score = gen_label_text(
            "", 0, left=False #label untuk skor
        )

        self._bricks = deque()
        self._dot = load_object(
            "brick", pos=Point2(0, 0)
        )
         #mengatur untuk event klik nya
        self._restart()
        self.accept("escape", sys.exit)
        self.accept("enter", self.restart) #untuk restart
        self.accept("arrow_up", self._turn, [settings.POS_Y]) #menggunakan setting dengan nama class nya untuk mengatur pada posisi maksimalnya di POS_Y
        self.accept("arrow_down", self._turn, [settings.NEG_Y])  #menggunakan setting dengan nama class nya untuk mengatur pada posisi maksimalnya di NEG_Y
        self.accept("arrow_left", self._turn, [settings.NEG_X])  #menggunakan setting dengan nama class nya untuk mengatur pada posisi maksimalnya di NEG_X
        self.accept("arrow_right", self._turn, [settings.POS_X])  #menggunakan setting dengan nama class nya untuk mengatur pada posisi maksimalnya di POS_X
        self.accept("space", self._tooggle_pause) #untuk psudr
        self.accept("r", self._restart) #untuk restart

        self.period = settings.PERIOD
        self.pause = True

    #game loop
    def _game_loop(self, task):
        dt = task.time - task.last
        if not self._snake.alive: #jika snake nya mati
            return task.done #mengembalikan tugas yang harus berhenti
        if self.pause: #jika dipaus maka akan
            return task.cont  #mengembalikan tugas yang harus dipanggil lagi pada frame berikutnya
        elif dt >= self.period: #jika dt lebih dari sama dengan period nya
            task.last = task.time #inisialisasi variable
            self._snake.move_forward() #memanggil fungsi untuk maju
            self._snake.check_state()#memanggil fungsi  mengecek status
            self._update_snake()  # memanggil fungsi update snake
            self._update_dot()  # memanggil fungsi update dot
            self._update_score()  # memanggil fungsi update score
        return task.cont  # mengembalikan tugas yang harus dipanggil lagi pada frame berikutnya

    #untuk menggambar snake
    def _draw_snake(self): 
        for point in self._snake.body: #menggunakan perulangan for point di body nya snake
            brick = load_object("brick", pos=Point2(point.real, point.imag)) #load object
            self._bricks.append(brick)

    #untuk update snake nya, akan semakin panjang
    def _update_snake(self):
        if len(self._snake.body) > len(self._bricks): #jika panjang dari body nya snake melebihi panjangnya dari briks
            new_head = self._dot #membuat variable new_head
            self._make_dot() #memanggil fungsi untuk membuat dot
            self._bricks.appendleft(new_head)

        for i in range(len(self._snake.body)): #perulangan for untuk range dari body snake
            point = self._snake.body[i] #deklarasi point dengan array i darii body snake
            brick = self._bricks[i] #deklarasi brick dengan array i dari _bricks
            brick.setPos(point.real, settings.SPRITE_POS, point.imag) #mengeset pos nya

    #fungsi membuat dot
    def _make_dot(self):
        self._dot = load_object( #load objek
            "brick", pos=Point2(self._snake.dot.real, self._snake.dot.imag)
        )

    #fungsi untuk mengupdate dot
    def _update_dot(self):
        x, y = self._dot.getX(), self._dot.getZ() #x dan y disini akan memanggil dari getX() dAN getZ()
        if (x, y) != self._snake.dot: #jika x dan y tidak sama dengan snake dot
            self._dot.setPos( #mengeset pos nya
                self._snake.dot.real, settings.SPRITE_POS, self._snake.dot.imag)

    #fungsi untuk mengupdate score
    def _update_score(self):
        self._score.setText(
            "Score: %s" % self._snake.get_score()
        )

    #fungsi untuk mempause
    def _tooggle_pause(self):
        self.pause = not self.pause

    #fungsi untuk rrstart
    def _restart(self):
        self.pause = True
        for b in self._bricks: #perulangan for untuk b di bricks maka akan di jalankan fungsi remove_node()
            b.remove_node()
        self._snake = Snake( #untuk snake nya
            body=_make_default_body(), #untuk body
            vector=settings.POS_X, #untuk posisi
            dot=complex() #untuk dot
        )
        self._snake.gen_dot()
        self._bricks = deque()
        self._update_dot()
        self._draw_snake()
        taskMgr.remove("GameLoop") 
        self._game_task = taskMgr.add(self._game_loop, "GameLoop")
        self._game_task.last = 0

    def _turn(self, direction: complex):  #untuk arahnya
        if not self.pause:
            self._snake.turn(direction)


def _make_default_body(): #membuat setelah default body nya
    return [complex(-i, 1) for i in range(7, 10)]

#untuk menjalankan program
if __name__ == '__main__': 
    w = World()
    w.run()
