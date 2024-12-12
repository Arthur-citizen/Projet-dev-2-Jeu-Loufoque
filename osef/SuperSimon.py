import tkinter as tk
import random
import time
import threading

def lorem_ipsum():
    # This function does nothing and only serves as demonstration purpose in the code → Will be removed from the final product.
    return 0


# Main window creation.
root = tk.Tk() # Opens a window
root.title("Super Simon") # Titles the window
square_image = tk.PhotoImage(width = 1, height = 1) # This fake square image will be put into the buttons to make them square.

# Buttons
## Buttons initialisation
green_button = tk.Button(root, bg = 'black', image = square_image, width = 300, height = 300, command = lorem_ipsum())
red_button = tk.Button(root, bg = 'black', image = square_image, width = 300, height = 300, command = lorem_ipsum())
yellow_button = tk.Button(root, bg = 'black', image = square_image, width = 300, height = 300, command = lorem_ipsum())
blue_button = tk.Button(root, bg = 'black', image = square_image, width = 300, height = 300, command = lorem_ipsum())


## Position the various buttons in a grid
green_button.grid(row = 0, column = 0) # Top left
red_button.grid(row = 0, column = 1) # Top right
yellow_button.grid(row = 1, column = 0) # Bottom left
blue_button.grid(row = 1, column = 1) # Botton right

# Sequence
sequence = []

def add_unit_to_sequence():
    """Adds a unit to the sequence"""
    buttons_list = ['Green', 'Red', 'Yellow', 'Blue']
    sequence.append( random.choice(buttons_list) )
    print(f"Showing following sequence on GUI: {sequence}")

def show_sequence_on_gui():
    """Show the sequence on the GUI"""
    for unit in sequence:
        if unit == 'Green':
            green_button.config(bg = 'green') # Green button get turned on.
            time.sleep(1) # Wait 1 second.
            green_button.config(bg = 'black') # Turn green button off.
        elif unit == 'Red':
            red_button.config(bg = 'red')
            time.sleep(1)
            red_button.config(bg = 'black')
        elif unit == 'Yellow':
            yellow_button.config(bg = 'yellow')
            time.sleep(1)
            yellow_button.config(bg = 'black')
        elif unit == 'Blue':
            blue_button.config(bg = 'blue')
            time.sleep(1)
            blue_button.config(bg = 'black')
        time.sleep(0.2) # Adds a delay after each unit of the sequence shown on the GUI.

def user_inputing():
    """Lets the user input a sequence and listen to the entered items."""
    input_sequence = []
    def sequenceComparator(): # Compares the user's entered sequence with the global sequence.
        if input_sequence == sequence:
            return True
        else:
            return False
    
    # Function body
    waitForClick = tk.IntVar() # Waits for a user to click a button on the GUI
    
    
    

def main():
    '''Programme principal'''
    run = 0
    while run < 6:
        add_unit_to_sequence()
        show_sequence_on_gui()
        print("Capturing user input on GUI...")
        print("> ")
        print("NOTE: The user is supposed to enter a sequence here by pressing the buttons and the program checks if it is correct.")
        time.sleep(3)
        print("Submitted answer is correct. Proceeding.\n")
        lorem_ipsum() # A function must be added here to capture user input then compare it with the actual sequence.
        run += 1
    print("Done.")

# Starts the main program
thread = threading.Thread(target = main)
thread.start()

root.mainloop()



"""
sequenceLength = input("Enter the length of the sequence:\n> ")
print(f"Entered length = {sequenceLength}\n")
"""