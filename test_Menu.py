from tkinter import *
from PIL import Image, ImageTk

# Function to animate the GIF
def update_gif(frame_index):
    global gif_frames
    frame = gif_frames[frame_index]
    background_label.configure(image=frame)
    frame_index = (frame_index + 1) % len(gif_frames)  # Loop back to the first frame
    fenetre.after(100, update_gif, frame_index)  # Adjust the delay as needed

# Create the main window
fenetre = Tk()

# Load the animated GIF using Pillow
gif = Image.open("image/bg.gif")  # Replace with the path to your animated GIF
gif_frames = []

# Get all frames of the GIF
for i in range(gif.n_frames):
    gif.seek(i)  # Move to the i-th frame
    frame = ImageTk.PhotoImage(gif.copy())  # Create PhotoImage from the current frame
    gif_frames.append(frame)

# Create a Label for the GIF background
background_label = Label(fenetre, image=gif_frames[0])
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill the window

# Add your other widgets
porte = PhotoImage(file="image/porte_menu.png")
titre = Label(fenetre, text="Préparez vous pour un jeu renversant", background="black", font=("Arial", 15), fg="green")
titre1 = Label(fenetre, text="Ouvrez la porte",width=14 , background="black", font=("Arial", 15), fg="green")


def play():
    bouton1['text'] = 'ABCDEFGHIJKLM'

bouton1 = Button(fenetre, image=porte, bg="black", highlightthickness=0, border=0, activebackground="black")
titre.pack()
titre1.pack()
bouton1.pack()

# Set window properties
fenetre.title("Jeu de plateau Loufoque")
fenetre.geometry("540x540")

# Start the GIF animation
update_gif(0)

# Start the main event loop
fenetre.mainloop()
