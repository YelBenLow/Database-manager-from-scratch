import customtkinter as ctk
import tkinter as tk
import datetime #from datetime import datetime
from tkinter import ttk
from PIL import Image, ImageTk
from functions import *
from settings import *


class SajatDictVar:
    def __init__(self, alap_dict = {}):
        self.mydict = alap_dict

    def get(self):
        return self.mydict

    def set(self, your_dict: dict):
        if type(your_dict) == dict:
            self.mydict = your_dict
        else:
            print(f'Szótárat adj meg paraméternek! ({your_dict})')

    def update_dictionary(self, your_dict: dict):
        try:
            self.mydict.update(your_dict)
        except Exception as e:
            print(f'Szótárat adj meg paraméternek! ({your_dict})')

    def delete_element(self, item):
        try:
            del self.mydict[item]
        except Exception as e:
            pass


class DatabaseList(ctk.CTkFrame):
    def __init__(self, parent, status, buttons_placed, opened_db_var):
        super().__init__(master = parent)

        # layout
        self.rowconfigure(list(range(10)), weight = 1, uniform = 'DatabaseList')
        self.columnconfigure(0, weight = 1, uniform = 'DatabaseList')
        self.buttons_placed = buttons_placed

        # data
        self.current_databases = get_current_databases()
        self.last_row_placed = ctk.IntVar(value = 0)  # db létrehozásnál az utolsó sorba illessze az új db-t
        self.opened_db_var = opened_db_var
        self.dbcreateordbdelete = ''

        if self.current_databases:
            self.database_status = SajatDictVar({name: ctk.StringVar(value = 'Closed') for name in self.current_databases})
            status.set(self.database_status.get())

            # trace
            for stringvar in self.database_status.get().values():
                stringvar.trace('w', self.update_dict)

            # widgets
            for index, databasename in enumerate(self.current_databases):
                self.databasename = DatabaseListButtonWidget(parent = self,
                                                             database_name = databasename,
                                                             checkbox_var = self.database_status.get()[databasename])
                self.databasename.grid(row = index+1, column = 0)
                self.buttons_placed.update_dictionary({databasename: self.databasename})

                self.last_row_placed.set(index + 1)


        else:
            create_database('example')

            self.database_status = SajatDictVar(alap_dict = {'example': ctk.StringVar(value = 'Closed')})
            status.set(self.database_status.get())

            self.example = DatabaseListButtonWidget(parent=self,
                                                    database_name='example',
                                                    checkbox_var=self.database_status.get()['example'])
            self.example.grid(row=1, column=0)
            self.buttons_placed.update_dictionary({'example': self.example})

            self.database_status.get()['example'].trace('w', self.update_dict)

            self.last_row_placed.set(1)

        # fonts
        dbtitleFont = ctk.CTkFont(family = DBLIST_TITLE_FAMILY,
                                  size = DBLIST_TITLE_TSIZE)

        averageButtonFont = ctk.CTkFont(family=AVERAGE_BUTTON_FAMILY,
                                        size=AVERAGE_BUTTON_TSIZE)

        # widgets also
        self.databaseTitle = ctk.CTkLabel(self,
                                          text = 'Jelenlegi Adatbázisok',
                                          text_color = DBLIST_TITLE_TCOLOR,
                                          font = dbtitleFont)

        self.createDatabaseBtn = ctk.CTkButton(self, text = '+',
                                               command = lambda: self.show_create_popup(status,'Létrehozása'),
                                               fg_color = AVERAGE_BUTTON_BG_COLOR,
                                               hover_color = AVERAGE_BUTTON_HOVER_COLOR,
                                               text_color = AVERAGE_BUTTON_TCOLOR,
                                               font = averageButtonFont,
                                               width = 50,
                                               height = 50)

        self.deleteDatabaseBtn = ctk.CTkButton(self,
                                               text = 'Del',
                                               command = lambda: self.show_delete_popup(status,'Törlése'),
                                               fg_color=AVERAGE_BUTTON_BG_COLOR,
                                               hover_color=AVERAGE_BUTTON_HOVER_COLOR,
                                               text_color=AVERAGE_BUTTON_TCOLOR,
                                               font=averageButtonFont,
                                               width = 50,
                                               height = 50)

        # grid
        self.databaseTitle.grid(row = 0, column = 0)
        self.createDatabaseBtn.grid(row = 0, column = 0, sticky = 'e', padx = 10)
        self.deleteDatabaseBtn.grid(row = 0, column = 0, sticky = 'w', padx = 10)
    def update_dict(self, *args):
        index_changed = args[0]  # melyik checkbox értéke változott
        status_changed_to = None
        is_open = False  # van-e megnyitott db

        for dbname, prettifyvar in self.database_status.get().items():
            if '.!databaselist' in str(prettifyvar):
                self.database_status.get()[dbname] = prettifyvar.kivalaszt_checkbox.cget('variable')

        # itt kiválasztjuk a változott checkbox StringVarját, hogy ha kinyitottuk a db-t, akkor ne zárjuk be egyből
        # amit ebben a sorban teszünk lehetővé (84):  if stringvar != status_changed_to
        for index, value in enumerate((self.database_status.get().values())):
            if value.get() == 'Opened':
                is_open = True
            if str(value) == index_changed:
                status_changed_to = value

        if not is_open:
            self.opened_db_var.set('Nyiss meg egy Adatbázist')

        # ha openeltük a db-t, akkor az összes db-t bezárjuk, kivéve amit megnyitottunk
        for databasename, stringvar in self.database_status.get().items():
            if stringvar != status_changed_to and status_changed_to.get().split()[-1] == 'Opened':
                stringvar.set('Closed')

            elif stringvar == status_changed_to and status_changed_to.get().split()[-1] == 'Opened':
                self.opened_db_var.set(databasename)
                is_open = True

    def show_create_popup(self, status, operation):
        if self.dbcreateordbdelete == 'Törlés':
            self.popup_exit_func('Törlése')
        self.dbcreateordbdelete = 'Létrehoz'

        self.DataBasePopupExit = ctk.CTkButton(self,
                                               text='X',
                                               command=lambda: self.popup_exit_func('Létrehozása'),
                                               fg_color = DBLIST_POPUP_BTN_BG_COLOR,
                                               hover_color = AVERAGE_BUTTON_HOVER_COLOR,
                                               text_color = AVERAGE_BUTTON_TCOLOR,
                                               font = ctk.CTkFont(family = AVERAGE_BUTTON_FAMILY,
                                                                  size = AVERAGE_BUTTON_TSIZE))

        self.createDatabasePopup = PopUp(parent=self,
                                         listparent=self,
                                         mainstatus=status,
                                         status=self.database_status,
                                         last_row=self.last_row_placed,
                                         trackfunc=self.update_dict,
                                         obj_to_lift=self.DataBasePopupExit,
                                         operation=operation)

        self.createDatabasePopup.place(relx=0.08, rely=0.2, relwidth = 0.8, relheight = 0.5)
        self.DataBasePopupExit.place(relx = 0.7, rely = 0.22, relwidth = 0.15, relheight = 0.08)

        self.createDatabasePopup.lift()
        self.DataBasePopupExit.lift()

    def show_delete_popup(self, status, operation):
        if self.dbcreateordbdelete == 'Létrehoz':
            self.popup_exit_func('Létrehozása')
        self.dbcreateordbdelete = 'Törlés'

        self.DataBasePopupExit = ctk.CTkButton(self,
                                               text='X',
                                               command=lambda: self.popup_exit_func('Törlése'),
                                               fg_color=DBLIST_POPUP_BTN_BG_COLOR,
                                               hover_color=AVERAGE_BUTTON_HOVER_COLOR,
                                               text_color=AVERAGE_BUTTON_TCOLOR,
                                               font=ctk.CTkFont(family=AVERAGE_BUTTON_FAMILY,
                                                                size=AVERAGE_BUTTON_TSIZE))
        self.deleteDatabasePopup = PopUp(parent=self,
                                         listparent=self,
                                         mainstatus=status,
                                         status=self.database_status,
                                         last_row=self.last_row_placed,
                                         trackfunc=self.update_dict,
                                         obj_to_lift=self.DataBasePopupExit,
                                         operation=operation)

        self.deleteDatabasePopup.place(relx=0.08, rely=0.2, relwidth=0.8, relheight=0.5)
        self.DataBasePopupExit.place(relx=0.7, rely=0.22, relwidth=0.15, relheight=0.08)

        self.deleteDatabasePopup.lift()
        self.DataBasePopupExit.lift()

    def popup_exit_func(self, which):
        if which == 'Létrehozása':
            self.createDatabasePopup.place_forget()
            self.DataBasePopupExit.place_forget()
        elif which == 'Törlése':
            self.deleteDatabasePopup.place_forget()
            self.DataBasePopupExit.place_forget()


class PopUp(ctk.CTkFrame):
    def __init__(self, parent, listparent, mainstatus, status, last_row, trackfunc, obj_to_lift, operation):
        super().__init__(master = parent, fg_color = DBLIST_POPUP_BG_COLOR)
        # data
        self.adatbazis_neve = ctk.StringVar()
        self.obj_need_to_lift = obj_to_lift

        # fonts
        titlefont = ctk.CTkFont(family = DBLIST_TITLE_FAMILY,
                                size = DBLIST_TITLE_TSIZE)

        innertitlefont = ctk.CTkFont(family = DBLIST_TITLE_FAMILY,
                                     size = DBLIST_INNERTITLE_TSIZE)

        buttonfont = ctk.CTkFont(family = AVERAGE_BUTTON_FAMILY,
                                 size = AVERAGE_BUTTON_TSIZE)

        # widgets
        self.popupname = ctk.CTkLabel(self, text = f'Adatbázis {operation}', font = titlefont)
        self.adatbazisnev = ctk.CTkLabel(self, textvariable = self.adatbazis_neve, font = innertitlefont)
        self.input_entry = ctk.CTkEntry(self, textvariable = self.adatbazis_neve)
        self.create_btn = ctk.CTkButton(self, text = operation[:-1],
                                        command = lambda: self.db_list_functions(db_name = self.adatbazis_neve,
                                                                                 mainstatus = mainstatus,
                                                                                 status = status,
                                                                                 last_row = last_row,
                                                                                 listparent = listparent,
                                                                                 track_func = trackfunc,
                                                                                 operation = operation),
                                        fg_color = DBLIST_POPUP_BTN_BG_COLOR,
                                        hover_color = AVERAGE_BUTTON_HOVER_COLOR,
                                        text_color = AVERAGE_BUTTON_TCOLOR,
                                        font = buttonfont)
        self.statusz = ctk.CTkLabel(self, text = 'Státusz\nParancsra várás', font = titlefont)

        # pack
        self.popupname.place(relx = 0.1, rely = 0.08)
        self.adatbazisnev.place(relx = 0.28, rely = 0.28)
        self.input_entry.place(relx = 0.25, rely = 0.4)
        self.create_btn.place(relx = 0.25, rely = 0.5)
        self.statusz.pack(side = 'bottom', fill = 'x', pady = 20, padx = 20)

    def db_list_functions(self, listparent, db_name, mainstatus, status, last_row, track_func, operation):
        db_name = db_name.get()
        if operation == 'Létrehozása':
            if db_name.count(' ') == len(db_name) or len(db_name) == 0:
                self.statusz.configure(text=f'Státusz\nNe csak szóközökből\n álljon a név!')
                return

            elif create_database(db_name) == 'Siker':
                self.statusz.configure(text = f'Státusz\nAdatbázis létrehozva!\n({db_name})')

                status.update_dictionary({db_name: ctk.StringVar(value = 'Closed')})
                mainstatus.update_dictionary({db_name: ctk.StringVar(value = 'Closed')})
                last_row.set(last_row.get()+1)

                mainstatus.get()[db_name].trace('w', track_func)

                newSection = DatabaseListButtonWidget(parent=listparent,
                                                      database_name=db_name,
                                                      checkbox_var=mainstatus.get()[db_name])

                newSection.grid(row=last_row.get(), column=0)

                listparent.buttons_placed.update_dictionary({db_name: newSection})

                self.lift()
                self.obj_need_to_lift.lift()
                return

            else:
                self.statusz.configure(text = f'Státusz\nAz adatbázis már létezik!\n({db_name})')
                return

        elif operation == 'Törlése':
            if db_name.count(' ') == len(db_name) or len(db_name) == 0:
                self.statusz.configure(text=f'Státusz\nNe csak szóközökből\n álljon a név!')
                return

            elif delete_database(db_name) == 'Siker':
                self.statusz.configure(text = f'Státusz\nAdatbázis törölve!\n({db_name})')


                # re-grid
                listparent.buttons_placed.get()[db_name].grid_forget()
                listparent.buttons_placed.delete_element(db_name)

                status.delete_element(db_name)
                mainstatus.delete_element(db_name)
                last_row.set(1)

                for object in listparent.buttons_placed.get().values():
                    object.grid(row = last_row.get(), column = 0)
                    last_row.set(last_row.get()+1)
                last_row.set(len(listparent.buttons_placed.get()))

                self.lift()
                self.obj_need_to_lift.lift()
                return

            else:
                self.statusz.configure(text=f'Státusz\nAz adatbázis nem létezik!\n({db_name})')
                return


