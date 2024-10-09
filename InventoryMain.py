# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 19:43:41 2024

@author: Taylor Gibbons
"""
import os
import pandas as pd
import InventoryFunc as IF


"""
For this code, my goals are to:
    1. Make a set of code that will be easily ran and used to keep track of any sort of 
        inventory list. For this project, I will be adding things that I have in my kitchen
    2. Make a way to see the inventory list using a GUI and be able to add things or remove 
        items through it (??)
        
To do this, I am making a couple of steps that I should work on things to make it a little
more organized.

    1. Start working on the Inventory class that will set names, brands, numbers of items, units
        and eventually categories to keep track of if they are food, cleaning supplies, dishes, or 
        whatever else will be kept track of. 
    2. Start making a way for items to be made manually through the terminal. Ie, it should
        run and then be able to take my input, make an Inventory object and be able to keep
        track of it in a list or dataframe
    3. Have a way to save the information of the Inventory objects into a dataframe 
        which will then be saved into a .xlsx and a .pkl file.
    4. Take in the pkl file and recreate the list to be able to see the list created
        before. Eventually, I would like to be able to make a way so that the user can
        create their own filename so that they could keep track of several different lists.
        
        This could be a good way to keep track of different rooms of a house, like the kitchen,
        living room, bedroom, office, and so on. 
    5. 
    
    6?. Create a gui that will display the inventory list of items
"""

global item_list
global inv_df 


def eq_print():
    term_size = os.get_terminal_size()  
    print('=' * term_size.columns)

def pass_fail(bool) -> str:
    if bool == True:
        return 'PASS'
        
    else:
        return 'FAIL'
    
def testing():
    print('Starting Testing Methods:')
    eq_print()
    
    #Filepath Testing
    print('\tStarting Filepath Test:')
    print('\t\tSaving Filepath as: "Testing"')
    IF.save_filepath('Testing')
    #print(IF.get_filepath())
    file_test = (IF.get_filepath() == os.getcwd() + '/Testing')
    print('Filepath test: {}'.format(pass_fail(file_test)))
    
    eq_print()
    
    #Reading/Saving Test
    print('\tStarting Reading pkl Test:\n\t\tInputting A Non-Existent FileName: NonExisting.pkl')
    IF.read_list
    
    
    
def main():
    review_old = input('Would you like to see the previous list? (y/n): ')
    
    filename = 'InventoryList'
    IF.save_filepath(filename)
    if review_old == 'y':
        print('Loading Previously list: ' + filename)
        inv_df = IF.read_list()
        if inv_df.empty:
            new_inv =input('Inventory list is empty. Try making a new list? (y/n)')
        else:
            print('Previous List Has Been Loaded!')
            print(inv_df)
            
    
    elif new_inv == 'y' or review_old == 'n':
        item_list = IF.makeInventoryList()
    
        for i in item_list:
            i.desc()
            
    
    #print(f'Item_List: {item_list}')