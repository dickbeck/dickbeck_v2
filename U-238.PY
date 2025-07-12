import tkinter as tk
import time

from PIL import Image, ImageTk


# Define transmutation steps
steps = [
            ("Uranium-238 (U-238)", "Stable", "0 MeV absorbed", "None"),
            ("Uranium-239 (U-239)", "Neutron Absorption", "6.5 MeV absorbed", "Gamma photon"),
            ("Neptunium-239 (Np-239)", "Beta Decay", "0.05 MeV released", "Beta particle, Antineutrino"),
            ("Plutonium-239 (Pu-239)", "Beta Decay", "0.70 MeV released", "Beta particle, Antineutrino"),
            ("Plutonium-239 (Pu-239, Fissile)", "Ready for fission", "200 MeV per fission", "Gamma rays, Neutrons")
        ]

# Create main GUI window
root = tk.Tk()
root.title("Uranium-238 Transmutation")
root.geometry("500x600")
root.configure(bg="#f5f5f5")  # Light background

gif_path = "abstract-atom.gif"  # Replace with your downloaded GIF file
gif = Image.open(gif_path)
 

frames = [ImageTk.PhotoImage(gif.copy().convert("RGBA")) for _ in range(gif.n_frames)]

# Label to display GIF
label_gif = tk.Label(root, bg="#f5f5f5")
label_gif.pack(pady=10)

# Function to animate GIF
def update_gif(frame=0):
    label_gif.config(image=frames[frame])
    root.after(100, update_gif, (frame + 1) % len(frames))  # Loop through frames

# Start animation
update_gif()

# Step counter
step_index = 0

# Create labels for transmutation data
font_title = ("Arial", 16, "bold")
font_labels = ("Arial", 12)
font_buttons = ("Arial", 12, "bold")

label_title = tk.Label(root, text="U-238 Transmutation Process", font=font_title, fg="#007acc", bg="#f5f5f5")
label_title.pack(pady=10)

label_name = tk.Label(root, text="", font=font_labels, fg="black", bg="#f5f5f5")
label_name.pack()
label_process = tk.Label(root, text="Process:", font=font_labels, fg="green", bg="#f5f5f5")
label_process.pack()
label_energy = tk.Label(root, text="Energy Change:", font=font_labels, fg="red", bg="#f5f5f5")
label_energy.pack()
label_radiation = tk.Label(root, text="Radiation Product:", font=font_labels, fg="purple", bg="#f5f5f5")
label_radiation.pack()

def blink_text():
    current_color = label_process.cget("fg")
    new_color = "green" if current_color == "black" else "black"
    label_process.config(fg=new_color)  # Update text color
    root.after(900, blink_text)  # Repeat every 500ms

# Start blinking effect
blink_text()


# Function to update transmutation stages
def update_stage():
    global step_index, button_next

    if step_index < len(steps):
        name, process, energy, radiation = steps[step_index]
        label_name.config(text=name)
        label_process.config(text=f"Process: {process}")
        blink_text()
        label_energy.config(text=f"Energy Change: {energy}")
        label_radiation.config(text=f"Radiation Product: {radiation}")

        step_index += 1  # Move to next step
        if step_index < len(steps):
            button_next.config(text=f"Next Step ({step_index + 1})")  # Update button text
        else:
            button_next.config(text="Transmutation Complete")  # Final stage

# Function to restart the process
def restart_process():
    global step_index
    step_index = 0  # Reset counter
    button_next.config(text="Next Step (1)")
    update_stage()  # Restart transmutation sequence

# Buttons to progress, restart, and quit
button_next = tk.Button(root, text="Next Step (1)", font=font_buttons, bg="#007acc", fg="white", relief="raised", bd=3, command=update_stage)
button_next.pack(pady=10)

button_restart = tk.Button(root, text="Restart Process", font=font_buttons, bg="#ffcc00", fg="black", relief="raised", bd=3, command=restart_process)
button_restart.pack(pady=10)

button_quit = tk.Button(root, text="Quit", font=font_buttons, bg="red", fg="white", relief="raised", bd=3, command=root.destroy)
button_quit.pack(pady=10)

# Start GUI
update_stage()  # Initialize first stage
root.mainloop()