class DatabaseListButtonWidget(ctk.CTkFrame):
    def __init__(self, parent, database_name, checkbox_var):
        super().__init__(master = parent, fg_color = DBLIST_LIST_BGCOLOR)

        # fonts
        buttonkafont = ctk.CTkFont(family = AVERAGE_BUTTON_FAMILY,
                                   size = AVERAGE_BUTTON_TSIZE-2)

        # widgets
        self.buttonka = ctk.CTkButton(self,
                                      text = database_name,
                                      fg_color = DBLIST_LIST_BTN_BG_COLOR,
                                      hover_color = AVERAGE_BUTTON_HOVER_COLOR,
                                      text_color = AVERAGE_BUTTON_TCOLOR,
                                      font = buttonkafont)

        self.kivalaszt_checkbox = ctk.CTkCheckBox(self,
                                                  text = 'Open',
                                                  variable = checkbox_var,
                                                  onvalue = 'Opened',
                                                  offvalue = 'Closed',
                                                  border_width = 1,
                                                  font = buttonkafont)
        self.bezar_checkbox = ctk.CTkCheckBox(self,
                                              text='Close',
                                              variable = checkbox_var,
                                              onvalue = 'Closed',
                                              offvalue = 'Opened',
                                              border_width = 1,
                                              font = buttonkafont)

        # pack
        self.buttonka.pack(side = 'left', padx = 5)
        self.kivalaszt_checkbox.pack(side = 'left', padx = 5)
        self.bezar_checkbox.pack(side = 'left', padx = 5)



class MainCenterFrame(ctk.CTkFrame):
    def __init__(self, parent, number_of_pages):
        super().__init__(master = parent)

        # main layout
        self.columnconfigure(0, weight = 1, uniform = 'mainpage')
        self.rowconfigure(0, weight = 1, uniform = 'mainpage')
        self.rowconfigure(1, weight = 8, uniform = 'mainpage')

        # data
        self.number_of_pages = number_of_pages
        self.sold_columns = 0
        self.last_opened_page = None
        self.page_buttons = {}
        self.page_objects = {}

        # widget
        self.page_frame = ctk.CTkFrame(self)

        # page layout
        self.page_frame.columnconfigure(list(range(self.number_of_pages)), weight=1, uniform='pagewidget')
        self.page_frame.rowconfigure(0, weight=1, uniform='pagewidget')

        # pack
        self.page_frame.grid(column = 0, row = 0, sticky = 'nsew', padx = 5, pady = 5)


    def add_page(self, page_name, page_window):

        # fonts
        buttontextfont = ctk.CTkFont(family = AVERAGE_BUTTON_FAMILY,
                                     size = AVERAGE_BUTTON_TSIZE)

        # widgets
        page_button = ctk.CTkButton(self.page_frame,
                                    text = page_name,
                                    command = lambda: self.switch_pages(page_name),
                                    fg_color = MAINFRAME_BTN_BG_COLOR,
                                    hover_color = AVERAGE_BUTTON_HOVER_COLOR,
                                    text_color = AVERAGE_BUTTON_TCOLOR,
                                    text_color_disabled = AVERAGE_DISABLEDBUTTON_TCOLOR,
                                    font = buttontextfont)
        self.page_objects[page_name] = page_window

        self.page_buttons[page_name] = page_button

        # grid
        page_button.grid(column = self.sold_columns, row = 0)

        self.sold_columns += 1
    def switch_pages(self, button_name):
        if self.last_opened_page == None: # ha először nyitunk meg egy oldalt
            self.last_opened_page = button_name
            self.page_objects[self.last_opened_page].grid(column = 0,
                                                          columnspan = self.number_of_pages,
                                                          row = 1,
                                                          sticky = 'nsew',
                                                          padx = 5,
                                                          pady = 5)

            self.page_buttons[self.last_opened_page].configure(state = 'disabled')

        elif self.last_opened_page != None and self.last_opened_page != button_name: # megnyitott oldal töröl, új oldal lerak
            # print(f'{self.last_opened_page} -> {button_name}')
            self.page_objects[self.last_opened_page].grid_forget()
            self.page_buttons[self.last_opened_page].configure(state='normal')


            self.last_opened_page = button_name
            self.page_objects[self.last_opened_page].grid(column = 0,
                                                          columnspan = self.number_of_pages,
                                                          row = 1,
                                                          sticky = 'nsew',
                                                          padx = 5,
                                                          pady = 5)

            self.page_buttons[self.last_opened_page].configure(state='disabled')

class DbaseTableSummary(ctk.CTkFrame):
    def __init__(self, parent, dbname, tablename):
        super().__init__(master = parent)

        # data
        self.table = tablename
        self.columns = get_table_content(dbname, tablename)
        self.grid_row_counter = 0

        # font
        columnfont = ctk.CTkFont(family = MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                                 size = DBSUMMARY_TSIZE)


        if self.columns['Columns']:
            self.rowconfigure(list(range(len(self.columns['Columns'])+1)), weight=1, uniform='visualize')

            ctk.CTkLabel(self, text = self.table, font = columnfont).grid(row = 0, column = 0)
            self.grid_row_counter += 2
            for columns in self.columns['Columns']:
                ctk.CTkLabel(self, text=columns).grid(row=self.grid_row_counter, column=0, ipadx = 30, sticky = 'nsew')
                self.grid_row_counter += 1

        else:
            self.rowconfigure(0, weight=1, uniform='visualize')

            ctk.CTkLabel(self, text=self.table, font = columnfont).grid(row=0, column=0, ipadx = 30, sticky = 'nsew') # működik, gyakorlatilag.


