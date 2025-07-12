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
scene.range         = 3  # Smaller values zoom in closer

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

def drift_particles():
    global particles
    particles = []
    colors = [color.cyan, color.magenta, color.orange,
              color.green, color.red, color.yellow]
    for i in range(80):
        pos = vector(random()-0.5, random()-0.5, random()-0.5) * 2
        v   = vector(random()-0.5, random()-0.5, random()-0.5) * 0.05
        col = colors[i % len(colors)]
        min_r, max_r = 0.05, 0.08
        r   = min_r + (max_r - min_r)*random()
        p   = sphere(pos=pos, radius=r, color=col, emissive=True)
        particles.append([p, v])
    for t in range(50):         # longer duration
        rate(30)
        for p, v in particles:
            p.pos    += v
            p.opacity = max(0, p.opacity - 0.003)

def uncertainty_blink():    
    clear_scene()  # optional if needed before this display
    light_pulse = sphere(pos=vector(0,0,0), radius=0.2, color=color.green, emissive=True)
    for i in range(50):
        rate(30)
        light_pulse.color   = color.green if i%2==0 else color.cyan
        light_pulse.opacity = abs(sin(i * pi/6))
    light_pulse.visible = False
            
def dramatic_fade():
    clear_scene()  # optional if needed before this display
    fade_panel = box(pos=vector(0,0,0), size=vector(1000,1000,0.1), color=color.white, opacity=0, emissive=True)
    core_flash = sphere(pos=vector(0,0,0), radius=2, color=color.red, emissive=True)    
    i = 0
    while core_flash.radius > 0.1:  # stops when radius nears minimum
        rate(30)
        fade_panel.visible = True      
        fade_panel.opacity = min(1,i * 0.04 )
        fade_panel.size = vector(1000 - i*10, 1000 - i*10, 0.1 + i * 0.02)
        fade_panel.pos += vector(0, 0, -0.02)
        if i < 10:
            core_flash.opacity = 1
            core_flash.radius = 2
            core_flash.color = color.red
        elif i > 10:
            core_flash.opacity = max(0, core_flash.opacity - 0.05)
            core_flash.radius = max(0.1, core_flash.radius - 0.1)
        i += 1

 
def sphere_explosion():
    clear_scene()
    boom_label = label(pos=vector(0, 1, 0),
                   text="BOOM",
                   height=30,
                   color=color.red,
                   box=False,
                   opacity=1,
                   emissive=True)     
    blast = sphere(pos=vector(0,0,0), radius=0.1, color=color.yellow, emissive=True, opacity=1)
    
    for i in range(30):
        rate(60)
        blast.radius += 0.2           # rapid expansion
        blast.opacity = max(0, 1 - i * 0.05)
        blast.color = color.red if i % 2 == 0 else color.orange
        boom_label.opacity = max(0, boom_label.opacity - 0.05)  # Fade out text

    # Optional fragments (debris flare-out)
    fragments = []
    for _ in range(20):
        frag = sphere(pos=vector(0,0,0),
                      radius=0.05,
                      color=color.white,
                      emissive=True)
        v = vector(random()-0.5, random()-0.5, random()-0.5) * 0.5
        fragments.append([frag, v])

    for t in range(50):
        rate(30)
        for frag, v in fragments:
            frag.pos += v
            frag.opacity = max(0, frag.opacity - 0.02)
            
def clear_scene():
    for obj in list(scene.objects):
        obj.visible = False
        del obj
      
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
    sphere_explosion()
    uncertainty_blink()
    
    label(pos=vector(0, 2, 0),text="⚛️ U-238 TRANSMUTATION COMPLETE ⚛️",
                          height=24, color=color.black, box=False)
    
button_main = button(text="Start Process", bind=update_stage, color=color.red)
button_restart = button(text="restart", bind=restart_process,color=color.black)
button_quit=button(text="Quit", bind=end_session, color=color.black)
