import pygame, mido, time
outport = mido.open_output("Virtual Port 1")

pygame.init()
pygame.joystick.init()

drum = pygame.joystick.Joystick(0)
drum.init()

#previous "button" states
prevleftmid = 0
prevrightmid = 0
prevleftside = 0
prevrightside = 0
prevselect = 0
prevstart = 0

while True:
    pygame.event.pump()

    leftmid = 0
    rightmid = 0
    leftside = 0
    rightside = 0
    select = 0
    start = 0

    numbuttons = drum.get_numbuttons()
    for i in range(numbuttons):
        if i == 15 and drum.get_button(15) == 1: #left mid
            leftmid = 1
        elif i == 1 and drum.get_button(1) == 1: #right mid
            rightmid = 1
        elif i == 6 and drum.get_button(6) == 1: #left side
            leftside = 1
        elif i == 7 and drum.get_button(7) == 1: #right side
            rightside = 1
        elif i == 8 and drum.get_button(8) == 1: #select (left button)
            select = 1
        elif i == 9 and drum.get_button(9) == 1: #start (right button)
            start = 1

    #calculate button deltas
    leftmiddledelta = (prevleftmid << 1) | leftmid
    rightmiddledelta = (prevrightmid << 1) | rightmid
    leftsidedelta = (prevleftside << 1) | leftside
    rightsidedelta = (prevrightside << 1) | rightside
    selectdelta = (prevselect << 1) | select
    startdelta = (prevstart << 1) | start

    deltas = [leftmiddledelta, rightmiddledelta, leftsidedelta, rightsidedelta, selectdelta, startdelta]

    for i in range(len(deltas)):
        if(deltas[i] == 0b01): #hit
            msg = mido.Message("note_on", note = (60 + i), velocity = 64)
            outport.send(msg)
            time.sleep(msg.time)
            print("note on at index " + str(i))
        elif(deltas[i] == 0b10): #release
            msg = mido.Message("note_off", note = (60 + i))
            outport.send(msg)
            time.sleep(msg.time)
            print("note off at index " + str(i))
        if((deltas[4] == 0b01 or deltas[4] == 0b11) and (deltas[5] == 0b01 or deltas[5] == 0b11)):
            quit()
