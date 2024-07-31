import customtkinter as ctk
import os
from elements import *
from settings import *

# first things first
makeEverythingOk()  # nem az életed, de jó lenne, mi? :)

class Database(ctk.CTk):
    def __init__(self):
        super().__init__()

        # window settings
        self.window_width = self.winfo_screenwidth()//2++self.winfo_screenwidth()//4
        self.window_height = self.winfo_screenheight()//1.3

        self.geometry(f'{self.window_width}x{self.window_height}')
        self.minsize(self.window_width, self.window_height)  # we ignore that this is a float number

        self.title('Adatbázis kezelő - Formáld a világot')
        self.iconbitmap(os.getcwd() + '\\' + '_img' + '\\' + 'icon.ico')

        ctk.set_appearance_mode('dark')

        # data
        self.database_statuses = SajatDictVar()  # tárolja a megnyitott, illetve bezárt adatbázisokat
        self.dblist_buttons_placed = SajatDictVar()  # tárolja az adatbázis listában lévő elemeket / szekciókat
        self.opened_db = ctk.StringVar(value = 'Nyiss meg egy Adatbázist')
        self.opened_segitseg = False

        # style
        selectedDbFont = ctk.CTkFont(family = MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                                     size = MAINWINDOW_SELECTED_DBTEXT_SIZE)

        averageButtonFont = ctk.CTkFont(family = AVERAGE_BUTTON_FAMILY,
                                        size = AVERAGE_BUTTON_TSIZE)

        # layout
        self.rowconfigure(0, weight = 1, uniform = 'mainwindow')
        self.rowconfigure(1, weight = 5, uniform = 'mainwindow')

        self.columnconfigure(0, weight = 2, uniform = 'mainwindow')
        self.columnconfigure(1, weight = 5, uniform = 'mainwindow')
        self.columnconfigure(2, weight = 1, uniform = 'mainwindow')

        # widgets
        self.reload_button = ctk.CTkButton(self,
                                           text = 'Újratöltés',
                                           command = self.reload_func,
                                           fg_color = AVERAGE_BUTTON_BG_COLOR,
                                           hover_color = AVERAGE_BUTTON_HOVER_COLOR,
                                           text_color = AVERAGE_BUTTON_TCOLOR,
                                           font = averageButtonFont)

        self.title_label = ctk.CTkLabel(self, textvariable = self.opened_db, font = selectedDbFont, text_color = MAINWINDOW_SELECTED_DBTEXT_COLOR)

        self.appearance_button = ctk.CTkButton(self,
                                               text = 'Mód: Sötét',
                                               command = self.change_appearance_mode,
                                               fg_color = AVERAGE_BUTTON_BG_COLOR,
                                               hover_color = AVERAGE_BUTTON_HOVER_COLOR,
                                               text_color = AVERAGE_BUTTON_TCOLOR,
                                               font = averageButtonFont)

        self.database_frame = DatabaseList(parent = self,
                                      status = self.database_statuses,
                                      buttons_placed = self.dblist_buttons_placed,
                                      opened_db_var = self.opened_db)

        self.main_center_frame = MainCenterFrame(parent = self, number_of_pages = 4)
        self.main_center_frame.add_page('Adatbázis', page_window = databasePage(parent = self.main_center_frame,
                                                                           dbase_name_var = self.opened_db))
        self.main_center_frame.add_page('Táblák', page_window = tablePage(parent = self.main_center_frame,
                                                                           dbase_name_var = self.opened_db))
        self.main_center_frame.add_page('Adatmanipuláció', page_window=datamanipulationPage(parent = self.main_center_frame,
                                                                                       dbase_name_var = self.opened_db))
        self.main_center_frame.add_page('Lekérdezés', page_window=queryPage(parent=self.main_center_frame,
                                                                                 dbase_name_var = self.opened_db))

        self.teszt = ctk.CTkButton(self,
                                   text = 'Segítség',
                                   command = self.open_segitseg,
                                   fg_color = AVERAGE_BUTTON_BG_COLOR,
                                   hover_color = AVERAGE_BUTTON_HOVER_COLOR,
                                   text_color = AVERAGE_BUTTON_TCOLOR,
                                   font = averageButtonFont)

        # grid
        self.reload_button.grid(row = 0, column = 0, sticky = 'nsew', padx = 60, pady = 35)
        self.title_label.grid(row = 0, column = 1, sticky = 'nsew')
        self.appearance_button.grid(row = 0, column = 2, sticky = 'nsew', padx = 30, pady = 40)
        self.database_frame.grid(row = 1, column = 0, sticky = 'nsew', padx = 5, pady = 5)
        self.main_center_frame.grid(row = 1, column = 1, sticky = 'nsew', padx = 5, pady = 5)
        self.teszt.grid(row = 1, column = 2)

    def change_appearance_mode(self):
        if 'Sötét' in self.appearance_button.cget('text'):
            self.appearance_button.configure(text = 'Mód: Világos')
            ctk.set_appearance_mode('light')
        else:
            self.appearance_button.configure(text='Mód: Sötét')
            ctk.set_appearance_mode('dark')

    def open_segitseg(self):
        if not self.opened_segitseg:
            segitsegablak = segitsegAblak()

            segitsegablak.protocol("WM_DELETE_WINDOW", lambda: self.close_segitseg(segitsegablak))
            self.opened_segitseg = True

    def close_segitseg(self, ablak):
        self.opened_segitseg = False

        with open('_query.query', 'w', encoding='utf-8', buffering=1) as f:
            f.write('')

        ablak.destroy()

    def reload_func(self):
        self.destroy()

        os.system('Database.py')


if __name__ == '__main__':
    database = Database()
    database.mainloop()
