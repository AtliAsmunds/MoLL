import os
from tkinter import IntVar, StringVar, filedialog
import pygubu
import pandas as pd
from data.expand_tag import expand_tag as ex_tag
from data.options import show_option, tag_dict


PROJECT_PATH = os.path.dirname(__file__)
PROJECT_UI = os.path.join(PROJECT_PATH, "data/Moll.ui")
ERRORS = ("Markastrengur ekki samþykktur",\
            "Ólöglegur upphafsstafur",\
            "Ekki fleiri möguleikar",\
            "Óþekktur valmöguleiki")
WORD, TAG, LEMMA, NEW_TAG, NEW_LEMMA = 'Orð', 'Mark', 'Lemma', 'Leiðrétt mark', 'Leiðrétt lemma'


class MollGuiApp:


    def __init__(self, root):

        # Configure root
        root.title('MoLL (Marka og Lemmu Leiðrétting)')
        root.bind('<Down>', self._next_word)
        root.bind('<Up>', self._prev_word)
        root.bind('<Alt-s>', self._save_changes)
        root.bind('<Control-s>', self._save_file)
        root.resizable(width=False, height=False)


        # Configure function loops
        root.after(20, self._show_option_text)
        root.after(20, self._expand_tag)

        
        # Read GUI data from file
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('mainframe')
        builder.connect_callbacks(self)


        # Initialize data collections
        self.data = {}
        self.words = []
        self.lemma = []
        self.tags = []
        self.new_tag = []
        self.new_lemma = []


        # Initialize persmissions and index
        self.allow_lemma = 0
        self.allow_tag = 0
        self.allow_save = 0
        self.word_index = 0


        # Initialize changeble string and integer variables
        self.text_var = StringVar()
        self.prev_word_var = StringVar()
        self.next_word_var = StringVar()
        self.current_word_var = StringVar()
        self.current_lemma_var = StringVar()
        self.current_tag_var = StringVar()
        self.options = StringVar()
        self.lemma_check_var = IntVar()
        self.tag_check_var = IntVar()
        self.old_file_var = IntVar()
        self.new_lemma_var = StringVar()
        self.new_tag_var = StringVar()
        self.current_index_var = StringVar()

        
        # Import necessary widgets and labels for variable assignment and other functions
        self.current_word = builder.get_object('current_word')
        self.word_entry = builder.get_object('entry_1')
        self.lemma_entry = builder.get_object('entry_2')
        self.tag_entry = builder.get_object('entry_3')
        self.prev = builder.get_object('back')
        self.next = builder.get_object('forward')
        self.save_change_button = builder.get_object('save_change_button')
        self.extended_tag = builder.get_object('extended_tag')
        self.path_chooser = builder.get_object('path_chooser')
        self.prev_word_label = builder.get_object('prev_word')
        self.next_word_label = builder.get_object('next_word')
        self.option_text = builder.get_object('option_text')
        self.separator = builder.get_object('sep_field')
        self.new_lemma_label = builder.get_object('new_lemma_label')
        self.new_tag_label = builder.get_object('new_tag_label')
        self.lemma_check = builder.get_object('lemma_check')
        self.tag_check = builder.get_object('tag_check')
        self.old_file_check = builder.get_object('old_file')
        self.index_button = builder.get_object('find_index_button')
        self.index_entry = builder.get_object('find_index')
        self.current_index = builder.get_object('current_index')

        
        # Assign variables to specific widgets and labels
        self.extended_tag.config(textvariable=self.text_var)
        self.prev_word_label.config(textvariable=self.prev_word_var)
        self.next_word_label.config(textvariable=self.next_word_var)
        self.option_text.config(textvariable=self.options)
        self.new_lemma_label.config(textvariable=self.new_lemma_var)
        self.new_tag_label.config(textvariable=self.new_tag_var)
        self.lemma_check.config(variable=self.lemma_check_var)
        self.tag_check.config(variable=self.tag_check_var)
        self.old_file_check.config(variable=self.old_file_var)
        self.current_index.config(textvariable=self.current_index_var)
        self.current_word.config(textvariable=self.current_word_var)
        self.word_entry.config(textvariable=self.current_word_var)
        self.lemma_entry.config(textvariable=self.current_lemma_var)
        self.tag_entry.config(textvariable=self.current_tag_var)


    def run(self):
        '''Runs the main program, needs to be called'''

        self.mainwindow.mainloop()


    def _config_entries(self, lemma_var, tag_var):
        '''Enables or disables lemma and tag enries according to permission'''

        self.lemma_entry.config(state='normal')
        self.tag_entry.config(state='normal')

        if not lemma_var:
            self.lemma_entry.config(state='disabled')

        if not tag_var:
            self.tag_entry.config(state='disabled')


    def _find_last_changed(self, column:list):
        '''Finds the first unchanged value in the column'''

        index = 0
        for value in column:
            if pd.isna(value):
                return index
            index += 1
        return 0


    def _del_index_error(self):
        '''Deletes index entry text'''

        self.index_entry.delete(0, 'end')
        self.index_entry.config(foreground='black')


    def _show_index_error(self):
        '''Shows an index error'''

        self.index_entry.delete(0, 'end')
        self.index_entry.insert(0, 'Utan marka')
        self.index_entry.config(foreground='grey')


    def _go_to_index(self):
        '''Sets the current word index (row) to a specific value'''

        if self.data:
            try:
                self.word_index = int(self.index_entry.get())
                self._update_all()
            except (ValueError, IndexError, KeyError):
                self._show_index_error()

        else:
            self._show_index_error()

        # Calls the _del_index function after 1 second
        root.after(1000, self._del_index_error)


    def _load_file(self, file_name, old_file:int):
        '''Loads up data from the given file for opening'''

        delimiter = ';' if self.separator.get() == '' else self.separator.get()
        self.allow_lemma = lemma = self.lemma_check_var.get()
        self.allow_tag = tag = self.tag_check_var.get()

        if old_file:
            self.data = pd.read_csv(file_name, delimiter=delimiter)
            self.word_index = self._find_last_changed(self.data[NEW_TAG])
            try:
                self.new_lemma = self.data[NEW_LEMMA]
            except KeyError:
                self.new_lemma = ['' for i in range(len(self.words))]
            self.new_tag = self.data[NEW_TAG]
            self.words = (self.data[WORD])

        else:
            self.data = pd.read_csv(file_name, delimiter=delimiter, names=[WORD, TAG, LEMMA])
            self.word_index = 0
            self.words = (self.data[WORD])

            # Set all values to empty to account for rows in data
            self.new_lemma = ['' for i in range(len(self.words))]
            self.new_tag = ['' for i in range(len(self.words))]

        self._config_entries(lemma, tag)
        self._update_all()


    def _open_file(self):
        '''Opens a given file'''

        file_name = self.path_chooser.cget('path')
        old_file = self.old_file_var.get()

        try:
            self._load_file(file_name, old_file)
        except FileNotFoundError:
            pass

        self.path_chooser.entry.delete(0, 'end')


    def _save_file(self, _event=None):
        '''Adds changes made to data and saves file'''

        f = filedialog.asksaveasfile(mode='w', defaultextension="(í vinnslu).csv")

        if f is None:
            return

        if self.allow_tag or self.allow_lemma:
            self.data[NEW_TAG] = self.new_tag
            self.data[NEW_LEMMA] = self.new_lemma

        # Save to csv without number index
        self.data.to_csv(f, index=False, sep=';')
        f.close()
    

    def _save_changes(self, _event=None):
        '''Saves each applied change to a new lemma or tag collection'''

        if (self.allow_save or not self.allow_tag) and dict(self.data):

            # Save the new lemma, or as '-' if unchanged
            self.new_lemma[self.word_index] = '-' \
                if self.current_lemma_var.get() == self.data[LEMMA][self.word_index] \
                    else self.current_lemma_var.get()

            # Save the new tag, or as '-' if unchanged
            self.new_tag[self.word_index] = '-' \
                if self.current_tag_var.get() == self.data[TAG][self.word_index] \
                    else self.current_tag_var.get()
            
            self.new_lemma_var.set(self.new_lemma[self.word_index])
            self.new_tag_var.set(self.new_tag[self.word_index])


    def _pretty_print(self, tag:dict, capitalize=False):
        '''Formats a dictionary for a printable output string'''

        pretty_tag = ""
        for key in tag.keys():

            if capitalize:
                pretty_tag += f"{key}: {tag[key]}\n".capitalize()

            else:
                pretty_tag += f"{key}: {tag[key]}\n"

        return pretty_tag
    

    def _expand_tag(self, _event=None):
        '''Shows word categorization from tag string'''

        try:
            tag = ex_tag(self.current_tag_var.get())
            expanded_tag = self._pretty_print(tag, capitalize=True)
            
            # If tag is empty saving is not allowed
            if not expanded_tag:
                expanded_tag = ERRORS[1]
                self.allow_save = 0
                self.save_change_button.config(state='disabled')

            # Otherwise saving is allowed
            else:
                self.allow_save = 1
                self.save_change_button.config(state='normal')
        
        # Saving is not allowed if any errors occur
        except (KeyError, IndexError):
            expanded_tag = ERRORS[0]
            if self.allow_tag:
                self.allow_save = 0
                self.save_change_button.config(state='disabled')
        
        # Pack the text and call function on loop
        self.text_var.set(expanded_tag)
        root.after(20, self._expand_tag)


    def _prev_word(self, _event=None):
        '''Updates the index to the previous word (row)'''

        if self.word_index > 0:
            self.word_index -= 1
        self._update_all()


    def _next_word(self, _event=None):
        '''Updates the index to the next word (row)'''

        if self.word_index < len(self.words)-1:
            self.word_index += 1
        self._update_all()


    def _update_text(self):
        '''Updates text shown in textbox'''

        self.current_word_var.set(self.words[self.word_index])

        # Set configurations for first word context
        if self.word_index == 0:
            self.prev_word_var.set('')
            self.next_word_var.set(self.words[self.word_index+1])
            self.prev.config(state='disabled')

        # Set configuration for last word context
        elif self.word_index == len(self.words)-1:
            self.prev_word_var.set(self.words[self.word_index-1])
            self.next_word_var.set('')
            self.next.config(state='disabled')

        # Set configuration for 'in-between' word context
        else:
            self.prev_word_var.set(self.words[self.word_index-1])
            self.next_word_var.set(self.words[self.word_index+1])
            self.prev.config(state='normal')
            self.next.config(state='normal')


    def _update_workspace(self):
        '''Updates text entry, lemmas and tags in workspace'''

        new_lemma_string = self.new_lemma[self.word_index]
        new_tag_string = self.new_tag[self.word_index]

        # Set tags and lemmas, or empty string if columns are NaN (empty)
        self.current_lemma_var.set("" if pd.isna(self.data[LEMMA][self.word_index]) else self.data[LEMMA][self.word_index])
        self.current_tag_var.set(self.data[TAG][self.word_index])
        self.new_lemma_var.set("" if pd.isna(new_lemma_string) else new_lemma_string)
        self.new_tag_var.set("" if pd.isna(new_tag_string) else new_tag_string)


    def _update_all(self):
        '''Updates everything in workspace along with index label and expanded tag'''

        try:
            self._update_text()            
            self. _update_workspace()
        except IndexError:
            pass

        self.current_index_var.set(str(self.word_index))
        if self.text_var:
            self._expand_tag()
        
    
    def _show_option_text(self):
        '''Shows options for next possible tag in tag string'''
        
        try:
            option = show_option(self.current_tag_var.get(), tag_dict)
            option = self._pretty_print(option)

        except (IndexError, AttributeError):
            option = ERRORS[2]
        except KeyError:
            option = ERRORS[3]

        # Pack text and run function on loop
        self.options.set(option)
        root.after(20, self._show_option_text)


if __name__ == '__main__':
    import tkinter as tk
    root = tk.Tk()
    app = MollGuiApp(root)
    app.run()

