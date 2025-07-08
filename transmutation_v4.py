Web VPython 3.2

from vpython import *
from random import random

fade_panel = box(
                 pos = scene.camera.pos + vector(0,0,-1),
                 size = vector(50,50,0.2),
                 color = color.black,
                 emissive = True,     # always pure black
                 shininess = 0,       # no silver highlights
                 opacity   = 0,       # start invisible
                 visible   = False    # start hidden
                )
fade_panel.visible = False

core_flash  = sphere(pos=vector(0,0,0), radius=0.2,
                     color=color.red, emissive=True, opacity=0)
light_pulse = sphere(pos=vector(0,0,0), radius=0.3,
                     color=color.cyan, emissive=True, opacity=0)

particles = []  # create the list before using it

steps = [
         ("Uranium-238 (U-238)", "Stable", "0 MeV absorbed", "None"),
         ("Uranium-239 (U-239)", "Neutron Absorption", "6.5 MeV absorbed", "Gamma photon"),
         ("Neptunium-239 (Np-239)", "Beta Decay", "0.05 MeV released", "Beta particle, Antineutrino"),
         ("Plutonium-239 (Pu-239)", "Beta Decay", "0.70 MeV released", "Beta particle, Antineutrino"),
         ("Plutonium-239 (Pu-239, Fissile)", "Ready for fission", "200 MeV per fission", "Gamma rays, Neutrons")
        ]

scene.camera.pos    = vector(0, 0, 10)
scene.camera.axis   = vector(0, 0, -10)
scene.range         = 4  # Smaller values zoom in closer

fade_panel.opacity = 0

# Setup the scene
scene.title = "U-238 Transmutation Process"
scene.background = color.white    
scene.caption = "  " 
 
flash = sphere(pos=vector(0, 0, 0), radius=0.4, color=color.yellow, emissive=True, opacity=0)

label_title = label(pos=vector(0, 2, 0), text="U-238 Transmutation", height=20, box=False, color=color.black)

step_index = 0

label_name      = label(pos=vector(0,  1.0, 0), text='name: 1', box=False,color=color.black, height=16)
label_name.visible = False
label_process   = label(pos=vector(0,  0.0, 0), text='Process: 1', box=False,color=color.red, height=18)
label_process.visible = False
label_energy    = label(pos=vector(0, -0.9, 0), text='EnergyChange', box=False, color=color.green, height=16) 
label_energy.visible = False
label_radiation = label(pos=vector(0, -1.8, 0), text='Radiation Product).',box=False,color=color.purple,height=16)
label_radiation.visible = False
label_completion = label(pos=vector(0, -2.8, 0), text='Radiation Product).',box=False,color=color.red,height=20)
label_completion.visible = False

status_text = wtext(text="")
status_text.text = "\n</b>Click Start Process button to begin the U-238 Transmutation.</b>\n\n "

def update_stage():
    global step_index
    if step_index < len(steps):
        name, process, energy, radiation = steps[step_index]
        label_name.text         =  f"{name}<br>"
        label_process.text      =  f"Process: {process} Step {step_index+1}\n<br>"  
        label_energy.text       =  f"Energy Change: {energy} <br>"  
        label_radiation.text    =  f"Radiation Product: {radiation}<br>"
 
        if step_index ==0:
            button_main.text = "Next Step"
            button_main.color = color.black
            label_name.visible = True
            label_process.visible = True
            label_energy.visible = True
            label_radiation.visible = True 
            status_text.text = "\n</b>Click Next Step button to continue.</b>\n\n "
        step_index += 1
        
        if step_index == len(steps):
            label_completion.text = "<b>Transmutation Complete</b>\n"
            status_text.text = "\n</b>Click Restrt button to restaet or the Quit button to quit.</b>\n\n "
            label_completion.visible = True
            button_main.text = "Complete"
            button_main.bind = None  # disables the button
            button_main.color = color.gray
            button_quit.visible = True
            button_restart.visible = True

def restart_process():
    global step_index 
    step_index = 0
    label_name.text = ""
    label_process.text = ""
    label_energy.text = ""
    label_radiation.text = ""
    status_text.text = "\n</b>Click Start Process button to restart.</b>\n\n "
    button_main.text = "Start Process"
    button_main.bind = update_stage
    label_completion.visible = False
                  
scene.ambient = color.white  # set your starting ambiance
scene.lights = []            # if you want to use custom lighting only

def drift_particles():
    global particles
    particles = []
    colors = [color.cyan, color.magenta, color.orange,
              color.green, color.red, color.yellow]
    for i in range(20):
        pos = vector(random()-0.5, random()-0.5, random()-0.5) * 2
        v   = vector(random()-0.5, random()-0.5, random()-0.5) * 0.05
        col = colors[i % len(colors)]
        p   = sphere(pos=pos, radius=0.07, color=col, emissive=True)
        particles.append([p, v])
    for t in range(200):         # longer duration
        rate(30)
        for p, v in particles:
            p.pos    += v
            p.opacity = max(0, p.opacity - 0.003)

def uncertainty_blink():
    for i in range(12):
        rate(20)
        light_pulse.color   = color.green if i%2==0 else color.cyan
        light_pulse.opacity = abs(sin(i * pi/6))
    light_pulse.visible = False
            
def dramatic_fade():
    global fade_panel
    fade_panel.visible = True
    for i in range(30):
        rate(25)
        
        forward = scene.camera.axis.norm()
        fade_panel.pos = scene.camera.pos + forward*1
        
        fade_panel.opacity = min(1,i * 0.04 )
        fade_panel.size = vector(50 + i, 50 + i, 0.1 + i * 0.02)
        fade_panel.pos += vector(0, 0, -0.02)
        if i == 10:
            core_flash.opacity = 1
            core_flash.radius = 1
            core_flash.color = color.white
        elif i > 10:
            core_flash.opacity = max(0, core_flash.opacity - 0.05)
            core_flash.radius = max(0.1, core_flash.radius - 0.1)

def end_session(evt):
    scene.title = "<b>Session Ended</b><br>"
    scene.caption = " "
    scene.ambient = color.red
    scene.lights = []
    fade_panel.opacity = 0

    # Hide labels
    label_name.visible = False
    label_process.visible = False
    label_energy.visible = False
    label_radiation.visible = False
    label_completion.visible = False
    label_title.visible = False
    drift_particles()
    dramatic_fade()
    fade_panel.visible = False
    uncertainty_blink()
    
    label(pos=vector(0, 2, 0),text="⚛️ U-238 TRANSMUTATION COMPLETE ⚛️",,
                          height=24, color=color.black, box=False)
    
button_main = button(text="Start Process", bind=update_stage, color=color.red)
button_restart = button(text="restart", bind=restart_process,color=color.black)
button_quit=button(text="Quit", bind=end_session, color=color.black)

