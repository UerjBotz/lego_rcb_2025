notas_derrota = ["G4/4_",
                 "F#4/4_",
                 "F4/4_", 
                 "E4/3"]

notas_vitoria = [     
                      "E3/4", "E3/4",
               "R/4",  
                      "E3/4", 
               "R/4",  
                      "C3/4", "E3/4", 
               "R/4",
                      "G3/4",
 "R/4", "R/4", "R/4",
                      "G3/4",
 "R/4", "R/4", "R/4",
                      "C4/4",
        "R/4", "R/4",
                      "G3/4",
        "R/4", "R/4",
                      "E3/4", 
        "R/4", "R/4",
                      "A4/4",
               "R/4",  
                      "B4/4",
               "R/4",  
                      "A#4/4", "A4/4",
               "R/4",
                      "G3/3", "E3/3", "G3/3", "A4/4",
               "R/4",  
                      "F3/4", "G3/4",
               "R/4",  
                      "E3/4", 
               "R/4",  
                      "C3/4",
]
#! melhorar musiquinha vitória (mario), talvez só cortar

inicio = lambda hub: hub.speaker.beep(frequency=500, duration=100)
final  = lambda hub: hub.speaker.beep(frequency=250, duration=250)

inicio_calibracao = lambda hub: hub.speaker.beep(frequency=300, duration=100)
inicio_cabeca     = lambda hub: hub.speaker.beep(frequency=600, duration=100)

vitoria = lambda hub: hub.speaker.play_notes(notas_vitoria, tempo=220)
derrota = lambda hub: hub.speaker.play_notes(notas_derrota) #! ajustar tempo, etc