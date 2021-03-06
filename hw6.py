#!/usr/bin/env python

"""
IT FDN 100 B: Intro to Python
James Butts
james.butts@gmail.com
Homework assignment 6
March 12, 2019

A script to maintain a list of tasks and their priority.

Present users menu options to list current data, add, delete, and save changes to the file.

Just like my assignment 5, except I've grouped my functions into a class.

Working data is loaded from the text file to a dictionary, changes are made in the dictionary, and then must be saved
using the menu option if the user wants the data to persist.

"""

class todo:

    def PrintMenu(self):

        print("\nWelcome to the To Do List tool. What would you like to do?:\n")
        print("1. Show current data")
        print("2. Add a new item")
        print("3. Remove an existing item")
        print("4. Save data to file")
        print("Or enter 'Q' to Quit")

    def GetItem(self, dict):

        response = ""
        # get user inputted task name
        task_item = str(raw_input("\nEnter the task: "))

        while True:
            try:
                # Get user-inputted task priority
                item_priority = str(raw_input("What is the priority of your " + task_item + " task: "))
                break
            except:
                pass

        print("\nYou entered:\n")
        print('Item' + " " * 17 + "Value" + " " * 15)
        print("=" * 20 + " " + "=" * 20)
        print('%-20s %-20s' % (task_item, item_priority))
        # Prompt user to add another item, only accept single character y/n
        while response.lower() not in ['y', 'n']:
            response = str(raw_input("\nAdd item to list? (Y/N): "))
            # if user agrees, add items to the dictionary
            if response.lower() == 'y':
              # Add item to dictionary
              dict.update({task_item: item_priority})

        return dict

    def SaveFile(self, dict, txtfile):
        """
        Create/overwrite file, write contents of dict to text file as CSV
        :param dict: working dictionary file from main
        :param txtfile: text file used to keep data persistent
        :return: None
        """

        f = open(txtfile, "w+")
        # W+ means for writing, create file if it doesn't exist, re-write existing file on save.
        for k, v in dict.items():
            f.writelines(k.strip(" ") + ", " + v.strip(" ") + "\n")
        f.close()

    def DisplayTodoFile(self, todo_file):
        """
        Write the contents of the inventory file to the user's screen
        Left justify text for each value, column width at 20 characters
        """

        # write out a header for the inventory table that matches the fixed-width spacing
        print("\n\nAll done, here are the current contents of your todo list file: \n")
        print('Item' + " " * 17 + "Priority" + " " * 12)
        print("=" * 20 + " " + "=" * 20 + "\n")

        f = open(todo_file)
        for line in f:
            print('%-20s %-20s' % (line.split(", ")[0], line.split(",")[1]))
        f.close()

    def DisplayTodoDict(self, dict):
        """
        Write the contents of the inventory dictionary to the user's screen
        Left justify text for each value, column width at 20 characters
        """

        # write out a header for the inventory table that matches the fixed-width spacing
        print("\n\nHere are the current contents of your todo list dictionary: \n")
        print('Item' + " " * 17 + "Priority" + " " * 12)
        print("=" * 20 + " " + "=" * 20)

        i = 0
        for k, v in dict.items():
            print('%-i. %-16s %-20s' % (i, k, v.strip("\n")))
            i += 1

    def populate_dict(self, txtfile):
        """
        Take a text file, containing comma-separated data as input. Add to a dictionary and then return the dictionary.
        :return: dictionary containing task list loaded from file passed as input.
        """
        dict = {}
        f = open(txtfile)
        for line in f:
            # strip the newline characters as we populate the dict object
            dict.update({line.split(", ")[0].strip("\n"): line.split(",")[1].strip("\n")})
        return dict
        f.close()

    def remove_item(self, dict):
        """
        :param dict: Take a dictionary object of tasks, display them, and allow user to select an item to delete from a menu
        handle empty dictionary and confirm delete selection
        this function deletes from the dictionary, but not the file, so a save from the main menu is required for persistence
        :return: return the updated dictionary.
        """
        response = ""
        item_to_remove_prompt = ""

        while item_to_remove_prompt.lower() != "q":

            self.DisplayTodoDict(dict)

            if len(dict) == 0:
                # handle empty dictionary with correct prompt
                item_to_remove_prompt = str(raw_input("\nNo items on the list, enter 'Q' to quit: "))
            else:
                # Get user selection for item to remove
                item_to_remove_prompt = str(raw_input("\nEnter item 0 through " + str(len(dict) - 1) + " or 'Q' to quit: "))
            try:
                dict.keys()[int(item_to_remove_prompt)] in dict
                while response.lower() not in ['y', 'n']:
                    response = str(raw_input("Delete " + dict.keys()[int(item_to_remove_prompt)] + "? (Y/N): "))
                    if response.lower() == 'y':
                        del dict[dict.keys()[int(item_to_remove_prompt)]]
            except:
                # re-prompt the user if input was invalid, or if user decided not to delete the task
                pass
        return dict

"""
A script to keep a task list. Maintain a list of tasks and their priority.

Here's the main input loop. Present users menu options to list current data, add, delete, and save changes to the file.

Working data is loaded from the text file to a dictionary, changes are made in the dictionary, and then must be saved
using the menu option if the user wants the data to persist.

"""

# Text file to store files for persistence -- Todo.txt, in the CWD
todo_file = "./ToDo.txt"

TodoList = todo() # get an instance of the todo class

todo_dict = TodoList.populate_dict(todo_file) # Grab the contents of the txt file into a dictionary

response = ""

while response.lower() != "q":

    # Write a menu to the screen giving the user numeric choices for functionality. 'q' to quit.

    TodoList.PrintMenu()
    response = str(raw_input("\nPlease enter your selection: "))

    if response == "1":
        # Print the dictionary to the users' screen
        TodoList.DisplayTodoDict(todo_dict)
    elif response == "2":
        # Walk the user through prompts to add a new item to the dictionary
        todo_dict = TodoList.GetItem(todo_dict)
    elif response == "3":
        # Walk the user through prompts to remove an item from the dictionary
        todo_dict = TodoList.remove_item(todo_dict)
    elif response == "4":
        # Save the contents of the dictionary to the text file, making changes persistent
        TodoList.SaveFile(todo_dict, todo_file)