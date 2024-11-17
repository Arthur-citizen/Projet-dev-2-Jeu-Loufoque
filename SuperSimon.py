import tkinter as tk
import random
import time
import threading

def loremIpsum():
    # This function does nothing and only serves as demonstration purpose in the code → Will be removed from the final product.
    return 0


# Main window creation.
root = tk.Tk() # Opens a window
root.title("Super Simon") # Titles the window
squareImage = tk.PhotoImage(width = 1, height = 1) # This fake square image will be put into the buttons to make them square.

# Buttons
## Buttons initialisation
greenButton = tk.Button(root, bg = 'black', image = squareImage, width = 300, height = 300, command = loremIpsum())
redButton = tk.Button(root, bg = 'black', image = squareImage, width = 300, height = 300, command = loremIpsum())
yellowButton = tk.Button(root, bg = 'black', image = squareImage, width = 300, height = 300, command = loremIpsum())
blueButton = tk.Button(root, bg = 'black', image = squareImage, width = 300, height = 300, command = loremIpsum())


## Position the various buttons in a grid
greenButton.grid(row = 0, column = 0) # Top left
redButton.grid(row = 0, column = 1) # Top right
yellowButton.grid(row = 1, column = 0) # Bottom left
blueButton.grid(row = 1, column = 1) # Botton right

# Sequence
sequence = []

def addUnitToSequence(): # Adds a unit to the sequence
    buttonsList = ['Green', 'Red', 'Yellow', 'Blue']
    sequence.append( random.choice(buttonsList) )
    print(f"Showing following sequence on GUI: {sequence}")

def showSequenceOnGUI(): # Shows the sequence on the GUI
    for unit in sequence:
        if unit == 'Green':
            greenButton.config(bg = 'green') # Green button get turned on.
            time.sleep(1) # Wait 1 second.
            greenButton.config(bg = 'black') # Turn green button off.
        elif unit == 'Red':
            redButton.config(bg = 'red')
            time.sleep(1)
            redButton.config(bg = 'black')
        elif unit == 'Yellow':
            yellowButton.config(bg = 'yellow')
            time.sleep(1)
            yellowButton.config(bg = 'black')
        elif unit == 'Blue':
            blueButton.config(bg = 'blue')
            time.sleep(1)
            blueButton.config(bg = 'black')
        time.sleep(0.2) # Adds a delay after each unit of the sequence shown on the GUI.

def userInputing(): # Lets the user input.
    inputSequence = []
    def sequenceComparator(): # Compares the user's entered sequence with the global sequence.
        if inputSequence == sequence:
            return True
        else:
            return False
    
    # Function body
    waitForClick = tk.IntVar() # Waits for a user to click a button on the GUI
    
    
    

def main():
    '''Programme principal'''
    run = 0
    while run < 6:
        addUnitToSequence()
        showSequenceOnGUI()
        print("Capturing user input on GUI...")
        print("> ")
        print("NOTE: The user is supposed to enter a sequence here by pressing the buttons and the program checks if it is correct.")
        time.sleep(3)
        print("Submitted answer is correct. Proceeding.\n")
        loremIpsum() # A function must be added here to capture user input then compare it with the actual sequence.
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