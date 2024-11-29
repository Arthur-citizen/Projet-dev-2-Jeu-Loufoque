from random import choice, randint
import tkinter as tk
from threading import Thread

class Simon:
    """An instance of a Super Simon game"""
    def __init__(self):
        """Initializes the various variables used by the game"""
        self.sequence = [] #The sequence that the player must be able to replicate
        self.super_simon = Thread(target = main_program) #The thread that will contain the program
        self.simon_gui_window = tk.Tk()
        self.simon_gui_window.title("Super Simon")

        #Initializes the buttons on the GUI
        self.square_image = tk.PhotoImage(width = 1, height = 1) # This fake square image will be put into the buttons to make them square.
        self.green_button = tk.Button(root, bg = 'black', image = square_image, width = 300, height = 300, command = lorem_ipsum())
        self.red_button = tk.Button(root, bg = 'black', image = square_image, width = 300, height = 300, command = lorem_ipsum())
        self.yellow_button = tk.Button(root, bg = 'black', image = square_image, width = 300, height = 300, command = lorem_ipsum())
        self.blue_button = tk.Button(root, bg = 'black', image = square_image, width = 300, height = 300, command = lorem_ipsum())
    
    def main_program(self):
        """The main program that coordinates the various functions of the class"""
        self.super_simon.start() #Starts a thread for the game
        self.simon_gui_window.mainloop()

        for round in randint(7, 15):
            add_unit_to_sequence()
            show_sequence_on_gui()

        # generates a sequence
        # shows it to the user
        # listens for the user to input and checks if it is correct
        # ends when the game is over


    def add_unit_to_sequence(self):
        """Adds an unit to the sequence"""
        buttons_list = ['Green', 'Red', 'Yellow', 'Blue']
        print(f"The sequence is currently: {self.sequence}")
        self.sequence.append(choice(self.buttons_list))
        print(f"The sequence is now: {self.sequence}")
    
    def show_sequence_on_gui(self):
        """Shows the saved sequence on the GUI"""
        print(f"Showing following sequence on GUI...\n{self.sequence}")
        for unit in self.sequence:
            if unit == 'Green':
                self.green_button.config(bg = 'green') # Green button get turned on.
                time.sleep(1) # Wait 1 second.
                self.green_button.config(bg = 'black') # Turn green button off.
            elif unit == 'Red':
                self.red_button.config(bg = 'red')
                time.sleep(1)
                self.red_button.config(bg = 'black')
            elif unit == 'Yellow':
                self.yellow_button.config(bg = 'yellow')
                time.sleep(1)
                self.yellow_button.config(bg = 'black')
            elif unit == 'Blue':
                self.blue_button.config(bg = 'blue')
                time.sleep(1)
                self.blue_button.config(bg = 'black')
            time.sleep(0.2) # Adds a delay after each unit of the sequence shown on the GUI.
        print(f"Done showing the sequence on GUI.\n")
    
    def listen_user_input(self):
        input_sequence = []
        print("This function is supposed to listen for user input then check it.")

game = Simon()
game.main_program()