# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 23:43:37 2024

@author: Taylor Gibbons
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ttkwidgets import CheckboxTreeview

import pandas as pd
import os
import InventoryFunc as IF
import InventoryMain as IM



global testing
testing = 1

    


def set_filepath(filename: str):
    global filepath
    filepath = filename
    print(f'{filepath} is set')
    
def get_filepath() -> str:
    return filepath

def set_ext(extension: str):
    global ext
    ext = extension

def get_ext()-> str:
    return ext

def set_inv_df(cur_df: pd.DataFrame):
    global inv_df
    inv_df = cur_df

def get_inv_df() -> pd.DataFrame:
    return inv_df
    
def get_inv_list(df: pd.DataFrame) -> list[IF.Inventory]:
    return (IF.remakeInventoryList(df))
    
def main():
            
    def toggle_mode():
        if mode_switch.instate(['selected']):
            style.theme_use('forest-light')
        else:
            style.theme_use('forest-dark')
    
    def file_dialog():
    
        filepath = filedialog.askopenfilename(initialdir= os.getcwd(), title = 'Select A File',
                                              filetype= (('xlsx files','*.xlsx'),
                                                     ('pickle files','*.pkl'),
                                                     ('all files','*.*')),
                                              multiple = False)
        
        set_filepath(filepath)
        for i in range(len(filepath) - 1, 0, -1):
            if filepath[i] == '/':
                path_label['text'] = filepath[i+1:]
                break
            else:
                continue
        
        #load_data()    
    def clear_data():
        
        path_label['text'] = 'No File Selected'
        
        treeview['columns'] = ['','','','']  
        treeview.delete(*treeview.get_children())
            
        
        
    def load_data():
        global ext
        try:
            doc_filename = r'{}'.format(get_filepath())
            print('File Found')
            match doc_filename[-4:]:
                case 'xlsx':
                    print('Excel File')
                    df = pd.read_excel(doc_filename)
                    #set_ext('.xlsx')
                case '.csv':
                    print('CSV file')
                    df = pd.read_csv(doc_filename)
                    #set_ext('.csv')
                case '.pkl':
                    print('Pickle File')
                    df = pd.read_pickle(doc_filename)
                    #set_ext('.pkl')
                    
        except ValueError:
            ttk.messagebox.showerror('Information', 'The file you have selected in invalid')
            return None
        except FileNotFoundError:
            ttk.messagebox.showerror('Information', 'The file cannot be found')
            return None
        
        clear_data()

        treeview['column'] = list(df.columns)
        treeview['show'] = 'headings'
        
        for column in treeview['columns']:
            treeview.heading(column, text = column)
        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            treeview.insert('','end',values = row)
            
        #Starting to make the Inventory Dataframe
        
        set_inv_df(df) #Sets the global dataframe to keep the reference
    
    def insert_row():
        # print(f'name is {type(name_entry.get())}\n'+
        #    f'brand is {type(brand_entry.get())}\n'+
        #    f'stock is {type(stock_spinbox.get())}\n' +
        #    f'Unit is {type(unit_drop.get())}')
        
        if isinstance(name_entry.get(), str):
            name = name_entry.get()
        if isinstance(brand_entry.get(), str):
            brand = brand_entry.get()
        if isinstance(stock_spinbox.get(), str):
            stock = stock_spinbox.get()
        if isinstance(unit_drop.get(), str):
            unit = unit_drop.get()
                    
                
        
        row_vals = [name, brand, float(stock), unit]
        treeview.insert('',tk.END, values = row_vals) #add the new item to treeview
        
        item_add(row_vals)
        
    def close():
        
        
        if tk.messagebox.askyesno('save','Would you like to save the file?'):
            print('Closing Program: Saving...')
            try:
                filepath = get_filepath()
                if filepath:
                    match get_ext():
                        case 'xlsx':
                            get_inv_df().to_excel(get_filepath())
                        case '.pkl':
                            get_inv_df().to_pickle(get_filepath())
                        case '.csv':
                            get_inv_df().to_csv(get_filepath())
                        case _:
                            print('Could Not Save File :(')
            except FileExistsError:
                ans = tk.messagebox.askyesno('showerror','File Does Not Exist. Continue?')
            except FileNotFoundError:
                ans = tk.messagebox.askyesno('showerror', 'File Not Found. Continue?')
            except NameError:
                ans = tk.messagebox.askyesno('showerror', 'File Has Not Been Defined. Continue?')
            finally:
                print('ans =' +  str(ans))
                if ans:
                    root.destroy()
        else:
            root.destroy()
            
            
    def entry_reset():
        name_entry.insert(0,'Item Name')
        brand_entry.insert(0,'Brand Name')
        stock_spinbox.insert(0,'Stock')
        unit_drop.current(0)
        
    def item_add(item: list):
        
        df = get_inv_df()
        size = len(df.index)
        print(f'size: {size}')
        
        new_df = pd.DataFrame([item], columns = df.columns)
        new_df = pd.concat([df,new_df])
        
        new_df.reindex()
        
        set_inv_df(new_df)
        
        
        
        
    def df_test():
        file_dialog()
        load_data()
        print('Current DataFrame:')
        print(get_inv_df())
        IM.eq_print()
        
        print('\nAdding new Inventory Item:\nName: Popcorn\tBrand: Orvile\tStock: 3\tUnits: bags')
        temp_item = ['Popcorn','Orvile','5','bags']
        item_add(temp_item)
        
        print(get_inv_df())
        IM.eq_print()
    #Constants
    butt_padx = (5,5)
    butt_pady = (10,10)
    
    unit_combo = ['Unit','pieces', 'bags', 'lbs', ]
    
    col_heads = ['Name','Brand','Stock','Units']
    
    root = tk.Tk()
    root.title('Inventory List')
    #Styles, Modes
    style = ttk.Style(root)
    root.tk.call('source','forest-dark.tcl')
    root.tk.call('source','forest-light.tcl')
    style.theme_use('forest-dark')
    
    #Windows
    window = ttk.Frame(root)
    window.pack()
    
    #Window Frames
    data_frame = ttk.LabelFrame(window,
                                text = 'Load Previous Inventory List')
    data_frame.grid(column= 0,
                    row = 0,
                    padx = (10,10),
                    pady = (5,5))

    
    #Data_Frame Items, picking/loading data as well as the file name
    file_button = ttk.Button(data_frame, text= 'Browse Files', command= lambda: file_dialog())
    
    file_button.grid(column= 0,
                      row= 0,
                      padx = 20,
                      pady = (5,5))
    
    load_button = ttk.Button(data_frame,
                             text= 'Load File',
                             command= lambda: load_data())
    load_button.grid(column= 1,
                     row = 0,
                     padx = 20,
                     pady = (5,5))
    
    clear_button = ttk.Button(data_frame,
                              text= 'Clear Data',
                              command= lambda: clear_data())
    clear_button.grid(column = 2, row = 0, padx = 20)
    #data_label_frame = ttk.LabelFrame(data_frame,
    #                                  text= 'Selected File')
    #data_label_frame.grid(column= 1, 
    #                      row = 0,
    #                      padx = (10,10),
    #                      pady = (5,5))   
     

    path_label = ttk.Label(data_frame, text= 'No File Selected')
    path_label.grid(column = 3, row = 0, padx = (20,20), pady = (5,5))
    
    #Entry Frame in Window
    entry_frame = ttk.LabelFrame(window,
                                 text = 'Enter Item')
    entry_frame.grid(column = 0,
                     row = 1,
                     padx = (10,10),
                     pady= (5,5))    
    
    #Entry_Frame items, enter an item without dealing with the code
    #Name entry tab
    name_entry = ttk.Entry(entry_frame)
    name_entry.insert(0,'Item Name')
    name_entry.bind('<FocusIn>',
                    lambda e: name_entry.delete('0','end'))
    
    if name_entry.get() == '':
        name_entry.bind('<FocusOut>', 
                        lambda e: name_entry.insert(0,'Item Name'))
        
    name_entry.grid(column = 0,
                    row = 0,
                    padx = butt_padx,
                    pady= butt_pady,
                    sticky= 'ew')
    
    #brand entry tab
    brand_entry = ttk.Entry(entry_frame)
    brand_entry.insert(0,'Brand Name')
    brand_entry.bind('<FocusIn>',
                     lambda e: brand_entry.delete('0','end'))
    
    if brand_entry.get() == '':
        brand_entry.bind('<FocusOut>', 
                         lambda e: brand_entry.insert(0,'Brand Name'))
    brand_entry.grid(column = 1,
                     row = 0,
                     padx = butt_padx,
                     pady = butt_pady, 
                     sticky= 'ew')
    
    stock_spinbox = ttk.Spinbox(entry_frame, from_=1, to_=1000)
    stock_spinbox.grid(column= 2,
                       row = 0, 
                       sticky= 'ew', 
                       padx= 5,
                       pady= 5)
    stock_spinbox.insert(0, 'Stock')
    stock_spinbox.bind('<FocusIn>',
                       lambda e: stock_spinbox.delete('0','end'))
    
    if not stock_spinbox.get():
        stock_spinbox.bind('<FocusOut>',
                           lambda e: stock_spinbox.insert(0,'Stock'))
        
    #Units Dropdown box
    unit_drop = ttk.Combobox(entry_frame, 
                             values = unit_combo)
    unit_drop.grid(column= 3,
                   row = 0,
                   sticky = 'ew',
                   padx = 5,
                   pady = 5)
    unit_drop.current(0)
    
    #Insert button
    insert_button = ttk.Button(entry_frame,
                               text= 'Insert Item',
                               command = lambda: [insert_row(), entry_reset()])
    insert_button.grid(column = 4,
                       row = 0,
                       sticky= 'nsew',
                       padx = 5,
                       pady = 5)
    

    
    
    
    #Tree view frame
    treeFrame = ttk.Frame(window)
    
    treeFrame.grid(column = 0, row = 2, pady = 10)
    
    #scrollwheel
    treescroll = ttk.Scrollbar(treeFrame)
    treescroll.pack(side= 'right', fill = 'y')
    
    #treeview
    treeview = CheckboxTreeview(treeFrame, show= 'headings',
                            yscrollcommand=treescroll.set,
                            columns = col_heads,
                            height= 13)
    
    treeview.column('Name', width = 100)
    treeview.column('Brand', width= 100)
    treeview.column('Stock', width = 35)
    treeview.column('Units', width = 50)
    
    treeview.pack()
    
    #Light/Dark Mode Switch
    mode_switch = ttk.Checkbutton(window, 
                                  text= 'Mode',
                                  style= 'Switch',
                                  command= lambda: toggle_mode())
    mode_switch.grid(column = 0, row = 3, sticky = 'nsew')
    #Close Button, Closes the window
    close_button = ttk.Button(window,
                              text = 'Close',
                              command= lambda: close())
    close_button.grid(column = 0,
                      row = 4)
    
    if testing:
        testing_frame = tk.Frame(window)
        testing_frame.grid(column = 0, row = 5, pady = (10,10))
        
        df_button = ttk.Button(testing_frame, text= 'DataFrame Testing', command= lambda: df_test())
        df_button.grid(column= 0, row= 0)
    
    
    root.mainloop()
    
