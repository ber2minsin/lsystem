import tkinter as tk
import tkinter.font
from tkinter import Event, ttk
from tkinter import colorchooser
from tkinter import messagebox
from lsystem import rgb_to_hex
import os
import json
import pygame



# TODO unshow the text indicator if the combobox
#      or any other input field is out of focus

class MainApp(ttk.Notebook):
    def __init__(self, master, *args, **kwargs):
        ttk.Notebook.__init__(self, master, *args, **kwargs)
        self.master = master
        
        master.title('Settings')
        master.geometry('500x500')
        master.option_add('*Font', 'Helvetica 12')

        self.style = ttk.Style()

        # Clear the dashed lines on tabs
        # credit to Fabien Andre(https://stackoverflow.com/users/428236/fabienandre)
        self.style.layout("Tab",
        [('Notebook.tab', {'sticky': 'nswe', 'children':
            [('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children':
                    [('Notebook.label', {'side': 'top', 'sticky': ''})],
            })],
        })]
        )

        self.session_settings = {
            'res': None,
            'ln_clr': None,
            'bg_clr': None,
            'ln_len': None
        }
        
        self.tabs = []
        self.lsys_tab = LsystemTab(self)
        self.add(self.lsys_tab, text='L-Systems')

        self.general_tab = GeneralSettingsTab(self)
        self.add(self.general_tab, text='General Settings')

        self.drawing_tab = DrawSettingsTab(self)
        self.add(self.drawing_tab, text='Drawing Settings')

        self.export_tab = ExportTab(self)
        self.add(self.export_tab, text='Export')

        self.tabs.append(self.lsys_tab)
        self.tabs.append(self.general_tab)
        self.tabs.append(self.drawing_tab)
        self.tabs.append(self.export_tab)
        
        self.save_settings_button = tk.Button(self, text='Save settings', command=self.save_settings)
        for tab in self.tabs:
            # TODO add save button to all pages
            print()

    # TODO maybe in later versions let the user save multiple settings
    def save_settings(self):
        self.session_settings['res'] = [int(x) for x in self.drawing_tab.res_combobox.get().split('x')]

        with open(os.path.dirname(__file__) + '\\settings.json', 'w') as f:
            f.write(json.dumps(self.session_settings, indent=4))
        
        saved_settings_dict.update(self.session_settings)
    
    def load_settings(self):
        with open(os.path.dirname(__file__) + '\\settings.json', 'r') as f:
            saved_settings_dict.update(json.loads(f.read()))
            self.session_settings.update(saved_settings_dict)
            
            if saved_settings_dict['res'] is not None:
                self.general_tab.res_combobox.set(str(saved_settings_dict['res'][0]) + 'x' + str(saved_settings_dict['res'][1]))
            if saved_settings_dict['ln_clr'] is not None:
                self.drawing_tab.ln_color_label.configure(background=lsystem.rgb_to_hex(saved_settings_dict['ln_clr'][0], saved_settings_dict['ln_clr'][1], saved_settings_dict['ln_clr'][2]))
            if saved_settings_dict['bg_clr'] is not None:
                self.drawing_tab.bg_color_label.configure(background=lsystem.rgb_to_hex(saved_settings_dict['bg_clr'][0], saved_settings_dict['bg_clr'][1], saved_settings_dict['bg_clr'][2]))
            if saved_settings_dict['ln_len'] is not None:
                self.drawing_tab.ln_length_slider.set(saved_settings_dict['ln_len'])
    

    def choose_color(self, label, dictionary_key, title):
        color_code = colorchooser.askcolor(title =title)
        self.session_settings[dictionary_key] = color_code[0]
        label.configure(background=color_code[1])
    
    def is_session_saved(self):
        for x in self.session_settings:
            if  self.session_settings[x] != None and saved_settings_dict[x] != None:
                if self.session_settings[x] != saved_settings_dict[x]:
                    print(x, 'is unsaved')
                    print('saved:', saved_settings_dict[x])
                    print('session:', self.session_settings[x])
                    return False
        print('True')
        return True
    
    def on_closing(self):
        if self.is_session_saved() == False:
            if tk.messagebox.askokcancel("Quit", "You have unsaved changes, do you really want to quit?"):
                root.destroy()
        else:
            root.destroy()


