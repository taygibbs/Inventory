# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 17:29:04 2024

@author: Taylor Gibbons
"""

import pandas as pd
import os

#Global Variables


#Sets the filepath gbl variable
def save_filepath(filename: str):
    """
    Initializes the global filepath

    Parameters
    ----------
    filename : str
        The name of the inventory list file.

    """
    
    global filepath 
    filepath = filename
   
    
#returns the gbl variable filepath
def get_filepath():
    """
    Returns the filepath

    """
    
    return filepath

def get_filename() -> str:
    for i in range(len(get_filepath()), 0, -1):
        if i == '/':
            return filepath[i+1:]
        else:
            continue
#Reads in the previous list (in pkl format)

def read_list(*args) -> pd.DataFrame:
    """
    Reads previous lists

    Returns
    -------
    df : PANDAS DataFrame
        A dataframe with the information of the previously made list.

    """
    if len(args) > 1:
        print('Too many arguments. Only 1 is allowed (filename)')
    else:
        save_filepath(args[0])
        #filepath_excel =  filepath + '.xlsx'
        filepath_pkl = filepath + '.pkl'
        
        try:
            df = pd.read_pickle(filepath_pkl)
        except FileNotFoundError:
            print('File not Found. Make a new list or make sure you inputted the right filename!')
            
        except UnboundLocalError as ULE:
            print(ULE )
        else:        
            return df
    #Should this be where the df gets turned into the inventory items or should it be okay to leave it in DF form?


    
class Inventory:
    
    def __init__(self, name: str, brand: str, in_stock: int, unit: str):
        """
        Initialize the Inventory object

        Parameters
        ----------
        name : str
            Name of item.
        brand : str
            Brand name.
        in_stock : int
            Number of items in stock.
        unit : str
            The units of each item (ie, bags, pieces, gallons, etc...).

        """
        
        self.name = name
        self.brand = brand
        self.stock = in_stock
        self.unit = unit
        

    def to_dict(self) -> dict:
        """
        Makes a dictionary of the Inventory instance variable

        Returns
        -------
        dict
            the dictionary of the inventory variable. This includes the name, brand, number of items and units.

        """
        
        print('Making a DataFrame:')
        return {'name': self.name, 'brand':self.brand, 'stock': self.stock,'unit':self.unit}
        
        
    def desc(self):
        """
        Prints a description of the Inventory instance variable

        """
        
        print('Item Name: ' + self. brand + ' ' +self.name)
        print('Number and units: ' + self.stock + ' ' + self.unit)
    
    def item_remove(self,rem: int):
        """
        Subtracts an indicated number from the current Inventory variable stock

        Parameters
        ----------
        rem : int
            the number to remove from the variable stock.


        """
        
        self.stock -= rem
        
    def item_add(self, add: int):
        """
        Adds an indicated number to the current Inventory variable stock

        Parameters
        ----------
        add : int
            Number to add to the variable stock.

        Returns
        -------
        None.

        """
        
        self.stock += add
        
    
def save_df(df: pd.DataFrame):
    """
    Saves the parameter dataframe into  a .pkl and .xlsx.
    Typically will be the last thing called (??)
    
    Parameters
    ----------
    df : DataFrame
        The dataframe of all the information from Inventory objects
    """
    
    filepath_pkl = filepath + '.pkl'
    pd.to_pickle(df, filepath_pkl)
    pd.to_excel(df,filepath + '.xlsx')

def to_df(item_list: list[Inventory]) -> pd.DataFrame:
    """
    Makes a PANDAS DataFrame of the information from the Inventory Objects

    Parameters
    ----------
    item_list : list[Inventory]
        list of Inventory Objects.

    Returns
    -------
    df : PANDAS DataFrame
        A dataframe of the Inventory Object information.

    """
    
    df = pd.DataFrame.from_records([s.to_dict() for s in item_list])     
    
    return df


def add_df(df: pd.DataFrame, item: Inventory)-> pd.DataFrame:
    """
    Adds a row to a previously made dataframe

    Parameters
    ----------
    df : pd.DataFrame
        Previously made DataFrame with Inventory Object Information.
    item : Inventory
        Inventory Object to be added to the dataframe.

    Returns
    -------
    df : pd.DataFrame
        A DataFrame with the og info and the newly added Inventory Object info.

    """
    
    df = pd.concat([pd.DataFrame([item.to_dict()],columns = df.columns),df], ignore_index = True)  
    
    return df


def makeInventoryList() -> list[Inventory]:
    """
    Main function to make Inventory Objects and will allow the user to make a list with any amount of items.

    Returns
    -------
    list[Inventory]
        A list of all the Inventory objects made.

    """
    
    item_list = []
    name = None
    try:
        name, brand, stock, unit = input('Input the name of item, brand, number, and units (separated by a comma) If exitting, enter None: ').split(', ',)
        while name:
            
            dynamic_variable_name = name.lower()
            locals()[dynamic_variable_name] = Inventory(name,brand,stock,unit)
            item_list.append(dynamic_variable_name)
            if input('Add another item? (y/n)') == 'y':
                name,brand,stock,unit = input('Input Name, Brand, # of units, Unit: ')
            else:
                name = None
    except TypeError: 
        print('Wrong Data Type: ' + TypeError)
    except ValueError:
        print('Not enough information. Enter all of the data.')
        
    save_df(item_list)
    
    return item_list


def remakeInventoryList(df: pd.DataFrame) -> list[Inventory]:
    """
    In the case that items from a previous list should be remade into Inventory Object, this will
    take in the datframe and remake each row into its own object, then return a list of the objects.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe of the previously made list.

    Returns
    -------
    list[Inventory]
        A list of the Inventory Objects.

    """
    
    item_list = []
    items = 0
    for ind, row in df.iterrows():
        print(row)
        dynamic_var_name = row.name    
        locals()[dynamic_var_name] = Inventory(row.name,row.brand,row.stock,row.unit)
        items += 1
        item_list.append(dynamic_var_name)
        
    return item_list
    

