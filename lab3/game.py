# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import random


class Cell:
    def __init__(self, state = 0):
        self.state = state #когда инициализируем, то состояние по умолчанию - мертвая клетка
    def is_alive(self):
        return self.state


class CellList:
    def __init__ (self, nrow = 6, ncol = 8):
        if not (str(nrow).isdigit()): #если наша строка не является числом
            self.n = [[Cell(int(i)) for i in line.split() if i in "01"] for line in open(nrow).readlines()]
            #создаем список, для каждой линии из открытого файла считываем строки и для каждой строки из файла создаем список
            #для каждого эл-та из каждой строки, если i это 0 или 1, добавляем клетку с состоянием, который передал этот символ
            self.nrow = len(self.n)  #количество строк равно количеству подсписков с списке
            self.ncol = len(self.n[0]) #по нулевому элементу смотрим клоличество столбцов
            self.count = self.nrow * self.ncol
            self.x = 0
            self.y = -1
        else:
            self.n = [] # список клеток, self используется для обращения к полям класса
            self.count = nrow * ncol
            for i in range(nrow):
                self.n.append([])
                for j in range(ncol):
                    self.n[i].append(Cell(random.randint(0, 1)))
                    # создаем двумерный список и рандомно наполняем его нуоями и единицами
            self.nrow = nrow
            self.ncol = ncol
            self.x = 0
            self.y = -1

    def draw(self):
        list = []
        for i in range(self.nrow):
            list.append([])
            for j in range(self.ncol):
                list[i].append(self.n[i][j].is_alive())
                #снова создаем двумерный массив и возвращаем текущее состояние игрового поля
        return list

    def get_neighbours(self, cell):
        q_list = []
        x = [-1, -1, -1, 0, 0, 1, 1, 1] #координаты соседей по строкам
        y = [-1, 0, 1, -1, 1, -1, 0, 1] #координаты соседей по столбцам
        for i in range(8):
            xxx = cell[0] + x[i]
            yyy = cell[1] + y[i]
            #координаты текущего соседа
            if xxx >= 0 and xxx < self.nrow and yyy >= 0 and yyy < self.ncol: #условия невыходимости за границы поля
                q_list.append(self.n[xxx][yyy].is_alive()) #ДОБАВЛЯЕМ НАШИХ СОСЕДЕЙ
        return q_list

    def update(self):
        a_list = [] #временный список
        for i in range(self.nrow):
            a_list.append([])
            for j in range(self.ncol):
                neighbours = self.get_neighbours([i, j]) #получение списка соседей
                k = 0 #счетчик наших живых соседей
                for m in neighbours:
                    if m == 1:
                        k += 1
                if self.n[i][j].is_alive() == 0:
                    if k == 3:
                        a_list[i].append(Cell(1))
                    else:
                        a_list[i].append(Cell())
                else:
                    if k == 2 or k == 3:
                        a_list[i].append(Cell(1))
                    else:
                        a_list[i].append(Cell())
        self.n = a_list

    def __iter__(self):
        return self #возвращаем самого себя следующего

    def __next__(self):
        if self.count == 0:
            self.count = self.nrow * self.ncol
            self.y = -1
            self.x = 0
            raise StopIteration
        if self.y + 1 == self.ncol: #когда ряд заканчивается нам нужно спуститься вниз и снова влево
            self.y = -1
            self.x += 1
        self.count -= 1
        self.y += 1
        return self.n[self.x][self.y] #возвращаем нашу текующую клеточку

    def __str__(self):
        list =[]
        for i in range(self.nrow):
            list.append([])
            for j in range(self.ncol):
                list[i].append(self.n[i][j].is_alive())
        return list.__str__()  ##обращаемся к методу класса лист, чтобы сделать строку

    def __repr__(self):
        return self.n #делает для внутреннего устройства питона для взаимодействия с другими классами


class GameOfLife:
    def __init__(self, width = 640, height = 480, cell_size = 10, speed = 10, filename = 'qwerty'):
        self.cl = 0
        if filename != 'qwerty': #не равен нашему шаблону, то этот аргумент задан по умолчанию
            self.cl = CellList(filename)
            self.width = cell_size * self.cl.ncol
            self.height = cell_size * self.cl.nrow
        else:
            self.width = width
            self.height = height
            self.cl = CellList(self.height // cell_size, self.width // cell_size) #заполняем поле клетками
        # Устанавливаем размер окна
        self.screen_size = self.width, self.height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)
        self.cell_size = cell_size
        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_cell_list(self, rects): #отображение списка клеток рэктс с закрашиванием их в соответсвенные цвета
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if rects[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('magenta'), (
                        j * self.cell_size + 1, i * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('pink'), (
                        j * self.cell_size + 1, i * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))
                    #размеры заливаемой области( координаты, ширина, выоста) +1 делаем, чтобы не залило границы

    def draw_grid(self):
        # http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                (0, y), (self.width, y))


    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_cell_list(self.cl.draw())
            pygame.display.flip()
            self.cl.update()
            clock.tick(self.speed)
        pygame.quit()

if __name__ == '__main__':
    game = GameOfLife(320, 240, 20, 10, 'grid.txt')
    game.run()