class databasePage(ctk.CTkFrame):
    def __init__(self, parent, dbase_name_var):
        super().__init__(master = parent)

        # layout
        self.columnconfigure(0, weight = 1, uniform = 'databasepage')
        self.columnconfigure(1, weight = 3, uniform = 'databasepage')
        self.columnconfigure(2, weight = 1, uniform = 'databasepage')
        self.rowconfigure((0,1), weight = 1, uniform = 'databasepage')

        # data
        self.dbase_name_var = dbase_name_var
        self.creation_time_var = ctk.StringVar()
        self.numoftables = ctk.StringVar()
        #self.kezdo_adatbazismegjelenito = 'NyissmegegyAdatbázist'

        self.tables_list = ''
        self.grid_row_number = 0
        self.grid_column_number_leftover = 0

        self.placed_table_visualize_objects = []

        # fonts
        labelekcimfontja = ctk.CTkFont(family = MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                                       size = LABELCIMSIZE)
        bodyfont = ctk.CTkFont(family = MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                                  size = LABELBODYSIZE)

        if self.dbase_name_var.get() != 'Nyiss meg egy Adatbázist':
            path = os.getcwd() + '\\' + 'Databases' + '\\' + self.dbase_name_var.get()
            ctime = str(datetime.fromtimestamp(os.path.getctime(path)))

            tables = len(get_current_database_tables(self.dbase_name_var.get()))

            self.creation_time_var.set(f'Keletkezési ideje\n{ctime.split()[0]} {ctime.split()[1].split(".")[0]}')
            self.numoftables.set(f'Táblák száma: {tables}')
        else:
            self.creation_time_var.set('Keletkezési ideje\nNyiss meg egy Adatbázist')
            self.numoftables.set('Táblák száma\nNyiss meg egy Adatbázist')

        # trace
        dbase_name_var.trace('w', self.update_datas)

        # widgets
        info_keret = ctk.CTkFrame(self)
        self.adatbazisTablaFrame = ctk.CTkFrame(self)
        erdekesseg_keret = ctk.CTkFrame(self)
        tipp_keret = ctk.CTkFrame(self)
        kukucs_keret = ctk.CTkFrame(self)

        alap_info_cim = ctk.CTkLabel(info_keret, text = 'Információk', font = labelekcimfontja)
        keszitesi_ido = ctk.CTkLabel(info_keret, textvariable = self.creation_time_var, font = bodyfont)
        tablak_szama = ctk.CTkLabel(info_keret, textvariable = self.numoftables, font = bodyfont)

        self.tablaobject_create()

        erdekesseg_cim = ctk.CTkLabel(erdekesseg_keret, text = 'Érdekességek', font = labelekcimfontja)
        erdekesseg1Label = ctk.CTkLabel(erdekesseg_keret, text = 'A forráskód\n sorainak száma:\n2485', font = bodyfont)

        tipp_cim = ctk.CTkLabel(tipp_keret, text = 'Tippek', font = labelekcimfontja)
        tipp1Label = ctk.CTkLabel(tipp_keret, text = 'A jobb oldali\n Segítség gombra\nkattintva megnyílik\negy segítség ablak!')
        tipp2Label = ctk.CTkLabel(tipp_keret, text = 'Jobb felső sarokban\ntudod beállítani\na neked tetsző megjelenési\nmódot.')
        tipp3Label = ctk.CTkLabel(tipp_keret, text = 'Bal felső sarokban\nlévő gombra kattintva\nújratöltheted az\negész alkalmazást.')

        kukucsLabel = ctk.CTkLabel(kukucs_keret, text = 'Pszt!', font = labelekcimfontja)
        kukucsLabel2 = ctk.CTkLabel(kukucs_keret, text = 'Elvileg az alkotóm\negy elavult modult használ!\n(customtkinter)\nMiközben már van egy\nmodernebb modul!\n(flet)')
        kukucslabel3 = ctk.CTkLabel(kukucs_keret, text = 'De azt is hallottam,\nhogy az alkotóm később\ntalálkozott a flettel,\nezért nem kockáztatott..')
        kukucslabel4 = ctk.CTkLabel(kukucs_keret, text = 'Engem hibáztass..\nne az alkotóm.\nÉn beszéltem rá. (hehe..)')

        # grid
        info_keret.grid(column = 0, row = 0, sticky = 'nsew', padx = 5, pady = 5)
        self.adatbazisTablaFrame.grid(column = 1, row = 0, rowspan = 2, sticky = 'nsew', padx = 5, pady = 5)
        erdekesseg_keret.grid(column = 0, row = 1, sticky = 'nsew', padx = 5, pady = 5)
        tipp_keret.grid(column = 2, row = 0, sticky = 'nsew', padx = 5, pady = 5)
        kukucs_keret.grid(column = 2, row = 1, sticky = 'nsew', padx = 5, pady = 5)

        alap_info_cim.pack()
        keszitesi_ido.pack(pady = 20)
        tablak_szama.pack(pady = 5)

        erdekesseg_cim.pack(pady = 5)
        erdekesseg1Label.pack(pady = 10)

        tipp_cim.pack()
        tipp1Label.pack(pady = 10)
        tipp2Label.pack(pady = 10)
        tipp3Label.pack(pady = 10)

        kukucsLabel.pack()
        kukucsLabel2.pack(pady = 5)
        kukucslabel3.pack(pady = 10)
        kukucslabel4.pack(pady = 10)


    def update_datas(self, *args):
        if self.placed_table_visualize_objects:
            for objects in self.placed_table_visualize_objects:
                objects.grid_forget()

        self.placed_table_visualize_objects = []

        self.tablaobject_create()

        if self.dbase_name_var.get() != 'Nyiss meg egy Adatbázist':
            path = os.getcwd() + '\\' + 'Databases' + '\\' + self.dbase_name_var.get()
            ctime = str(datetime.fromtimestamp(os.path.getctime(path)))

            tables = len(get_current_database_tables(self.dbase_name_var.get()))

            self.creation_time_var.set(f'Keletkezési ideje\n{ctime.split()[0]} {ctime.split()[1].split(".")[0]}')
            self.numoftables.set(f'Táblák száma: {tables}')

        else:
            self.creation_time_var.set('Keletkezési ideje\nNyiss meg egy Adatbázist!')
            self.numoftables.set('Táblák száma\nNyiss meg egy Adatbázist')

    def tablaobject_create(self):
        tableindex = 0
        if self.dbase_name_var.get() != 'Nyiss meg egy Adatbázist':

            self.tables_list = get_current_database_tables(self.dbase_name_var.get())
            self.grid_row_number = len(self.tables_list) // 3 if len(self.tables_list) // 3 >= 1 else 0
            self.grid_column_number_leftover = len(self.tables_list) % 3

            self.adatbazisTablaFrame.columnconfigure(list(range(3)), weight=1, uniform='visualizeTables') # , weight=1, uniform='visualizeTables'
            self.adatbazisTablaFrame.rowconfigure(list(range(self.grid_row_number)) or 0, weight=1, uniform='visualizeTables')

            stickyness = '' #if len(self.tables_list) < 6 else 'ew'

            if self.tables_list:
                if self.grid_column_number_leftover == 0:  # ha mindegyik sort fullra betudjuk tölteni. pl.: 2 sor 6 oszlop
                    for row in range(self.grid_row_number):
                        for column in range(3):
                            objekt = DbaseTableSummary(parent=self.adatbazisTablaFrame, dbname=self.dbase_name_var.get(),
                                                   tablename=self.tables_list[tableindex][:-4])
                            objekt.grid(column=column, row=row, sticky = stickyness, padx=5, pady=5)

                            tableindex += 1

                            self.placed_table_visualize_objects.append(objekt)

                else:  # ha nem tudunk betölteni minden sort. pl.: 2 sor, 5 oszlop
                    for row in range(self.grid_row_number):
                        if row == self.grid_row_number:
                            break
                        for column in range(3):
                            objekt = DbaseTableSummary(parent=self.adatbazisTablaFrame, dbname=self.dbase_name_var.get(),
                                                       tablename=self.tables_list[tableindex][:-4])
                            objekt.grid(column=column, row=row, sticky = stickyness, padx=5, pady=5)

                            tableindex += 1

                            self.placed_table_visualize_objects.append(objekt)


                    for column in range(self.grid_column_number_leftover):
                        objekt = DbaseTableSummary(parent=self.adatbazisTablaFrame, dbname=self.dbase_name_var.get(),
                                                       tablename=self.tables_list[tableindex][:-4])
                        objekt.grid(column=column, row=self.grid_row_number,  sticky = stickyness, padx=5, pady=5)

                        tableindex += 1
                        self.placed_table_visualize_objects.append(objekt)


class tablePageTableSection(ctk.CTkFrame):
    def __init__(self, parent, tablename, buttonCommand):
        super().__init__(master = parent, fg_color=DBLIST_LIST_BGCOLOR)

        # layout
        self.rowconfigure(0, weight = 1, uniform = 'tablePageTableSection')
        self.columnconfigure((0,1), weight = 1, uniform = 'tablePageTableSection')

        # font
        cimfont = ctk.CTkFont(family = MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                              size = AVERAGE_BUTTON_TSIZE-2)

        # widgets
        nameLabel = ctk.CTkLabel(self,
                                 text = tablename,
                                 fg_color = LIGHTER_BGCOLOR,
                                 corner_radius = 5,
                                 font = cimfont)
        openButton = ctk.CTkButton(self,
                                   text = 'Open',
                                   command = lambda: buttonCommand(tablename),
                                   fg_color = DBLIST_LIST_BTN_BG_COLOR,
                                   hover_color = AVERAGE_BUTTON_HOVER_COLOR,
                                   text_color = AVERAGE_BUTTON_TCOLOR,
                                   font = ctk.CTkFont(family = MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                                                      size = TABLEFRAME_DATASIZE))

        # grid
        nameLabel.grid(row = 0, column = 0, sticky = 'nsew', padx = 5, pady = 5)
        openButton.grid(row = 0, column = 1, sticky = 'nsew', padx = 5, pady = 5)


class tablePagePopup(ctk.CTkFrame):
    def __init__(self, parent, operation, dbase_var, last_row_var, section_dict, reload_func, button_func):
        super().__init__(master = parent, fg_color=DBLIST_POPUP_BG_COLOR)

        # data
        self.tablanev_var = ctk.StringVar()
        self.dbase_var = dbase_var
        self.parent = parent
        self.reload_func = reload_func
        self.button_func = button_func

        # fonts
        cimFont = ctk.CTkFont(family = MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                              size = TABLESPOPUPCIM_TSIZE)

        dbnameFont = ctk.CTkFont(family=MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                             size=TABLESPOPUPCIM_TSIZE-2)

        btnFont = ctk.CTkFont(family = AVERAGE_BUTTON_FAMILY,
                              size = AVERAGE_BUTTON_TSIZE)

        self.tablepopupname = ctk.CTkLabel(self, text=f'Tábla {operation}', font = cimFont)
        self.tablanev = ctk.CTkLabel(self, textvariable=self.tablanev_var, font = dbnameFont)
        self.tableinput_entry = ctk.CTkEntry(self, textvariable=self.tablanev_var, font = dbnameFont)
        self.tablecreate_btn = ctk.CTkButton(self,
                                             text=operation[:-1],
                                             command = lambda: self.feladatvegzes(operation = operation,
                                                                                  tablanev_var = self.tablanev_var),
                                             fg_color = TABLEPOPUPBTN_BG_COLOR,
                                             hover_color = AVERAGE_BUTTON_HOVER_COLOR,
                                             text_color = AVERAGE_BUTTON_TCOLOR,
                                             font = btnFont)

        self.statusz = ctk.CTkLabel(self, text='Státusz\nParancsra várás')

        self.tablepopupname.pack(side = 'top', pady = 20)
        self.tablanev.pack(side = 'top', pady = 10)
        self.tableinput_entry.pack(side = 'top')
        self.tablecreate_btn.pack(side = 'top', pady = 10)
        self.statusz.pack(side = 'bottom')

    def feladatvegzes(self, operation, tablanev_var):
        if operation == 'Létrehozása':
            if self.dbase_var.get() != 'Nyiss meg egy Adatbázist':
                if tablanev_var.get() + '.txt' in get_current_database_tables(self.dbase_var.get()):
                    self.statusz.configure(text=f'Státusz\nSikertelen Tábla létrehozás!\n(Ez a tábla már létezik!)')
                    return

                elif len(tablanev_var.get()) == 0 or len(tablanev_var.get()) == tablanev_var.get().count(' '):
                    self.statusz.configure(text=f'Státusz\nSikertelen Tábla létrehozás!\n(Üres táblanév!)')
                    return

                elif len(tablanev_var.get().split()) > 1:
                    self.statusz.configure(text=f'Státusz\nSikertelen Tábla létrehozás!\nNe használj szóközöket!')
                    return

                elif create_table(database_name = self.dbase_var.get(), table_name = tablanev_var.get()) == 'Siker':
                    tablePageTableSection(parent = self.parent, tablename = tablanev_var.get(), buttonCommand = self.button_func)


                    self.statusz.configure(text=f'Státusz\nSikeres Tábla létrehozás!\n({self.dbase_var.get()} -> {tablanev_var.get()})')
                    self.reload_func()
                    return

            elif self.dbase_var.get() == 'Nyiss meg egy Adatbázist':
                self.statusz.configure(text=f'Státusz\nSikertelen Tábla létrehozás!\n(Nyiss meg egy Adatbázist)')
                return

        elif operation == 'Törlése':
            if self.dbase_var.get() != 'Nyiss meg egy Adatbázist':
                if tablanev_var.get() + '.txt' in get_current_database_tables(self.dbase_var.get()):
                    if delete_table(database_name = self.dbase_var.get(), table_name = tablanev_var.get()) == 'Siker':
                        self.statusz.configure(text=f'Státusz\nSikeres tábla törlés!\n({self.dbase_var.get()} -> {tablanev_var.get()})')

                        self.reload_func()
                        return

                elif len(tablanev_var.get()) == 0 or len(tablanev_var.get()) == tablanev_var.get().count(' '):
                    self.statusz.configure(text=f'Státusz\nSikertelen Tábla törlés!\n(Üres táblanév!)')
                    return

                else:
                    self.statusz.configure(text=f'Státusz\nSikertelen tábla törlés!\n(Ez a tábla nem létezik!)')
                    return

            elif self.dbase_var.get() == 'Nyiss meg egy Adatbázist':
                self.statusz.configure(text=f'Státusz\nSikertelen Tábla törlés!\n(Nyiss meg egy Adatbázist)')
                return

