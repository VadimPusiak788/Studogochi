import pygame
from game_object import GameObject
from abc import ABC, abstractmethod
from statusbar import *
from interface_draw import IDraw
import time


class Student(GameObject, IDraw):
    def __init__(self, x, y, width, height, name, image, surface):
        super().__init__(x, y, width, height)
        self._name = name
        self.image = image
        self.statistics = {'health': 100,
                           'fatigue': 100,
                           # Сделать много подпунтков в пункте "Grades"
                           # 'Grades': {'Матеша': 0,
                           # 		'ФП': 0},
                           'grades': 0,
                           'money': 1000,
                           'alcohol': 10,  # ТУТ БЫЛО 10 Алкоголь записывать в % (процент спирта в крови)
                           }
        self.__subscribers = {}
        self.font = pygame.font.Font('freesansbold.ttf', 25)
        self.surface = surface

    def subscribe(self, characteristic, subscriber, ):
        self.__subscribers[characteristic] = subscriber

    def update_grades(self, grade):
        '''В перспективе это будет отдельный от update_statistic метод
        который будет принимать название предмета и оценку'''
        self.statistics['grades'] += grade
        self.__subscribers['grades'].update_status(self.statistics['grades'])
        self.__subscribers['gameover'].update_status('grades', self.statistics['grades'])

    def update_statistic(self, characteristic, value):
        trigger = self.__subscribers['gameover'].big_value(characteristic, self.statistics[characteristic], value)
        if trigger:
            pass
        else:
            self.statistics[characteristic] += value
            self.__subscribers[characteristic].update_status(self.statistics[characteristic])
            self.__subscribers['gameover'].update_status(characteristic, self.statistics[characteristic])

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        print("You can't do this operation!")
        return 0

    def draw(self):
        surf = pygame.image.load(self.image)
        surf = pygame.transform.scale(surf, (self.width, self.height))
        rect = surf.get_rect(bottomright=(self.bounds.x, self.bounds.y))
        self.surface.blit(surf, rect)
        text = self.font.render(str(self._name), True, (255, 0, 0),
                                (255, 255, 255))
        self.surface.blit(text, (self.bounds.x - 130, self.bounds.y))
