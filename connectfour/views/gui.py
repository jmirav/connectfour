import Tkinter as tk

from connectfour import pubsub

from connectfour.util.color import get_color_list
from connectfour.views.gui_config import (
    WINDOW_TITLE_TEXT, GAME_TITLE_TEXT, SETUP_TITLE_TEXT,
    ADD_PLAYER_TEXT, LAUNCH_GAME_TEXT, PLAY_AGAIN_TEXT,
    COLUMN_TEXT, QUIT_TEXT, PLAYER_FEEDBACK_TEXT,
    SQUARE_BACKGROUND, SQUARE_SIZE, SQUARE_BORDER_WIDTH,
    FLASH_CYCLES, FLASH_CYCLE_TIME, FLASH_WAIT_TIME,
    COLOR_TO_TK, REASON_TO_STR, PAD,
)

COLORS = get_color_list()


class GUIView(object):

    def __init__(self, game):
        self.game = game

        self._create_subscriptions()

        # Store widgets here
        self.widgets = {}

        # Initialize GUI window
        window = tk.Tk()
        window.title(WINDOW_TITLE_TEXT)
        self.widgets['window'] = window

        # Initialize and launch setup screen
        self._create_setup_frame()
        window.mainloop()

        # Cleanup once main loop ends
        window.destroy()

    def _create_subscriptions(self):
        responses = {
            pubsub.Action.player_added: self._on_player_added,
            pubsub.Action.round_started: self._on_round_started,
            pubsub.Action.next_player: self._on_next_player,
            pubsub.Action.try_again: self._on_try_again,
            pubsub.Action.disc_played: self._on_disc_played,
            pubsub.Action.round_won: self._on_round_won,
            pubsub.Action.round_draw: self._on_round_draw,
        }

        for action, response in responses.iteritems():
            pubsub.subscribe(action, response)

    ###########################
    # Widgets for Setup Frame #
    ###########################

    def _create_setup_frame(self):
        setup_frame = tk.Frame(self.widgets['window'])
        setup_frame.grid(padx=PAD, pady=PAD)
        self.widgets['setup_frame'] = setup_frame
        self._create_setup_components()

    def _create_setup_components(self):
        TITLE_ROW = 0
        DIMENSIONS_ROW = 1
        ADD_PLAYER_ROW = 2
        PLAYER_FEEDBACK_ROW = 3
        CONTROL_ROW = 4

        self._create_setup_title_row(TITLE_ROW)
        self._create_dimensions_row(DIMENSIONS_ROW)
        self._create_add_player_row(ADD_PLAYER_ROW)
        self._create_player_feedback_row(PLAYER_FEEDBACK_ROW)
        self._create_setup_control_row(CONTROL_ROW)

    def _create_setup_title_row(self, row):
        setup_title = tk.Label(self.widgets['setup_frame'],
                               text=SETUP_TITLE_TEXT)
        setup_title.grid(row=row, columnspan=3)

    def _create_dimensions_row(self, row):

        def create_dimension_pair(column, text, default, widget_name):
            frame = tk.Frame(self.widgets['setup_frame'])
            frame.grid(row=row, column=column, padx=PAD, pady=PAD)

            prompt = tk.Label(frame, text=text)
            prompt.grid(row=0, column=0)

            entry = tk.Entry(frame, width=1)
            entry.insert(tk.END, default)
            entry.grid(row=0, column=1)
            self.widgets[widget_name] = entry

        create_dimension_pair(
            column=0, text='Rows:', default='6', widget_name='row_entry')
        create_dimension_pair(
            column=1, text='Columns:', default='7',
            widget_name='column_entry')
        create_dimension_pair(
            column=2, text='To Win:', default='4',
            widget_name='to_win_entry')

    def _create_add_player_row(self, row):
        player_entry = tk.Entry(self.widgets['setup_frame'])
        player_entry.grid(row=row, column=0, columnspan=2, pady=PAD)
        self.widgets['player_entry'] = player_entry

        add_player_button = tk.Button(self.widgets['setup_frame'],
                                      text=ADD_PLAYER_TEXT,
                                      command=self._add_player)

        add_player_button.grid(row=row, column=2)
        self.widgets['add_player_button'] = add_player_button

    def _create_player_feedback_row(self, row):
        player_feedback = tk.Message(self.widgets['setup_frame'], width=500)
        player_feedback.grid(row=row, columnspan=3, pady=PAD)
        self.widgets['player_feedback'] = player_feedback

    def _create_setup_control_row(self, row):
        setup_quit_button = tk.Button(self.widgets['setup_frame'],
                                      text=QUIT_TEXT,
                                      command=self.widgets['window'].quit)
        setup_quit_button.grid(row=row, column=0)

        launch_game_button = tk.Button(self.widgets['setup_frame'],
                                       text=LAUNCH_GAME_TEXT,
                                       state=tk.DISABLED,
                                       command=self._launch_game)
        launch_game_button.grid(row=row, column=2)
        self.widgets['launch_game_button'] = launch_game_button

    ##########################
    # Widgets for Game Frame #
    ##########################

    def _create_game_frame(self):
        game_frame = tk.Frame(self.widgets['window'])
        game_frame.grid()
        self.widgets['game_frame'] = game_frame
        self._create_game_components()

    def _create_game_components(self):
        TITLE_ROW = 0
        FEEDBACK_ROW = 1
        COLUMN_BUTTONS_ROW = 2
        GRID_START_ROW = 3
        CONTROL_ROW = GRID_START_ROW + self.game.get_num_rows()

        self._create_game_title_row(TITLE_ROW)
        self._create_game_feedback_row(FEEDBACK_ROW)
        self._create_column_buttons_row(COLUMN_BUTTONS_ROW)
        self._create_game_grid(GRID_START_ROW)
        self._create_game_control_row(CONTROL_ROW)

    def _create_game_title_row(self, row):
        game_title = tk.Label(self.widgets['game_frame'], text=GAME_TITLE_TEXT)
        game_title.grid(row=row, columnspan=self.game.get_num_columns())

    def _create_game_feedback_row(self, row):
        game_feedback = tk.Label(self.widgets['game_frame'])
        game_feedback.grid(row=row, columnspan=self.game.get_num_columns())
        self.widgets['game_feedback'] = game_feedback

    def _create_column_buttons_row(self, row):
        column_buttons = []

        for column in range(self.game.get_num_columns()):
            button = tk.Button(self.widgets['game_frame'], text=COLUMN_TEXT,
                               command=lambda i=column: self._play_disc(i))
            button.grid(row=row, column=column)
            column_buttons.append(button)

        self.widgets['column_buttons'] = column_buttons

    def _create_game_grid(self, start_row):
        num_rows = self.game.get_num_rows()
        num_columns = self.game.get_num_columns()
        # Create 2D array to hold pointers to slot widgets
        squares = [[None for column in range(num_columns)]
                   for row in range(num_rows)]

        for row in range(num_rows):
            for column in range(num_columns):
                square = tk.Frame(self.widgets['game_frame'],
                                  width=SQUARE_SIZE, height=SQUARE_SIZE,
                                  bg=SQUARE_BACKGROUND, bd=SQUARE_BORDER_WIDTH,
                                  relief=tk.RAISED)
                square.grid(row=row + start_row, column=column)
                squares[row][column] = square

        self.widgets['squares'] = squares

    def _create_game_control_row(self, row):
        play_again_button = tk.Button(self.widgets['game_frame'],
                                      text=PLAY_AGAIN_TEXT,
                                      command=self._play_again)
        play_again_button.grid(row=row, column=0, columnspan=2)
        self.widgets['play_again_button'] = play_again_button

        game_quit_button = tk.Button(self.widgets['game_frame'],
                                     text=QUIT_TEXT,
                                     command=self.widgets['window'].quit)
        game_quit_button.grid(row=row, column=2, columnspan=2)

    #################################
    # Button (de)activation helpers #
    #################################
    def _enable_column_buttons(self):
        for button in self.widgets['column_buttons']:
            button.configure(state=tk.NORMAL)

    def _disable_column_buttons(self):
        for button in self.widgets['column_buttons']:
            button.configure(state=tk.DISABLED)

    ###########################################
    # Button callbacks (which call the model) #
    ###########################################

    def _add_player(self):
        name = self.widgets['player_entry'].get()
        index = self.game.get_num_players()
        color = COLORS[index]
        self.game.add_player(name, color)
        self.widgets['player_entry'].delete(0, 'end')

    def _launch_game(self):
        # Add board to model
        num_rows = int(self.widgets['row_entry'].get())
        num_columns = int(self.widgets['column_entry'].get())
        num_to_win = int(self.widgets['to_win_entry'].get())

        self.game.add_board(num_rows, num_columns, num_to_win)

        # Move on to game frame
        self.widgets['setup_frame'].grid_forget()
        self._create_game_frame()
        self.game.start_round()

    def _play_again(self):
        self.widgets['game_frame'].grid_forget()
        self._create_game_frame()
        self.game.start_round()

    def _play_disc(self, column):
        self.game.play_disc(column)

    ################################
    # Respond to events from model #
    ################################

    def _on_player_added(self, player):
        self.widgets['player_feedback'].configure(text=(
            PLAYER_FEEDBACK_TEXT.format(player, self.game.get_num_players())))

        # Only one player is needed to enable start button
        self.widgets['launch_game_button'].configure(state=tk.NORMAL)

    def _on_round_started(self, round_number):
        self.widgets['play_again_button'].configure(state=tk.DISABLED)
        self._enable_column_buttons()

    def _on_next_player(self, player):
        self.widgets['game_feedback'].configure(
            text="{}'s turn".format(player))

    def _on_try_again(self, player, reason):
        self.widgets['game_feedback'].configure(
            text='{} try again ({})'.format(player, REASON_TO_STR[reason]))

    def _on_disc_played(self, player, position):
        row, column = position
        self.widgets['squares'][row][column].configure(
            bg=COLOR_TO_TK[player.disc.color])

    def flash(self, element):
        original_color = element['bg']

        for i in range(FLASH_CYCLES):
            self.widgets['window'].after(
                FLASH_WAIT_TIME + FLASH_CYCLE_TIME * i,
                lambda: element.config(bg=SQUARE_BACKGROUND))
            self.widgets['window'].after(
                int(FLASH_WAIT_TIME + FLASH_CYCLE_TIME * (i + 0.5)),
                lambda: element.config(bg=original_color))

    def _on_round_won(self, player, winning_positions):
        self.widgets['game_feedback'].configure(
            text='{} won the round'.format(player))
        self._disable_column_buttons()

        for row, column in winning_positions:
            self.flash(self.widgets['squares'][row][column])

        self.widgets['play_again_button'].configure(state=tk.NORMAL)

    def _on_round_draw(self):
        self.widgets['game_feedback'].configure(text='Round ended in a draw')
        self._disable_column_buttons()
        self.widgets['play_again_button'].configure(state=tk.NORMAL)