class tablePage(ctk.CTkFrame):
    def __init__(self, parent, dbase_name_var):
        super().__init__(master = parent)

        # layout
        self.columnconfigure(0, weight = 1, uniform = 'tablePage')
        self.columnconfigure(1, weight = 2, uniform = 'tablePage')
        self.columnconfigure(2, weight = 1, uniform = 'tablePage')

        self.rowconfigure(0, weight = 5, uniform = 'tablePage')
        self.rowconfigure(1, weight = 1, uniform = 'tablePage')

        # data
        self.dbase_name_var = dbase_name_var
        self.previous_dbase = self.dbase_name_var.get()
        self.last_row_section_placed = ctk.IntVar(value = 0)
        self.placed_table_sections = {}
        self.table_content = None
        self.col_number = ctk.StringVar()
        self.record_number = ctk.StringVar()

        # trace
        self.dbase_name_var.trace('w', self.update_datas)

        # widget-frames
        self.tablesFrame = ctk.CTkFrame(self)
        self.tablesFrame.rowconfigure((list(range(10))), weight = 1, uniform = 'innerTableFrame')
        self.tablesFrame.columnconfigure(0, weight = 1, uniform = 'innerTableFrame')

        self.tableCreateFrame = ctk.CTkFrame(self)
        self.tableCreateFrame.rowconfigure(list(range(6)), weight = 1, uniform = 'innerTableCreateFrame')
        self.tableCreateFrame.columnconfigure((0, 1), weight = 1, uniform = 'innerTableCreateFrame')

        # style
        style = ttk.Style()
        style.configure("Treeview", highlightthickness=0, bd=0,font=('Calibri', 11))
        style.configure("Treeview.Heading", font=('Calibri', 13, 'bold'))

        # fonts
        adatfont = ctk.CTkFont(family = MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                               size = TABLEFRAME_DATASIZE)

        exitButtonFont = ctk.CTkFont(family = AVERAGE_BUTTON_FAMILY,
                                     size = AVERAGE_BUTTON_TSIZE)

        # widgets
        self.tablatartalom_treeview = None

        self.createTableBtnPopup = ctk.CTkButton(self.tableCreateFrame,
                                                 text = '+',
                                                 command = lambda: self.show_table_popup(operation = 'Létrehozása'),
                                                 fg_color = AVERAGE_BUTTON_BG_COLOR,
                                                 hover_color = AVERAGE_BUTTON_HOVER_COLOR,
                                                 text_color = AVERAGE_BUTTON_TCOLOR,
                                                 font = adatfont)

        self.deleteTableBtnPopup = ctk.CTkButton(self.tableCreateFrame,
                                                 text = 'Del',
                                                 command = lambda: self.show_table_popup(operation = 'Törlése'),
                                                 fg_color=AVERAGE_BUTTON_BG_COLOR,
                                                 hover_color=AVERAGE_BUTTON_HOVER_COLOR,
                                                 text_color=AVERAGE_BUTTON_TCOLOR,
                                                 font=adatfont)

        self.col_number_label = ctk.CTkLabel(self.tableCreateFrame, textvariable=self.col_number, font = adatfont)
        self.record_number_label = ctk.CTkLabel(self.tableCreateFrame, textvariable=self.record_number, font = adatfont)

        self.exitTableBtnPopup = ctk.CTkButton(self,
                                               text = 'X',
                                               command = self.exit_table_popup,
                                               fg_color = TABLESEXITBTN_BGCOLOR,
                                               hover_color = AVERAGE_BUTTON_HOVER_COLOR,
                                               text_color = AVERAGE_BUTTON_TCOLOR,
                                               font = exitButtonFont)

        self.tablatartalom_treeview = ttk.Treeview(self,
                                                   columns=[],
                                                   show='headings')

        # treeview scrollbars

        self.scrollbary = ctk.CTkScrollbar(self,
                                           orientation=tk.VERTICAL,
                                           command=self.tablatartalom_treeview.yview,
                                           width = 20,
                                           fg_color = SCROLLBAR_BGCOLOR)

        self.scrollbarx = ctk.CTkScrollbar(self,
                                           orientation=tk.HORIZONTAL,
                                           command=self.tablatartalom_treeview.xview,
                                           width = 20,
                                           fg_color = SCROLLBAR_BGCOLOR)

        # treeview scrollbars configure
        self.tablatartalom_treeview.configure(yscrollcommand=self.scrollbary.set)
        self.tablatartalom_treeview.configure(xscrollcommand=self.scrollbarx.set)


        self.notify_when_empty = ctk.CTkLabel(self, text='Üres Tábla!')

        # frames-grid
        self.tablesFrame.grid(column = 0, row = 0, rowspan = 2, sticky = 'nsew', padx = 5, pady = 5)
        self.tableCreateFrame.grid(column = 2, row = 0, rowspan = 2, sticky = 'nsew', padx = 5, pady = 5)

        # widgets-grid
        self.createTableBtnPopup.grid(column = 1, row = 0, sticky = 'nsew', padx = 20, pady = 20)
        self.deleteTableBtnPopup.grid(column = 0, row = 0, sticky = 'nsew', padx = 20, pady = 20)

    def update_datas(self, *args):
        self.db_change_logic()

    def db_change_logic(self):
        self.scrollbary.grid_forget()
        self.scrollbarx.grid_forget()
        self.tablatartalom_treeview.grid_forget()
        self.notify_when_empty.grid_forget()
        self.col_number_label.grid_forget()
        self.record_number_label.grid_forget()

        if self.placed_table_sections:
            for name, object in self.placed_table_sections.items():
                object.grid_forget()

        self.last_row_section_placed.set(0)
        if self.dbase_name_var.get() != 'Nyiss meg egy Adatbázist':
            if len(get_current_database_tables(self.dbase_name_var.get())) > 0:
                if self.previous_dbase != self.dbase_name_var.get():
                    for name, section in self.placed_table_sections.items():
                        section.grid_forget()

                    self.last_row_section_placed.set(0)
                    self.previous_dbase = self.dbase_name_var.get()

                for tablenames in get_current_database_tables(self.dbase_name_var.get()):
                    section = tablePageTableSection(parent=self.tablesFrame,
                                                    tablename=tablenames[:-4],
                                                    buttonCommand=self.set_treeview)

                    section.grid(column=0, row=self.last_row_section_placed.get())
                    self.placed_table_sections[tablenames] = section

                    self.last_row_section_placed.set(self.last_row_section_placed.get()+1)
            else:
                for name, section in self.placed_table_sections.items():
                    section.grid_forget()
                    self.last_row_section_placed.set(0)
        else:
            for name, section in self.placed_table_sections.items():
                section.grid_forget()

            self.last_row_section_placed.set(0)

    def show_table_popup(self, operation):
        self.exit_table_popup()

        self.table_popup = tablePagePopup(parent = self,
                                          operation = operation,
                                          last_row_var = self.last_row_section_placed,
                                          section_dict = self.placed_table_sections,
                                          dbase_var = self.dbase_name_var,
                                          reload_func = self.db_change_logic,
                                          button_func = self.set_treeview)

        self.table_popup.place(relx = 0.763, rely = 0.15, relwidth = 0.228, relheight = 0.45)
        self.exitTableBtnPopup.place(relx = 0.94, rely = 0.15, relwidth = 0.05, relheight = 0.05)

        self.exitTableBtnPopup.lift()

    def set_treeview(self, tablename):
        self.table_content = get_table_content(database_name = self.dbase_name_var.get(),
                                               table_name= tablename)

        self.scrollbary.grid_forget()
        self.scrollbarx.grid_forget()
        self.tablatartalom_treeview.grid_forget()

        for item in self.tablatartalom_treeview.get_children():
            self.tablatartalom_treeview.delete(item)

        if self.table_content['Columns']: # ha van tartalom a táblában
            self.notify_when_empty.grid_forget()

            # additional widgets
            self.col_number.set(f'Oszlop szám: {len(self.table_content["Columns"])}')
            self.record_number.set(f'Rekord szám: {len(self.table_content["Content"])}')

            self.tablatartalom_treeview.configure(columns = self.table_content['Columns'])

            maxlen_columns = {name: 0 for name in self.table_content['Columns']}
            for column in self.table_content['Columns']:  # kiszámoljuk, mennyi szélesség kell, hogy kiférjenek a karakterek
                for content in self.table_content['Content']:
                    for index, check in enumerate(content):
                        if maxlen_columns[self.table_content['Columns'][index]] < len(check):
                            maxlen_columns[self.table_content['Columns'][index]] = len(check)

                self.tablatartalom_treeview.heading(column, text = column)
                if len(column) > maxlen_columns[column]:
                    self.tablatartalom_treeview.column(column, width = 10+len(column)*10, anchor = tk.CENTER)

                else:
                    self.tablatartalom_treeview.column(column, width = 10+maxlen_columns[column]*10, anchor = tk.CENTER)

            if self.table_content['Content']:
                for content in self.table_content['Content']:
                    self.tablatartalom_treeview.insert('', tk.END, values = content)

            # grid
            self.tablatartalom_treeview.grid(column = 1, row = 0, rowspan = 2, sticky = 'nsew', padx = 30, pady = 30)
            self.scrollbary.grid(column=1, row=0, rowspan=2, sticky='nse', pady = 5)
            self.scrollbarx.grid(column=1, row=0, rowspan=2, sticky='ews', padx = 5)

            self.col_number_label.grid(column=0, columnspan=2, row=4)
            self.record_number_label.grid(column=0, columnspan=2, row=5)

        else:
            self.col_number.set(f'Column number: 0')
            self.record_number.set(f'Record number: 0')

            self.col_number_label.grid(column=0, columnspan=2, row=4)
            self.record_number_label.grid(column=0, columnspan=2, row=5)
            self.notify_when_empty.grid(column = 1, row = 0, rowspan = 2)

    def exit_table_popup(self):
        try:
            self.table_popup.place_forget()
            self.exitTableBtnPopup.place_forget()
        except:
            pass


