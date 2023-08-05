"""
Author: Heinrich Sporys
"""

import os
import pickle

import numpy as np
import pygame
import pygame.freetype

from nevolution_risk.constants.colors import black, dimgray, water_blue
from nevolution_risk.constants.view_settings import width, height, radius, line_thickness, font_multiplier


class Gui(object):
    def __init__(self, graph, env):
        """
        creates a gui to allow the game to be displayed, sets up most important things to allow the rendering
        :param graph: graph, which is more like a gamestate, to use for the gui
        """
        self.graph = graph
        self.env = env
        self.game_display = None
        self.font = None
        self.rendering = True
        self.default_font = None
        self.font_init = False
        self.troop = True

        filename_x = "pixel_matrix.pickle"
        dir_name = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(dir_name, '../../res', filename_x)

        file = open(path, "rb")
        self.picture_matrix = pickle.load(file)

        dir_name = os.path.dirname(os.path.realpath(__file__))
        self.sword = pygame.image.load(os.path.join(dir_name, '../../res', 'sword.png'))

        self.country_images = []

        for index in range(42):
            filename = str(index) + ".png"
            self.country_images.append(pygame.image.load(os.path.join(dir_name, '../../res/output', filename)))

            self.country_images[index].fill(self.graph.nodes[index].player.color, special_flags=pygame.BLEND_MIN)

        self.map = pygame.image.load(os.path.join(dir_name, '../../res/output', "blank.png"))

        filename_x = "relative_position_x.txt"
        dir_name = os.path.dirname(os.path.realpath(__file__))
        path_x = os.path.join(dir_name, '../../res', filename_x)

        filename_y = "relative_position_y.txt"
        dir_name = os.path.dirname(os.path.realpath(__file__))
        path_y = os.path.join(dir_name, '../../res', filename_y)

        file_x = open(path_x)
        file_y = open(path_y)

        x_lines = file_x.readlines()
        y_lines = file_y.readlines()

        file_x.close()
        file_y.close()

        self.x_positions = [0] * 42
        self.y_positions = [0] * 42

        for i in range(42):
            self.x_positions[i] = int(x_lines[i])
            self.y_positions[i] = int(y_lines[i])

        for index, country in enumerate(self.country_images):
            self.map.blit(country, (self.x_positions[index], self.y_positions[index]))

        self.grid = pygame.image.load(os.path.join(dir_name, '../../res/output', "grid.png"))
        self.map.blit(self.grid, (0, 0))

    def update_country(self, country):
        self.country_images[country].fill((255, 255, 255), special_flags=pygame.BLEND_MAX)
        self.country_images[country].fill(self.graph.nodes[country].player.color, special_flags=pygame.BLEND_MIN)
        self.map.blit(self.country_images[country], (self.x_positions[country], self.y_positions[country]))
        self.map.blit(self.grid, (0, 0))

    def render(self, mode="human"):
        """
        renders the current state of the game saved in the graph, also opens the gui window on the first call
        :param mode: string, render mode, default is 'human' which does nothing special, 'rgb_array' causes the function
        to return a numpy array of the guis rgb-data as uint8s
        :return: a numpy array of the current gui if mode is 'rgb_array', None otherwise
        """
        if self.game_display is None:
            self.init()

        self.game_display.fill(water_blue)
        self.game_display.blit(self.map, (0, 0))
        for node in self.graph.nodes:
            self.draw_node(node)

        if self.env.game_state == 0:
            self.draw_text("Phase 1: distribute", (width - 830, 640), 60)
        elif self.env.game_state == 1:
            self.draw_text("Phase 2: attack", (width - 830, 640), 60)
        else:
            self.draw_text("Phase 3: move", (width - 830, 640), 60)

        offset = 0
        self.env.gui.draw_text("cards", (30, height - 55), 40)
        for card in self.env.graph.players[0].cards:
            self.env.gui.draw_text(str(card.typ), (140 + offset, height - 55), 40)
            offset += 30
        self.env.gui.draw_text("troops: " + str(self.env.graph.players[0].troops), (30, height - 105), 40)

        if mode == 'rgb_array':
            raw_pxarray = pygame.PixelArray(self.game_display)
            pxarray = []
            for row in raw_pxarray:
                row_px = []
                for pix in row:
                    tup = self.game_display.unmap_rgb(pix)
                    rgb = [tup[0], tup[1], tup[2]]
                    row_px.append(rgb)
                pxarray.append(row_px)
            return np.array(pxarray).astype(np.uint8)

        return None

    def draw_gui_elements(self):
        if self.troop:
            pygame.draw.rect(self.game_display, (30, 200, 30), ((width - 150, 200), (150, 100)))
        else:
            pygame.draw.rect(self.game_display, (200, 30, 30), ((width - 150, 200), (150, 100)))
        pygame.draw.rect(self.game_display, (0, 0, 255), ((width - 150, 300), (150, 100)))

    def init(self):
        """
        initializes pygame, the gui's font and creates a window to render to
        :return: None
        """
        pygame.init()
        self.game_display = pygame.display.set_mode((width, height))
        pygame.freetype.init()
        self.font = pygame.freetype.SysFont("bahnschrift", radius * font_multiplier, bold=True)

    def set_cursor_arrow(self):
        """
        makes the cursor visible
        :return: None
        """
        pygame.mouse.set_visible(True)

    def set_cursor_sword(self):
        """
        makes the cursor invisible allowing to draw another image (sword) at the cursors position
        :return:
        """
        pygame.mouse.set_visible(False)

    def draw_text(self, text, pos, size):
        """
        draws a text at a specified position in a specified size in the 'bahnschrift' font
        :param text: string to draw
        :param pos: position to draw at, in pixes coordinates, from the top left corner
        :param size: text font size
        :return: None
        """
        if not self.font_init:
            self.default_font = pygame.freetype.SysFont("bahnschrift", size)
            self.font_init = True

        self.default_font.render_to(self.game_display, pos, text, size=size)

    def draw_sword(self, pos1, pos2):
        """
        draws a sword at a given point and a line from the sword to another given point
        :param pos1: lines start position in  pixes coordinates, from the top left corner
        :param pos2: lines end position, also the position of the sword's point, pixes coordinates, from the top left
        :return: None
        """
        # en garde!
        pygame.draw.line(self.game_display, black, pos1, pos2, line_thickness)
        self.game_display.blit(self.sword, pos2)

    def draw_node(self, node):
        """
        draws a node in the countries graph, this draws a circle in a players color with background and the troop count
        as text
        :param node: Node, node to draw
        :return: None
        """
        pos = [0, 0]
        pos[0] = node.x
        pos[1] = node.y
        length = np.sqrt(2) * radius
        pos[0] = pos[0] - (length / 2) * 1.14
        pos[1] = pos[1] - (length / 2) * 0.8
        position = (int(pos[0]), int(pos[1]))

        if node.troops < 10:
            self.font.render_to(self.game_display, position, "0" + str(node.troops))
        else:
            self.font.render_to(self.game_display, position, str(node.troops))
