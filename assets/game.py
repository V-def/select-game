# -*- coding: utf-8 -*-

"""
Main game program files
Used only during a game
"""

import pygame
import assets.consts as c
from assets.initial_layout import InitialLayout
import pickle
import os


class Game:
    """
    Class used to create games objects
    """

    def __init__(self, board, time, textures):
        """
        needed parameter
        board : object from Board
        textures : object from Textures
        time : object from Time
        """

        # Global

        self.process_string = "choose insect"

        self.turn = "white"
        self.last_turn = "black"

        self.ended = False

        # Board

        self.tile_pos = None
        self.tile_insect = None
        self.moving_insect = None

        self.board = board
        self.time = time
        self.textures = textures

        self.setback = None

        self.last_move = []

        self.log = None, None

        self.changed_turn = True

        self.turn_number = 0
        self.color_number = 0

        self.board_saves = []

        self.to_draw_board = {'last move': [], 'ways': [], 'setback': []}

        self.click = False
        self.drag = False
        self.display_drag = False
        self.origin_drag = None

        self.update_board_bol = False
        self.update_display_bol = False
        self.update_insects_bol = False

        self.update_process = False
        self.caption = None

        self.static_board = None
        self.insect_board = None

        # Clock

        self.clock = True  # allow clock

        if self.clock:
            # list that stores clock data in the form [white, black]

            # total time used by the player each round
            self.player_stopwatch = [0, 0]
            # beginning of the time measurement
            self.last_check = [0, 0]
            # end of the time measurement
            self.check = [0, 0]

            # clock value at the beginning in milliseconds and during all the game
            self.player_clock = list(c.CLOCK_VALUE)

        # value in milliseconds of the incrementation (0 = no incrementation)
        self.clock_incrementation = c.CLOCK_INCREMENTATION

    # process
    def _get_process(self):
        return self.process_string

    def _set_process(self, process):

        self.process_string = process

        self.update_caption()

    # allows to store the data and use it in main properly
    process = property(_get_process, _set_process)  # indicate during a game what the players should do

    def start(self, textures):
        """
        starts the game
        """
        # prepare the initial position of the insects
        for insect_data in InitialLayout.classic():
            insect = insect_data[0](insect_data[1], insect_data[2], textures.insect_path)
            # update tile
            self.board.tile(insect.pos, insect)

            # importing insect texture
            textures.save_insect(insect.full_name, insect)

        self.update_caption()
        self.update_ways()

        self.restart()

    def restart(self):
        """
        restart the game after an interrupt
        """
        self.update_all()

        self.start_clock()

    def stop(self):
        """
        end the game and display the reason
        """
        # stop the clock
        self.stop_clock()

        # used to stop the process of moving insects
        self.ended = True

    def change_turn(self):
        """
        change the turn
        """
        self.process = 'choose insect'

        # change the turn value
        turn = self.last_turn
        self.last_turn = self.turn
        self.turn = turn

        # changing window name
        self.update_caption()

        self.update_insects_bol = True

        # delete old last move
        self.board.reset_surface('last move')

        # delete setback log
        self.log = None, None
        # reset setback surface
        self.board.reset_surface('setback')
        self.board.to_draw['setback'] = None

        # calculating insect possible movements
        self.update_ways()

        self.changed_turn = True

        # clock update if clock is on
        if self.clock:
            # update
            self.start_clock()
            # add incrementation to the clock
            self.player_clock[self.turn_number % 2] += self.clock_incrementation

        # update turn number
        self.turn_number = self.turn_number + 1

        self.board_saves.append(self.board)

    def update_caption(self):
        """
        update the window name
        """
        bond = ' - '
        self.caption = c.GAME_NAME + bond + 'In game' + bond + self.turn.capitalize()

    def select_insect(self, tile_pos):
        """
        select the insect if good color
        """

        # check any insect is on this tile
        if self.board.tile_state[tile_pos] is not None:

            # check if insect is owned by the player
            if self.board.tile_state[tile_pos].color == self.turn:

                return self.board.tile_state[tile_pos]

    def choose_insect(self):
        """
        allows the player to select the tile on which there is the insect he want to move
        """

        # return the object of the tile insect if the insect can be selected
        self.tile_insect = self.select_insect(self.tile_pos)

        self.to_draw_board['ways'] = []

        # check is something has been selected
        if self.tile_insect is not None:

            ways, eat = self.tile_insect.ways, self.tile_insect.eat

            for way_cell in ways:
                self.to_draw_board['ways'].append(('tile way', way_cell, 'ways surface'))

            for eat_cell in eat:
                self.to_draw_board['ways'].append(('tile eat', eat_cell, 'eat surface'))

            self.update_board_bol = True
            self.update_insects_bol = True
            self.process = 'choose way'

    def choose_way(self):
        """
        allows the player to give the new position of the selected insect
        """
        reset = True
        self.update_board_bol = True
        self.update_insects_bol = True

        if self.tile_insect is not None:

            # just moove
            if self.tile_pos in self.tile_insect.ways:

                self.last_move = self.tile_insect.pos, self.tile_pos
                self.move(self.tile_insect, self.tile_pos)

                self.display_drag = False
                self.process = 'next turn'
                for tile in self.last_move:
                    self.to_draw_board['last move'].append(('tile move', tile, 'last move surface'))

            # moove and kill
            elif self.tile_pos in self.tile_insect.eat:

                self.last_move = self.tile_insect.pos, self.tile_pos

                self.display_drag = False
                self.kill(self.tile_insect, self.board.tile_state[self.tile_pos])
                self.process = 'next turn'

                for tile in self.last_move:
                    self.to_draw_board['last move'].append(('tile move', tile, 'last kill surface'))

            # select another one
            elif self.board.tile_state[self.tile_pos] is not None:

                # same tile
                if self.tile_pos == self.tile_insect.pos:
                    reset = False
                    self.process = 'choose way'

                # other tile but also an insect from team
                if self.board.tile_state[self.tile_pos].color == self.turn and self.drag:
                    self.choose_insect()

                else:
                    self.display_drag = False

            # tile with nothing on it and which the insect can't go
            else:
                self.process = 'choose insect'
                self.display_drag = False

        if reset:
            # reset surface
            self.board.reset_surface('ways')
            self.board.to_draw['ways'] = None

    # Movement of the insect on the board

    def move(self, insect, new_pos):
        # moving on board
        self.board.tile(insect.pos, None)
        self.board.tile(new_pos, insect)

        # moving object
        insect.pos = new_pos

    def kill(self, murderer, dead):
        self.board.tile(murderer.pos, None)
        murderer.pos = dead.pos

        # special killing -> killer gets killed with the dead insect
        if murderer.kamikaze:
            self.board.tile(dead.pos, None)

        # normal killing -> murderer replacing the dead insect
        else:
            self.board.tile(dead.pos, murderer)

    # movement related
    def update_ways(self):
        """
        update all the possible ways the insects can go
        """

        self.setback = None
        total_paths = []

        for tile in self.board.tile_state:

            if self.board.tile_state[tile] is not None:

                insect = self.board.tile_state[tile]

                ways, eat = self.check_obstacle(insect)

                if insect.color == self.turn:  # check ways

                    new_ways, new_eat = [], []

                    for cell in ways:

                        # check and remove illegal moves
                        if not self.removed_illegal_moves(insect, cell):
                            new_ways.append(cell)

                    for cell in eat:

                        # check and remove illegal moves
                        if not self.removed_illegal_moves(insect, cell):
                            if self.board.tile_state[cell].ant is not True:
                                new_eat.append(cell)

                    insect.ways = new_ways
                    insect.eat = new_eat

                    for cell in new_ways + new_eat:
                        total_paths.append(cell)

                else:  # check setback

                    for cell in eat:

                        # check setback
                        if self.board.tile_state[cell].color != insect.color and self.board.tile_state[cell].ant:
                            self.setback = self.board.tile_state[cell]

        if self.setback is not None:

            # update log
            self.log = None, '{} attacked !'.format(self.turn.capitalize())
            # draw setback tile
            self.to_draw_board['setback'].append(('tile setback', self.setback.pos, 'setback surface'))

        if len(total_paths) == 0:
            if self.setback:
                self.log = self.turn, '{} lost ! Ant stuck'.format(self.turn.capitalize())
                self.stop()
            else:
                self.log = None, 'Draw ! {} cannot move'.format(self.turn.capitalize())
                self.stop()

    def removed_illegal_moves(self, insect, new_pos, temp=None):
        """
        check if this move is an illegal move
        illegal move mean it set its own ant into setback
        """
        if temp is None:
            temp = self.board.tile_state.copy()

        if insect.kamikaze and temp[new_pos] is not None:
            # if insect is kamikaze and eat consider him dead
            temp.update({new_pos: None})
        else:
            temp.update({new_pos: insect})

        temp.update({insect.pos: None})

        # render a picture of all possible move (~3 s loading each move) for debug
        # image = self.board.render(temp, self.textures)

        # try:
        #     pygame.image.save(image, '{}test/{}/{}.png'.format(c.SCREENSHOTS, self.turn_number, insect.pos))
        # except pygame.error:
        #     os.makedirs('{}test/{}/'.format(c.SCREENSHOTS, self.turn_number))
        #     pygame.image.save(image, '{}test/{}/{}.png'.format(c.SCREENSHOTS, self.turn_number, insect.pos))

        for tile in self.board.tile_state:

            insect_attacking = temp[tile]

            # check if someone on it, and if it is an enemy
            if insect_attacking is not None and insect_attacking.color != insect.color:

                # get all the possible path he can get
                paths = self.check_obstacle(temp[tile], temp, paths=True)

                # check them
                for pot_attack_pos in paths:

                    insect_attacked = temp[pot_attack_pos]

                    # check if something on cell, check if there is an opponent on it, and if it is an ant
                    if insect_attacked is not None and insect_attacked.color == insect.color and insect_attacked.ant:
                        # if i split the conditions i can rescue some helpful information
                        # as how many insect it can attack

                        # it is an illegal move because in this case the ant of the insect is attacked by the opponent
                        return True

        # if the method gets to this place it means there is no illegal moves in here
        return False

    def check_obstacle(self, insect, board=None, paths=False):
        """
        check if the insect can go on this tile
        check if the tile is on the board
        check if there is no obstacle or another insect to kill
        """

        if board is None:
            board = self.board.tile_state

        directions_way, pos_eat, eat_last = insect.calc_directions(pos=None)
        ways, eat = [], []

        for direction in directions_way:
            can_continue = True
            i = 0

            # each direction is a list of possible cells
            while can_continue and i < len(direction):
                cell = direction[i]
                i = i + 1

                # check if tile exist and if there is obstacle on it
                if cell in self.board.pos_list:
                    if board[cell] is None:
                        # nothing on this cell
                        ways.append(cell)

                    else:
                        if eat_last and board[cell].color != insect.color:
                            eat.append(cell)
                        can_continue = False

                else:
                    can_continue = False

        for cell in pos_eat:
            # check if tile exist and if there is someone to eat on it
            if cell in self.board.pos_list and board[cell] is not None:
                if board[cell].color != insect.color:

                    eat.append(cell)

                else:
                    # same team so dont eat him
                    pass

        # return every pos this insect can normally go
        if paths:
            return ways + eat
        else:
            return ways, eat

    def check_turn(self):

        if self.changed_turn:
            self.changed_turn = False
            return True

        else:
            return False

    def save(self):
        """
        save current object
        """
        filehandler = open('save.obj', 'wb')
        obj = self.board.tile_state
        pickle.dump(obj, filehandler)
        filehandler.close()

    def open_file(self, file):
        """
        open and convert colors file
        """
        with open(file, 'w') as save:
            save.write(str(self.board_saves))
            save.close()

    # clock related

    def start_clock(self):
        """
        start the clock of the player
        """
        self.last_check[self.turn_number % 2] = self.time.stopwatch.get_ticks()
        self.time.last_update = self.time.stopwatch.get_ticks()

    def update_clock(self):
        """
        update the clock value
        """
        if self.clock:
            i = self.turn_number % 2

            self.player_stopwatch[i] = self.time.stopwatch.get_ticks()-self.last_check[i]
            self.player_clock[i] = self.player_clock[i]-self.player_stopwatch[i]

            self.last_check[(self.turn_number + 1) % 2] = self.time.stopwatch.get_ticks()

            self.last_check[i] = self.time.stopwatch.get_ticks()

            # if time is negative : end the game and lock the time to 0 for the one who ran out of time
            if self.player_clock[i] < 0:
                self.log = self.turn, "{} lost ! Run out of time".format(self.turn.capitalize())
                self.player_clock[i] = 0
                self.stop()

    def stop_clock(self):
        """
        block the clocks
        """
        self.clock = False

    def send_events(self, events, textures):
        """
        events
        """
        events.check(mask_list=self.board.mask_list)

        if events.key == "leave":
            self.save()

        if events.key == "escape":
            events.state = 'menu pause'

        # draw overlay
        for touched_mask in events.mask_touching:

            if touched_mask[3] == "tile":
                self.update_board_bol, self.tile_pos = self.board.draw_tile_overview(touched_mask, textures)

        if not self.ended:

            if self.process == "next turn":
                self.change_turn()
                self.board.to_draw['ways'] = None

            # act after a click
            if events.click:

                self.drag = True
                self.display_drag = True
                self.update_process = True
                self.update_board_bol = True

            elif self.drag and not events.mouse_but_down:

                self.drag = False
                self.display_drag = False
                self.update_process = True

            if self.update_process:

                self.click = events.click

                if self.process == 'choose insect':

                    self.choose_insect()

                elif self.process == "choose way":

                    self.choose_way()

                self.update_process = False

    def update_all(self):
        """
        update every surfaces
        """
        self.update_board_bol = True
        self.update_display_bol = True
        self.update_insects_bol = True

    def check_updates(self, textures):
        """
        check updates
        """
        if self.update_board_bol or self.static_board is None:
            self.update_display_bol = True
            self.update_board(textures)

        if self.update_insects_bol:
            self.update_display_bol = True
            self.update_insects(textures)

        if self.moving_insect is not None:
            self.update_insects_bol = True

    def update_board(self, textures):
        """
        update only the static board named static_board
        """

        self.update_board_bol = False
        self.static_board = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)

        # draw the board to erase old position of the insects for the next update
        self.board.draw_surface(draw_this_surface=textures.game["board"], on_this_surface=self.static_board,
                                disp_pos=c.CENTER, center=False)

        # draw every overlays on the board (ways, last move, setback)
        if self.board.draw_ways:
            # create surface if it needs to be updated
            for category in self.to_draw_board:

                if len(self.to_draw_board[category]) > 0:
                    self.board.game_draw(category, self.to_draw_board[category], textures)
                    self.to_draw_board[category] = []

                # draw the surfaces
                if self.board.to_draw[category] is not None:
                    self.board.draw_surface(draw_this_surface=self.board.to_draw[category],
                                            on_this_surface=self.static_board, disp_pos=c.CENTER, center=False)

        return self.static_board

    def update_insects(self, textures):
        """
        update only the insect surface named insect_board
        """

        self.update_insects_bol = False
        self.insect_board = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)

        # draw the insects
        for tile in self.board.tile_state:
            if self.board.tile_state[tile] is not None:
                insect = self.board.tile_state[tile]

                # draw the insect that is dragged near the mouse
                if insect is self.tile_insect and self.display_drag:
                    self.moving_insect = insect

                else:
                    self.board.draw_surface(draw_this_surface=textures.dflt[insect.full_name],
                                            on_this_surface=self.insect_board, disp_pos=self.board.position(insect.pos))

    def update_screen(self, display, textures, events):
        """
        update the whole screen
        """
        if self.update_display_bol:

            # clean screen
            display.draw_screen()

            # update caption
            if display.caption != self.caption:
                display.set_caption(caption=self.caption)
            display.draw_screen()

            # update the screen
            log_text = str((self.tile_pos, self.turn_number))

            log = textures.font["menu button"].render(log_text, True, textures.colors["button text"])
            display.draw_surface_screen(log, c.CENTER, False)

            # update clock
            self.update_clock()

            # table on the right
            display.draw_table(self.last_turn, self.turn, self.process, self.player_clock, textures)

            if self.log is not None:
                display.big_log(self.log[1], textures)

            # draw the board
            display.draw_surface_screen(draw_this_surface=self.static_board)

            # draw the mouse tile pos
            display.draw_surface_screen(draw_this_surface=self.board.mouse_interaction_surface, disp_pos=c.CENTER,
                                        center=False)

            # draw the insects
            display.draw_surface_screen(draw_this_surface=self.insect_board, disp_pos=c.CENTER, center=False)

            if self.moving_insect is not None:
                if self.display_drag:
                    display.draw_surface_screen(draw_this_surface=textures.dflt[self.moving_insect.full_name],
                                                disp_pos=events.mouse_pos, center=True)

                else:
                    self.moving_insect = None

            # update
            pygame.display.flip()
            self.update_display_bol = False


class Time:
    """
    time
    """
    def __init__(self):

        self.clock = pygame.time.Clock()
        self.stopwatch = pygame.time
        self.last_update = None

    def tick(self):
        """
        limit frame rate
        """
        self.clock.tick(c.FPS)

    def check_display_update(self):
        if self.last_update // 100 != self.stopwatch.get_ticks() // 100:
            self.last_update = self.stopwatch.get_ticks()
            return True
        return False