class datamanipulation_manipulateFrame(ctk.CTkFrame):
    def __init__(self, parent, cim, buttonfunc = None, entryvar = None, sorvar=None, oszlopvar=None, changevar=None):
        super().__init__(master = parent, fg_color = DBLIST_LIST_BGCOLOR)
        self.rowconfigure((0, 1, 2, 3), weight = 1)
        self.columnconfigure(0, weight = 1)

        # data
        milyenstring = '(Adatok)' if cim == 'Sor Hozzáadása' else '(Sornak a száma)' if cim == 'Sor Törlése' else '(Oszlopnév)'

        # fonts
        cimfont = ctk.CTkFont(family = MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                              size = 20)

        milyenfont = ctk.CTkFont(family = MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                                 size = 18)


        # widgets
        if cim != 'Sor/Rekord szerkesztése':
            cimLabel = ctk.CTkLabel(self, text = cim, font = cimfont)
            milyenadatLabel = ctk.CTkLabel(self, text = milyenstring, font = milyenfont)
            dataEntry = ctk.CTkEntry(self, textvariable = entryvar)
            submitButton = ctk.CTkButton(self,
                                         text = 'Mehet!',
                                         command = buttonfunc,
                                         fg_color = AVERAGE_BUTTON_BG_COLOR,
                                         hover_color = AVERAGE_BUTTON_HOVER_COLOR,
                                         text_color = AVERAGE_BUTTON_TCOLOR,
                                         font = milyenfont)

            # pack
            cimLabel.grid(column = 0, row = 0)
            milyenadatLabel.grid(column = 0, row = 1)
            dataEntry.grid(column = 0, row = 2)
            submitButton.grid(column = 0, row = 3)

        else:
            cimLabel = ctk.CTkLabel(self, text=cim, font = cimfont)

            sorFrame = ctk.CTkFrame(self)

            # layout
            sorFrame.rowconfigure((0,1,2,3), weight = 1, uniform = 'innersorframeke')
            sorFrame.columnconfigure((0,1,2), weight = 1, uniform = 'innersorframeke')

            soradatLabel = ctk.CTkLabel(sorFrame, text='  (oszlop neve)', font = milyenfont)
            oszlopadatLabel = ctk.CTkLabel(sorFrame, text='(sornak a száma)', font = milyenfont)
            dataadatLabel = ctk.CTkLabel(sorFrame, text='(adat)   ', font = milyenfont)

            oszlopEntry = ctk.CTkEntry(sorFrame, textvariable=oszlopvar)
            sorEntry = ctk.CTkEntry(sorFrame, textvariable=sorvar)
            dataEntry = ctk.CTkEntry(sorFrame, textvariable=changevar)

            submitButton = ctk.CTkButton(self,
                                         text='Mehet!',
                                         command=buttonfunc,
                                         fg_color=AVERAGE_BUTTON_BG_COLOR,
                                         hover_color=AVERAGE_BUTTON_HOVER_COLOR,
                                         text_color=AVERAGE_BUTTON_TCOLOR,
                                         font=milyenfont)

            # pack
            cimLabel.grid(column = 0, row = 0)

            sorFrame.grid(column = 0, row = 1, sticky = 'ew')
            soradatLabel.grid(column = 0, row = 1)
            oszlopadatLabel.grid(column = 1, row = 1)
            dataadatLabel.grid(column = 2, row = 1)

            oszlopEntry.grid(column = 0, row = 3)
            sorEntry.grid(column = 1, row = 3)
            dataEntry.grid(column = 2, row = 3)

            submitButton.grid(column = 0, row = 3)