class LsystemTab(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        ttk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master

class GeneralSettingsTab(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        ttk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master

        # Elements
        self.res_text_label = tk.Label(self, text='Resolution: ')
        self.res_combobox = ttk.Combobox(self, values=self.get_supported_resolutions(), width=9)

        # Virtual Events
        self.res_combobox.bind('<<ComboboxSelected>>', self.save_cbox_res_val)

        # Grid
        self.res_text_label.grid(column=0, row=0)
        self.res_combobox.grid(column=1, row=0, columnspan=2)

    def save_cbox_res_val(self, event):
        # Change resolution back to integer format
        self.master.session_settings['res'] = [int(x) for x in self.res_combobox.get().split('x')]
        print(self.res_combobox.get())
    

    def get_supported_resolutions(self):
        all_resolutions = pygame.display.list_modes()

        # Get rid of non-unique values using set properties
        tempset = set()
        all_resolutions = [x for x in all_resolutions if x not in tempset and not tempset.add(x)]

        # Format the resolutions
        all_resolutions_formatted = []
        for res in all_resolutions:
            all_resolutions_formatted.append(str(res[0]) + 'x' + str(res[1]))
        
        return all_resolutions_formatted

class DrawSettingsTab(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        ttk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master

        self.align = tk.W

        # Elements
        self.ln_length_text_label =  tk.Label(self, text='Line length: ')
        self.ln_color_text_label =   tk.Label(self, text='Line color: ')
        self.bg_color_text_label =   tk.Label(self, text='BG color: ')

        self.ln_color_label = tk.Label(self, text="".rjust(5), background='white', borderwidth=1, relief=tk.SOLID)
        self.bg_color_label = tk.Label(self, text="".rjust(5), background='white', borderwidth=1, relief=tk.SOLID)
        
        self.ln_color_button = tk.Button(self, text = "Select", command=lambda: master.choose_color(self.ln_color_label, 'ln_clr', 'Choose line color'))
        self.bg_color_button = tk.Button(self, text="Select", command=lambda: master.choose_color(self.bg_color_label, 'bg_clr', 'Choose background color'))

        self.ln_length_value_label = tk.Label(self, text='0', width=3, anchor=tk.W) # TODO give user the freedom to input with text
        self.ln_length_slider =      tk.Scale(self, from_=0, to=99, orient=tk.HORIZONTAL, showvalue=0, command=self.show_ln_len_val) # 99 because 3 digit numbers fucks up alignments and I can't be bothered

        # Virtual Events
        self.ln_length_slider.bind('<ButtonRelease-1>', self.save_ln_len_val)
        self.ln_color_label.bind('<Button-1>', lambda Event: master.choose_color(self.ln_color_label, 'ln_clr', 'Choose line color'))
        self.bg_color_label.bind('<Button-1>', lambda Event: master.choose_color(self.bg_color_label, 'bg_clr', 'Choose background color'))
        
        # Grid
        self.ln_length_text_label.grid(column=0, row=0, sticky=self.align)
        self.ln_length_value_label.grid(column=1, row=0, sticky=self.align)
        self.ln_length_slider.grid(column=2, row=0, sticky=self.align)

        self.ln_color_text_label.grid(column=0, row=1, sticky=self.align)
        self.ln_color_label.grid(column=1, row=1, sticky=self.align)
        self.ln_color_button.grid(column=2, row=1, sticky=self.align)

        self.bg_color_text_label.grid(column=0, row=2, sticky=self.align)
        self.bg_color_label.grid(column=1, row=2, sticky=self.align)
        self.bg_color_button.grid(column=2, row=2, sticky=self.align)

    def save_ln_len_val(self, event):
        self.master.session_settings['ln_len'] = self.ln_length_slider.get()

    def show_ln_len_val(self, event):
        self.ln_length_value_label.configure(text=self.ln_length_slider.get())
class ExportTab(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        ttk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master


if __name__ == '__main__':
    # Saved settings on settings.json
    saved_settings_dict = {}

    root = tk.Tk()

    pygame.init()

    main_app = MainApp(root)
    main_app.load_settings()
    main_app.pack(expand=1, fill='both')

    root.protocol("WM_DELETE_WINDOW", main_app.on_closing)
    root.mainloop()