class datamanipulationPage(ctk.CTkFrame):
    def __init__(self, parent, dbase_name_var):
        super().__init__(master = parent)

        # layout
        self.columnconfigure(0, weight = 1, uniform = 'main_datamanipulation')
        self.columnconfigure(1, weight = 3, uniform = 'main_datamanipulation')
        self.columnconfigure(2, weight = 1, uniform = 'main_datamanipulation')

        self.rowconfigure((0,1,2,3), weight = 1, uniform = 'main_datamanipulation')

        # data
        self.dbase_name_var = dbase_name_var
        self.choosed_table_var = ctk.StringVar(value = 'Nyiss meg egy Adatbázist')
        self.tables_avaliable = []
        self.statuszcheck = ctk.StringVar(value = 'Státusz\nParancsra várás')

        self.addline_var = ctk.StringVar()
        self.removeline_var = ctk.StringVar()
        self.addcolumn_var = ctk.StringVar()
        self.removecolumn_var = ctk.StringVar()

        self.sormanOszlop_var = ctk.StringVar()
        self.sormanSor_var = ctk.StringVar()
        self.sormanAdat_var = ctk.StringVar()

        self.sorokszama = ctk.StringVar(value = 'Rekordok/Sorok száma\n?')
        self.oszlopokszama = ctk.StringVar(value = 'Oszlopok száma\n?')

        # trace
        dbase_name_var.trace('w', self.update_manipulation_datas)
        self.choosed_table_var .trace('w', self.small_update)

        # fonts
        cimfont = ctk.CTkFont(family = MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                              size = DMANIPULATETITLESIZE)

        optionmenufont = ctk.CTkFont(family = MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                                     size = OPTIONMENU_TSIZE)

        statuszfont = ctk.CTkFont(family = MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                                  size = STATUSZSIZE)

        adatfont = ctk.CTkFont(family = MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                               size = ADATOKSIZE)

        tippfont = ctk.CTkFont(family = MAINWINDOW_SELECTED_DBTEXT_FAMILY, weight = 'bold')

        # widgets
        self.optionmenu = ctk.CTkOptionMenu(self,
                                            values=self.tables_avaliable,
                                            variable=self.choosed_table_var,
                                            fg_color = OPTIONMENU_FGCOLOR,
                                            text_color = OPTIONMENU_TCOLOR,
                                            button_color = OPTIONMENU_NYILFGCOLOR,
                                            font = optionmenufont)

        self.table_name_label = ctk.CTkLabel(self,textvariable = self.choosed_table_var, font = cimfont)

        self.statusz_label = ctk.CTkLabel(self, textvariable = self.statuszcheck, font = statuszfont)

        self.sorhozzaadWidget = datamanipulation_manipulateFrame(parent = self,
                                                                 cim = 'Sor Hozzáadása',
                                                                 entryvar = self.addline_var,
                                                                 buttonfunc = self.lineadd_ellenorzo)
        self.sortorlesWidget = datamanipulation_manipulateFrame(parent=self,
                                                                cim='Sor Törlése',
                                                                entryvar=self.removeline_var,
                                                                buttonfunc=self.lineremove_ellenorzo)

        self.oszlophozzaadWidget = datamanipulation_manipulateFrame(parent = self,
                                                                    cim = 'Oszlop Hozzáadása',
                                                                    entryvar=self.addcolumn_var,
                                                                    buttonfunc=self.coloumnadd_ellenorzo)
        self.oszloptorlesWidget = datamanipulation_manipulateFrame(parent=self,
                                                                   cim='Oszlop Törlése',
                                                                   entryvar=self.removecolumn_var,
                                                                   buttonfunc=self.coloumnremove_ellenorzo)

        self.sormanipulacioWidget = datamanipulation_manipulateFrame(parent = self,
                                                                     cim = 'Sor/Rekord szerkesztése',
                                                                     sorvar = self.sormanSor_var,
                                                                     oszlopvar = self.sormanOszlop_var,
                                                                     changevar = self.sormanAdat_var,
                                                                     buttonfunc = self.sor_manipulacio_ellenorzo)

        self.sorszamLabel = ctk.CTkLabel(self, textvariable = self.sorokszama, font = adatfont)
        self.oszlopszamLabel = ctk.CTkLabel(self, textvariable = self.oszlopokszama, font = adatfont)

        self.tippFrame = ctk.CTkFrame(self)

        self.tippLabel = ctk.CTkLabel(self.tippFrame, text='Tipp', font = tippfont)
        self.tippKontent = ctk.CTkLabel(self.tippFrame,
                                        text='Ha sortörléshez, vagy\nsormanipulácóhoz\na sorhoz nullát írsz,\nakkor az az utolsó\n sort fogja jelenteni.',
                                        font = tippfont)

        # grid
        self.optionmenu.grid(column = 0, row = 0, sticky = 'n', pady = 10)
        self.table_name_label.grid(column = 1, row = 0)

        self.sorhozzaadWidget.grid(column = 0, row = 1, sticky = 'nsew', padx = 5, pady = 5)
        self.sortorlesWidget.grid(column = 0, row = 2, sticky = 'nsew', padx = 5, pady = 5)

        self.oszlophozzaadWidget.grid(column = 2, row = 1, sticky = 'nsew', padx = 5, pady = 5)
        self.oszloptorlesWidget.grid(column = 2, row = 2, sticky = 'nsew', padx = 5, pady = 5)

        self.sormanipulacioWidget.grid(column = 1, row = 2, rowspan = 2, sticky = 'nsew')

        self.statusz_label.grid(column = 1, row = 1)

        self.sorszamLabel.grid(column = 0, row = 3)
        self.oszlopszamLabel.grid(column = 2, row = 3)

        self.tippFrame.grid(row = 0, column = 2, sticky = 'nsew', padx= 5, pady = 5)
        self.tippLabel.pack()
        self.tippKontent.pack()


    def small_update(self, *args):
        if self.choosed_table_var.get() not in ['', 'Nyiss meg egy Adatbázist']:
            datas = get_table_content(self.dbase_name_var.get(), self.choosed_table_var.get())

            self.sorokszama.set(f'Rekordok/Sorok száma\n{len(datas["Content"])}')
            self.oszlopokszama.set(f'Oszlopok száma\n{len(datas["Columns"])}')

    def update_manipulation_datas(self, *args):
        self.tables_avaliable = []

        self.addline_var.set('')
        self.removeline_var.set('')
        self.addcolumn_var.set('')
        self.removecolumn_var.set('')

        self.sormanOszlop_var.set('')
        self.sormanSor_var.set('')
        self.sormanAdat_var.set('')

        self.choosed_table_var.set('')
        self.statuszcheck.set('Státusz\nParancsra várás')

        if self.dbase_name_var.get() != 'Nyiss meg egy Adatbázist':
            for prettify in get_current_database_tables(self.dbase_name_var.get()):
                self.tables_avaliable.append(prettify[:-4])

        else:
            self.tables_avaliable = []
            self.choosed_table_var.set('Nyiss meg egy Adatbázist')

            self.sorokszama.set(f'Rekordok/Sorok száma\n?')
            self.oszlopokszama.set(f'Oszlopok száma\n?')

        self.optionmenu.configure(values = self.tables_avaliable)

    def lineadd_ellenorzo(self):
        if len(self.addline_var.get()) < 1:
            self.statuszcheck.set('Státusz\nSikertelen sorbeillesztés!\nÜres sort nem tudsz beilleszteni.')
            return

        if len(self.addline_var.get()) >= 1:
            if self.dbase_name_var.get() != 'Nyiss meg egy Adatbázist':
                if self.choosed_table_var.get():
                    maxcol = get_table_content(self.dbase_name_var.get(), self.choosed_table_var.get())
                    if maxcol['Columns']:
                        if len(self.addline_var.get().split()) <= len(maxcol['Columns']):
                            if tablecontent_record_manipulation(database_name=self.dbase_name_var.get(),
                                         table_name=self.choosed_table_var.get(),
                                         input_line=self.addline_var.get(),
                                         operation='add') == 'Siker':
                                self.statuszcheck.set(f'Státusz\nSikeres sorbeillesztés!\nSort illesztettél be itt: {self.choosed_table_var.get()} | Adatok: {self.addline_var.get()}\nAhhoz, hogy lásd az eredményt: Táblák szekcióban nyisd meg a táblát.\nHa megvan nyitva az adott tábla, nyisd meg újra.')
                                datas = get_table_content(self.dbase_name_var.get(), self.choosed_table_var.get())

                                self.sorokszama.set(f'Rekordok/Sorok száma\n{len(datas["Content"])}')
                        else:
                            self.statuszcheck.set('Státusz\nSikertelen sorbeillesztés!\nTöbb adatot adtál meg, mint ahány oszlop van!\nHa space-t írsz, az olyan, mintha több oszlopnyi adatot adsz meg!\n(oszlopadat1 oszlopadat2.)\nHelyette használj _ jelet. (oszlop_adat1 oszlop_adat2)')
                    else:
                        self.statuszcheck.set('Státusz\nSikertelen sorbeillesztés!\nNincs oszlop!')
                else:
                    self.statuszcheck.set('Státusz\nSikertelen sorbeillesztés!\nNyiss meg egy táblát!')
            else:
                self.statuszcheck.set('Státusz\nSikertelen sorbeillesztés!\nNyiss meg egy Adatbázist!')

        self.addline_var.set('')
        self.removeline_var.set('')
        self.addcolumn_var.set('')
        self.removecolumn_var.set('')

        self.sormanOszlop_var.set('')
        self.sormanSor_var.set('')
        self.sormanAdat_var.set('')

    def lineremove_ellenorzo(self):
        if len(self.removeline_var.get()) >= 1 or self.removeline_var.get().count(' ') != len(self.removeline_var.get()):
            if self.dbase_name_var.get() != 'Nyiss meg egy Adatbázist':
                if self.choosed_table_var.get():
                    maxrow = get_table_content(self.dbase_name_var.get(), self.choosed_table_var.get())
                    if maxrow['Columns']:
                        if self.removeline_var.get().isnumeric():
                            if int(self.removeline_var.get()) <= len(maxrow['Content']):
                                if tablecontent_record_manipulation(database_name=self.dbase_name_var.get(),
                                                        table_name=self.choosed_table_var.get(),
                                                        input_line=self.removeline_var.get(),
                                                        operation='del') == 'Siker':
                                    self.statuszcheck.set(f'Státusz\nSikeres sortörlés!\nTörölted a(z) {self.removeline_var.get()+"." if self.removeline_var.get() != "0" else "utolsó"} sort itt: {self.choosed_table_var.get()}\nAhhoz, hogy lásd az eredményt:\nTáblák szekcióban nyisd meg a táblát.\nHa megvan nyitva az adott tábla, nyisd meg újra.')

                                    datas = get_table_content(self.dbase_name_var.get(), self.choosed_table_var.get())

                                    self.sorokszama.set(f'Rekordok/Sorok száma\n{len(datas["Content"])}')

                            else:
                                self.statuszcheck.set(f'Státusz\nSikertelen sortörlés!\nNagyobb számot adtál meg, mint ahány sor van!\n(Utolsó sor: {len(maxrow["Content"])})')
                        else:
                            self.statuszcheck.set(f'Státusz\nSikertelen sortörlés!\nSorszámnak számot adj meg!')
                    else:
                        self.statuszcheck.set(f'Státusz\nSikertelen sortörlés!\nNincs oszlop, tehát sor sincs!')
                else:
                    self.statuszcheck.set(f'Státusz\nSikertelen sortörlés!\nNyiss meg egy táblát!')
            else:
                self.statuszcheck.set(f'Státusz\nSikertelen sortörlés!\nNyiss meg egy Adatbázist!')
        else:
            self.statuszcheck.set('Státusz\nSikertelen sortörlés!\nNem adtál meg sorszámot!')

        self.addline_var.set('')
        self.removeline_var.set('')
        self.addcolumn_var.set('')
        self.removecolumn_var.set('')

        self.sormanOszlop_var.set('')
        self.sormanSor_var.set('')
        self.sormanAdat_var.set('')

    def coloumnadd_ellenorzo(self):
        if len(self.addcolumn_var.get()) < 1 or self.addcolumn_var.get().count(' ') == len(self.addcolumn_var.get()):
            self.statuszcheck.set('Státusz\nSikertelen oszlopbeillesztés!\nÜres oszlopot nem tudsz beilleszteni.')
            return

        elif len(self.addcolumn_var.get()) >= 1 and self.choosed_table_var.get():
            if self.dbase_name_var.get() == 'Nyiss meg egy Adatbázist':
                self.statuszcheck.set('Státusz\nSikertelen oszlopbeillesztés!\nNyiss meg egy Adatbázist!')
                return

            cols = get_table_content(self.dbase_name_var.get(), self.choosed_table_var.get())['Columns']
            if self.addcolumn_var.get() in cols:
                self.statuszcheck.set('Státusz\nSikertelen oszlopbeillesztés!\nEz az oszlop már létezik!')
                return

            if len(self.addcolumn_var.get().split()) > 1:
                self.statuszcheck.set('Státusz\nSikertelen oszlopbeillesztés!\nSzóközök helyett használj egy kitöltő karaktert kérlek!\nPéldául: én_oszlopom')
                return


            if tablecontent_column_manipulation(database_name=self.dbase_name_var.get(),
                                         table_name=self.choosed_table_var.get(),
                                         column_name=self.addcolumn_var.get(),
                                         operation='add') == 'Siker':
                self.statuszcheck.set(f'Státusz\nSikeres oszlopbeillesztés!\n{self.addcolumn_var.get()} nevű oszlopot illesztettél be itt: {self.choosed_table_var.get()}\nAhhoz, hogy lásd az eredményt:\nTáblák szekcióban nyisd meg a táblát.\nHa megvan nyitva az adott tábla, nyisd meg újra.')

                datas = get_table_content(self.dbase_name_var.get(), self.choosed_table_var.get())

                self.oszlopokszama.set(f'Oszlopok száma\n{len(datas["Columns"])}')


        else:
            self.statuszcheck.set('Státusz\nSikertelen oszlopbeillesztés!\nNyiss meg egy táblát!')

        self.addline_var.set('')
        self.removeline_var.set('')
        self.addcolumn_var.set('')
        self.removecolumn_var.set('')

        self.sormanOszlop_var.set('')
        self.sormanSor_var.set('')
        self.sormanAdat_var.set('')

    def coloumnremove_ellenorzo(self):
        if len(self.removecolumn_var.get()) < 1 or self.removecolumn_var.get().count(' ') == len(self.removecolumn_var.get()):
            self.statuszcheck.set('Státusz\nSikertelen oszloptörlés!\nÜres oszlopot nem tudsz törölni.')
            return

        elif len(self.removecolumn_var.get()) >= 1 and self.choosed_table_var.get():
            if self.dbase_name_var.get() == 'Nyiss meg egy Adatbázist':
                self.statuszcheck.set('Státusz\nSikertelen oszloptörlés!\nNyiss meg egy Adatbázist!')
                return

            cols = get_table_content(self.dbase_name_var.get(), self.choosed_table_var.get())['Columns']
            if self.removecolumn_var.get() not in cols:
                self.statuszcheck.set('Státusz\nSikertelen oszloptörlés!\nEz az oszlop nem létezik!')
                return


            if tablecontent_column_manipulation(database_name=self.dbase_name_var.get(),
                                            table_name=self.choosed_table_var.get(),
                                            column_name=self.removecolumn_var.get(),
                                            operation='del') == 'Siker':
                self.statuszcheck.set(f'Státusz\nSikeres oszloptörlés!\n{self.removecolumn_var.get()} nevű oszlopot töröltél itt: {self.choosed_table_var.get()}\nAhhoz, hogy lásd az eredményt:\nTáblák szekcióban nyisd meg a táblát.\nHa megvan nyitva az adott tábla, nyisd meg újra.')

                datas = get_table_content(self.dbase_name_var.get(), self.choosed_table_var.get())

                self.oszlopokszama.set(f'Oszlopok száma\n{len(datas["Columns"])}')


        else:
            self.statuszcheck.set('Státusz\nSikertelen oszloptörlés!\nNyiss meg egy táblát!')

        self.addline_var.set('')
        self.removeline_var.set('')
        self.addcolumn_var.set('')
        self.removecolumn_var.set('')

        self.sormanOszlop_var.set('')
        self.sormanSor_var.set('')
        self.sormanAdat_var.set('')

    def sor_manipulacio_ellenorzo(self):
        if self.dbase_name_var.get() != 'Nyiss meg egy Adatbázist':
            if self.choosed_table_var.get():
                daata = get_table_content(self.dbase_name_var.get(), self.choosed_table_var.get())
                if self.sormanOszlop_var.get() in daata['Columns']:
                    if self.sormanSor_var.get():
                        if int(self.sormanSor_var.get()) <= len(daata['Content']):
                            if self.sormanAdat_var.get():
                                if len(self.sormanAdat_var.get().split()) == 1:

                                    if sorszerkeszto(database_name = self.dbase_name_var.get(),
                                             table_name = self.choosed_table_var.get(),
                                             sor = int(self.sormanSor_var.get()),
                                             column_name = self.sormanOszlop_var.get(),
                                             data = self.sormanAdat_var.get()) == 'Siker':
                                        self.statuszcheck.set(f'Státusz\nSikeres sorszerkesztés a(z) {self.sormanSor_var.get()+"." if self.sormanSor_var.get() != "0" else "utolsó"} soron. {self.sormanOszlop_var.get()} oszlop tartalma: {self.sormanAdat_var.get().strip()}\nAhhoz, hogy lásd az eredményt:\nTáblák szekcióban nyisd meg a táblát.\nHa megvan nyitva az adott tábla, nyisd meg újra.')

                                        self.sormanOszlop_var.set('')
                                        self.sormanSor_var.set('')
                                        self.sormanAdat_var.set('')
                                else:
                                    self.statuszcheck.set(f'Státusz\nSikertelen sorszerkesztés!\nTöbb adatot adtál meg, viszont csak 1 oszlopot szerkesztesz!')
                            else:
                                self.statuszcheck.set(f'Státusz\nSikertelen sorszerkesztés!\nNem adtál meg adatot!')
                        else:
                            self.statuszcheck.set(f'Státusz\nSikertelen sorszerkesztés!\nNincs ilyen sor! Max sor: {len(daata["Content"])}')
                    else:
                        self.statuszcheck.set(f'Státusz\nSikertelen sorszerkesztés!\nNincs ilyen sor! Max sor: {len(daata["Content"])}')
                else:
                    self.statuszcheck.set(f'Státusz\nSikertelen sorszerkesztés!\nA megadott oszlop nincs az oszlopok között!')
            else:
                self.statuszcheck.set(f'Státusz\nSikertelen sorszerkesztés!\nNyiss meg egy táblát!')
        else:
            self.statuszcheck.set(f'Státusz\nSikertelen sorszerkesztés!\nNyiss meg egy Adatbázist!')

        self.addline_var.set('')
        self.removeline_var.set('')
        self.addcolumn_var.set('')
        self.removecolumn_var.set('')


class queryPagePopup(ctk.CTkFrame):
    def __init__(self, parent, content):
        super().__init__(master = parent)

        # data
        self.content = content
        self.queryname = ctk.StringVar()

        # fonts
        titleFont = ctk.CTkFont(family = MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                                size = QUERYSAVETITLE_TSIZE)

        querynameFont = ctk.CTkFont(family = MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                                    size = QUERYSAVENAME_TSIZE)

        mentesButtonFont = ctk.CTkFont(family = AVERAGE_BUTTON_FAMILY,
                                       size = AVERAGE_BUTTON_TSIZE)

        statuszFont = ctk.CTkFont(family = MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                                  size = QUERYSTATUSZ_TSIZE)

        # widgets
        self.cimLabel = ctk.CTkLabel(self, text = f'Lekérdezés mentése', font = titleFont)
        self.utasitasLabel = ctk.CTkLabel(self, text = 'A lekérdezés neve', font = querynameFont)
        self.nevEntry = ctk.CTkEntry(self, textvariable = self.queryname, font = querynameFont)


        self.savebutton = ctk.CTkButton(self,
                                        text = 'Mentés',
                                        command = self.save_func,
                                        fg_color = AVERAGE_BUTTON_BG_COLOR,
                                        hover_color = AVERAGE_BUTTON_HOVER_COLOR,
                                        text_color = AVERAGE_BUTTON_TCOLOR,
                                        font = mentesButtonFont)


        self.statuszLabel = ctk.CTkLabel(self, text = 'Státusz\nParancsra Várás', font = statuszFont)

        self.cimLabel.pack(expand = True, fill = 'both',pady = 10)
        self.utasitasLabel.pack(expand = True, fill = 'both',pady = 10)
        self.nevEntry.pack(expand = True, fill = 'both',pady = 10, padx = 50)
        self.savebutton.pack(expand = True, fill = 'both',pady = 10, padx = 100)
        self.statuszLabel.pack(expand = True, fill = 'both',pady = 10)

    def save_func(self):
        pathToQueries = os.getcwd() + '\\' + 'Queries' + '\\'


        if self.queryname.get() in get_saved_queries():
            self.statuszLabel.configure(text='Státusz\nSikertelenül mentetted a lekérdezést!\nIlyen nevű lekérdezés már létezik!')
            return

        if self.content != '':
            try:
                if 'Hiba' not in self.content['Columns'][0] and 'Lehet valamit elírtál, kérlek csekkold.' not in self.content['Content'][0][0]:
                    if self.queryname.get():
                        with open(pathToQueries+self.queryname.get()+'.query', 'w', encoding = 'utf-8') as f:
                            f.write(' '.join(self.content['Columns'])+'\n')

                            for records in self.content['Content']:
                                f.write(' '.join(records)+'\n')

                        self.statuszLabel.configure(text = 'Státusz\nSikeresen mentetted a lekérdezést!')
                    else:
                        self.statuszLabel.configure(text='Státusz\nSikertelenül mentetted a lekérdezést!\nAdj nevet a lekérdezésnek!')
                else:
                    self.statuszLabel.configure(text='Státusz\nSikertelenül mentetted a lekérdezést!\nHaha.. a hibaüzenetet nem engedem, hogy lementsd.')
            except:
                self.statuszLabel.configure(text='Státusz\nSikertelenül mentetted a lekérdezést!\nHaha.. a hibaüzenetet nem engedem, hogy lementsd.')
        else:
            self.statuszLabel.configure(text='Státusz\nSikertelenül mentetted a lekérdezést!\nÜres lekérdezést felesleges lementeni.')

class queryPage(ctk.CTkFrame):
    def __init__(self, parent, dbase_name_var):
        super().__init__(master = parent)

        # layout
        self.rowconfigure(0, weight = 1, uniform = 'queryPage')
        self.rowconfigure(1, weight = 5, uniform = 'queryPage')
        self.rowconfigure(2, weight = 1, uniform = 'queryPage')

        self.columnconfigure((0,1), weight = 2, uniform = 'queryPage')
        self.columnconfigure(2, weight = 1, uniform = 'queryPage')

        # fonts
        lekerdezFont = ctk.CTkFont(family = MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                                   size = BIG_QUERY_BUTTON_TSIZE)

        sqlsectionFont = ctk.CTkFont(family = MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                                     size = SQLSECTION_TSIZE)

        cimFont = ctk.CTkFont(family = MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                              size = SQLCIMSIZE)

        torlescimFont = ctk.CTkFont(family = MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                              size = SQLCIMSIZE+4)

        buttonFont = ctk.CTkFont(family = AVERAGE_BUTTON_FAMILY,
                                 size = AVERAGE_BUTTON_TSIZE-4)

        exitbuttonFont = ctk.CTkFont(family=AVERAGE_BUTTON_FAMILY,
                                     size=AVERAGE_BUTTON_TSIZE)

        optionmenufont = ctk.CTkFont(family=MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                                     size=OPTIONMENU_TSIZE)

        # data
        self.dbase_name_var = dbase_name_var
        self.query = ''
        self.saved_queries = get_saved_queries()
        self.choosed_query = ctk.StringVar(value = 'Mentett lekérdezések')
        self.delete_query = ctk.StringVar(value = 'Lekérdezés törlése')

        # widgets
        self.sqlInfoLabel = ctk.CTkLabel(self, text = 'SQL Szekció', font = cimFont)
        self.eredmenyInfoLabel = ctk.CTkLabel(self, text = 'Eredmény', font = cimFont)
        self.eszkozokInfoLabel = ctk.CTkLabel(self, text = 'Eszközök', font = cimFont)

        self.sqlSubmitButton = ctk.CTkButton(self,
                                             text = 'Lekérdez',
                                             command = self.doQueryFunc,
                                             fg_color = BIG_QUERY_BUTTON_BGCOLOR,
                                             hover_color = AVERAGE_BUTTON_HOVER_COLOR,
                                             text_color = AVERAGE_BUTTON_TCOLOR,
                                             font = lekerdezFont)
        self.sqlTextSection = ctk.CTkTextbox(self, font = sqlsectionFont)

        self.querytreeview = ttk.Treeview(self,
                                          columns=[],
                                          show='headings',
                                          style = 'mystyle.Treeview')

        self.scrollbary = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.querytreeview.yview)
        self.scrollbarx = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.querytreeview.xview)

        # treeview scrollbars configure
        self.querytreeview.configure(yscrollcommand=self.scrollbary.set)
        self.querytreeview.configure(xscrollcommand=self.scrollbarx.set)
        # --

        self.lekerdezesManageFrame = ctk.CTkFrame(self)
        self.lekerdezesManageFrame.rowconfigure(list(range(6)), weight = 1, uniform = 'lekerdezesManageFrame')
        self.lekerdezesManageFrame.columnconfigure(0, weight = 1, uniform = 'lekerdezesManageFrame')


        self.saveButton = ctk.CTkButton(self.lekerdezesManageFrame,
                                        text = 'Lekérdezés Mentése',
                                        command = lambda: self.show_popup(type = 'Save'),
                                        fg_color = DBLIST_LIST_BTN_BG_COLOR,
                                        hover_color = AVERAGE_BUTTON_HOVER_COLOR,
                                        text_color = AVERAGE_BUTTON_TCOLOR,
                                        font = buttonFont)

        self.queryOptionMenu = ctk.CTkOptionMenu(self.lekerdezesManageFrame,
                                                 values=self.saved_queries,
                                                 variable=self.choosed_query,
                                                 fg_color=OPTIONMENU_FGCOLOR,
                                                 text_color=OPTIONMENU_TCOLOR,
                                                 button_color=OPTIONMENU_NYILFGCOLOR,
                                                 font=optionmenufont)

        self.loadButton = ctk.CTkButton(self.lekerdezesManageFrame,
                                        text = 'Lekérdezés Betöltése',
                                        command = self.loadqueryFunc,
                                        fg_color=DBLIST_LIST_BTN_BG_COLOR,
                                        hover_color=AVERAGE_BUTTON_HOVER_COLOR,
                                        text_color=AVERAGE_BUTTON_TCOLOR,
                                        font=buttonFont)

        self.savePopup = queryPagePopup(parent=self, content=self.query)

        self.popupExitButton = ctk.CTkButton(self,
                                             text = 'X',
                                             command = self.exit_popup,
                                             fg_color=DBLIST_LIST_BTN_BG_COLOR,
                                             hover_color=AVERAGE_BUTTON_HOVER_COLOR,
                                             text_color=AVERAGE_BUTTON_TCOLOR,
                                             font=exitbuttonFont)

        self.deleteQueryOptionMenu = ctk.CTkOptionMenu(self.lekerdezesManageFrame,
                                                       values=self.saved_queries,
                                                       variable=self.delete_query,
                                                       fg_color=OPTIONMENU_FGCOLOR,
                                                       text_color=OPTIONMENU_TCOLOR,
                                                       button_color=OPTIONMENU_NYILFGCOLOR,
                                                       font=optionmenufont)

        self.deleteQueryButton = ctk.CTkButton(self.lekerdezesManageFrame,
                                               text = 'Lekérdezés törlése',
                                               command = lambda: self.deleteQueryFunc(self.delete_query.get()),
                                               fg_color=DBLIST_LIST_BTN_BG_COLOR,
                                               hover_color=AVERAGE_BUTTON_HOVER_COLOR,
                                               text_color=AVERAGE_BUTTON_TCOLOR,
                                               font=buttonFont)

        self.sikeresTorlesFrame = ctk.CTkFrame(self)
        self.sikeresTorlesCim = ctk.CTkLabel(self.sikeresTorlesFrame, text = 'Sikeres lekérdezés törlés!', font = torlescimFont)
        self.sikeresTorlesKontent = ctk.CTkLabel(self.sikeresTorlesFrame,
                                                 text = 'Sikeresen törölted a(z) .. lekérdezést!',
                                                 font = cimFont)

        self.sikeresTorlesExitButton = ctk.CTkButton(self,
                                                     text = 'X',
                                                     command = self.torlespopupExitfunc,
                                                     fg_color = AVERAGE_BUTTON_BG_COLOR,
                                                     hover_color = AVERAGE_BUTTON_HOVER_COLOR,
                                                     text_color = AVERAGE_BUTTON_TCOLOR,
                                                     font = exitbuttonFont)

        self.alap_lekerdezestbeilleszto_gomb = ctk.CTkButton(self.lekerdezesManageFrame,
                                                             text='Alap lekérdezés',
                                                             command=self.alapsqlInsert,
                                                             fg_color=DBLIST_LIST_BTN_BG_COLOR,
                                                             hover_color=AVERAGE_BUTTON_HOVER_COLOR,
                                                             text_color=AVERAGE_BUTTON_TCOLOR,
                                                             font=buttonFont)


        # grid
        self.sqlInfoLabel.grid(column = 0, row = 0)
        self.eredmenyInfoLabel.grid(column = 1, row = 0)
        self.eszkozokInfoLabel.grid(column = 2, row = 0)

        self.sqlSubmitButton.grid(column = 0, row = 2, sticky = 'nsew', padx = 20, pady = 20)
        self.sqlTextSection.grid(column = 0, row = 1, sticky = 'nsew', padx = 10, pady = 10)

        self.lekerdezesManageFrame.grid(column = 2, row = 1, rowspan = 2, sticky = 'nsew')

        self.saveButton.grid(column = 0, row = 0, sticky = 'n', pady = 10)

        self.queryOptionMenu.grid(column = 0, row = 1, sticky = 's', pady = 10)
        self.loadButton.grid(column = 0, row = 2, rowspan = 2, sticky = 'n', pady = 10)

        self.deleteQueryOptionMenu.grid(column = 0, row = 3, sticky = 's', pady = 10)
        self.deleteQueryButton.grid(column = 0, row = 4, sticky = 'n', pady = 10)

        self.alap_lekerdezestbeilleszto_gomb.grid(column = 0, row = 5)

        self.sikeresTorlesCim.pack()
        self.sikeresTorlesKontent.pack(pady = 30)

    def doQueryFunc(self):
        self.exit_popup()
        sql_code = self.sqlTextSection.get("0.0", "end").strip()
        try:
            self.query = doQueryStuff(self.dbase_name_var.get(), sql_code)
        except:
            self.query = {'Columns': ['Hiba'], 'Content': [['Lehet valamit elírtál, kérlek csekkold.'],
                                                           ['Lehet üres a lekérdezésed.'],
                                                           ['Nem felejtettél el megnyitni egy Adatbázist?'],
                                                           ['Esetleg üres az oszlop, vagy rekord mező.'],
                                                           ['Vagy hibás SQL kódot írtál.'],
                                                           ['Esetleg az egyik oszlopodban több fajta adat van.'],
                                                           ['(pl.: szám is, és szöveg is)'],
                                                           ['Esetleg te, vagy én logikai hibát vétettünk.']]}

        self.savePopup = queryPagePopup(parent=self, content=self.query)
        self.popupExitButton.lift()
        self.set_treeview()

    def set_treeview(self):
        self.scrollbarx.grid_forget()
        self.scrollbary.grid_forget()
        self.querytreeview.grid_forget()

        style = ttk.Style(self)
        style.configure("Treeview", fieldbackground = 'black')

        for item in self.querytreeview.get_children():
            self.querytreeview.delete(item)

        try:
            if self.query['Columns'][0] != 'Hiba' and self.query['Content'][0] != 'Valamit elírtál, kérlek csekkold.':
                if self.query['Columns'] and self.query['Content']:
                    self.querytreeview.configure(columns=self.query['Columns'])

                    maxlen_columns = {name: 0 for name in self.query['Columns']}
                    for column in self.query['Columns']:  # kiszámoljuk, mennyi szélesség kell, hogy kiférjenek a karakterek
                        for content in self.query['Content']:
                            for index, check in enumerate(content):
                                if maxlen_columns[self.query['Columns'][index]] < len(check):
                                    maxlen_columns[self.query['Columns'][index]] = len(check)


                        self.querytreeview.heading(column, text=column)

                        
                        if len(column) > maxlen_columns[column]:
                            self.querytreeview.column(column, width=10 + len(column) * 10, anchor=tk.CENTER)

                        else:
                            self.querytreeview.column(column, width=10 + maxlen_columns[column] * 10, anchor=tk.CENTER)


                if self.query['Content']:
                    for content in self.query['Content']:
                        self.querytreeview.insert('', tk.END, values=content)
            else:
                self.querytreeview.configure(columns='Hiba')
                self.querytreeview.heading('Hiba', text='Hiba')

                for hibauzenetek in self.query['Content']:
                    self.querytreeview.insert('', tk.END, values=hibauzenetek)

                self.querytreeview.column('Hiba', width=312, anchor=tk.CENTER)

        except:
            self.query = {'Columns': ['Hiba'], 'Content': [['Lehet valamit elírtál, kérlek csekkold.'],
                                                           ['Lehet üres a lekérdezésed.'],
                                                           ['Nem felejtettél el megnyitni egy Adatbázist?'],
                                                           ['Esetleg üres az oszlop, vagy rekord mező.'],
                                                           ['Vagy hibás SQL kódot írtál.'],
                                                           ['Esetleg az egyik oszlopodban több fajta adat van.'],
                                                           ['(pl.: szám is, és szöveg is)'],
                                                           ['Esetleg te, vagy én logikai hibát vétettünk.']]}

            self.querytreeview.configure(columns='Hiba')
            self.querytreeview.heading('Hiba', text='Hiba')

            for hibauzenetek in self.query['Content']:
                self.querytreeview.insert('', tk.END, values=hibauzenetek)

            self.querytreeview.column('Hiba', width=312, anchor=tk.CENTER)

        self.scrollbarx.grid(column=1, row=1, rowspan=2, sticky='ews')
        self.scrollbary.grid(column=1, row=1, rowspan=2, sticky='nse')
        self.querytreeview.grid(column = 1, row = 1, rowspan=2, padx = 19, pady = 19, sticky = 'nsew')


    def show_popup(self, type):
        self.savePopup.place(relx = 0.3, rely = 0.2, relwidth = 0.48, relheight = 0.6)
        self.popupExitButton.place(relx = 0.7, rely = 0.22, relwidth = 0.06, relheight = 0.08)

    def exit_popup(self):
        self.saved_queries = get_saved_queries()
        self.queryOptionMenu.configure(values=self.saved_queries)
        self.deleteQueryOptionMenu.configure(values=self.saved_queries)

        self.savePopup.place_forget()
        self.popupExitButton.place_forget()

    def loadqueryFunc(self):
        if self.choosed_query.get() != 'Mentett lekérdezések':
            self.query = get_table_content(database_name = '__nagyonegyedikülönckesavedQuery', table_name = self.choosed_query.get()+'.query')
            self.set_treeview()

    def alapsqlInsert(self):
        self.sqlTextSection.delete('0.0', tk.END)
        self.sqlTextSection.insert('0.0', 'SELECT *\nFROM <táblanév>\nWHERE <feltétel>;')

    def deleteQueryFunc(self, queryname):
        if queryname != 'Lekérdezés törlése':
            if delete_query(queryname) == 'Siker':
                self.saved_queries = get_saved_queries()
                self.queryOptionMenu.configure(values=self.saved_queries)
                self.deleteQueryOptionMenu.configure(values=self.saved_queries)

                self.delete_query.set('Lekérdezés törlése')
                self.choosed_query.set('Mentett lekérdezések')

                self.sikeresTorlesKontent.configure(text=f'Sikeresen törölted a(z)\n{queryname} nevű lekérdezést!')

                self.sikeresTorlesFrame.place(relx=0.3, rely=0.2, relwidth=0.48, relheight=0.35)
                self.sikeresTorlesExitButton.place(relx=0.71, rely=0.21, relwidth=0.06, relheight=0.08)

            else:
                pass

    def torlespopupExitfunc(self):
        self.sikeresTorlesFrame.place_forget()
        self.sikeresTorlesExitButton.place_forget()

class segitsegAblak(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        # window settings
        self.window_width = self.winfo_screenwidth() // 2 + +self.winfo_screenwidth() // 4
        self.window_height = self.winfo_screenheight() // 1.3

        self.geometry(f'{self.window_width+350}x{self.window_height+100}')

        self.title('Segítség - Tutorial')
        self.iconbitmap(os.getcwd() + '\\' + '_img' + '\\' + 'icon.ico')

        # window layout
        self.columnconfigure(0, weight = 1, uniform = 'segitsegablak')
        self.columnconfigure(1, weight = 8, uniform = 'segitsegablak')
        self.columnconfigure(2, weight = 1, uniform = 'segitsegablak')

        self.rowconfigure(0, weight = 1, uniform = 'segitsegablak')

        # data
        self.hanyadik_kep = 0

        self.img_path = os.getcwd()+'\\_img\\tutorial_imgs'
        self.img_list = list(sorted(os.listdir(self.img_path), key=len))

        self.image = Image.open(self.img_path + '\\' + self.img_list[self.hanyadik_kep])
        self.image_tk = ImageTk.PhotoImage(self.image)

        # font
        buttonFont = ctk.CTkFont(family = AVERAGE_BUTTON_FAMILY,
                                 size = AVERAGE_BUTTON_TSIZE+20)

        segitsegSzovegFont = ctk.CTkFont(family = MAINWINDOW_SELECTED_DBTEXT_FAMILY,
                                         size = 30)

        # widgets
        self.balraButton = ctk.CTkButton(self,
                                         text = '<',
                                         width = 100,
                                         height = 100,
                                         command = lambda: self.kepvaltas('Balra'),
                                         fg_color = AVERAGE_BUTTON_BG_COLOR,
                                         hover_color = AVERAGE_BUTTON_HOVER_COLOR,
                                         text_color = AVERAGE_BUTTON_TCOLOR,
                                         font = buttonFont)

        self.kepmegjelenitoCanvas = tk.Canvas(self, background = '#242424', bd = 0, highlightthickness = 0, relief = 'ridge')

        self.jobbraButton = ctk.CTkButton(self,
                                          text = '>',
                                          width = 100,
                                          height = 100,
                                          command = lambda: self.kepvaltas('Jobbra'),
                                          fg_color=AVERAGE_BUTTON_BG_COLOR,
                                          hover_color=AVERAGE_BUTTON_HOVER_COLOR,
                                          text_color=AVERAGE_BUTTON_TCOLOR,
                                          font=buttonFont)

        self.segitsegSzoveg = ctk.CTkLabel(self.kepmegjelenitoCanvas,
                                           text = f'Oldal {self.hanyadik_kep+1}',
                                           text_color = SEGITSEGOLDAL_SZOVEGSZIN,
                                           font = segitsegSzovegFont)

        # set first image to the canvas
        self.kepmegjelenitoCanvas.create_image(self.image_tk.width()/2, self.image_tk.height()/2, image = self.image_tk)

        # widgets grid
        self.balraButton.grid(column = 0, row = 0, padx = 5)
        self.kepmegjelenitoCanvas.grid(column = 1, row = 0, sticky = 'nsew', padx = 5, pady = 5)
        self.jobbraButton.grid(column = 2, row = 0, padx = 5)
        self.segitsegSzoveg.pack(side = 'bottom', pady = 10)

    def kepvaltas(self, merre):
        self.kepmegjelenitoCanvas.delete('all')

        if self.hanyadik_kep == len(self.img_list)-1 and merre == 'Jobbra':
            self.hanyadik_kep = 0

        elif self.hanyadik_kep == 0 and merre == 'Balra':
            self.hanyadik_kep = len(self.img_list)-1

        else:
            self.hanyadik_kep += 1 if merre == 'Jobbra' else -1

        self.image = Image.open(self.img_path + '\\' + self.img_list[self.hanyadik_kep])
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.kepmegjelenitoCanvas.create_image(self.image_tk.width() / 2,
                                               self.image_tk.height() / 2,
                                               image=self.image_tk)

        self.segitsegSzoveg.configure(text = f'Oldal {self.hanyadik_kep+1}')
