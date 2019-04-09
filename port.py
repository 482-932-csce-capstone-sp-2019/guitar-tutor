import mido 
print(mido.get_input_names())
i = 0
for i in range(0,5):
    try:

        inport = mido.open_input('LoopBe Internal MIDI ' + str(i))
        i+=1
        break
    except:
        print(i)
        i+=1
        continue

while True:
    for msg in inport.__iter__():
        if msg.type == 'note_on':
            print(msg)
    msg = inport.receive()
    print(msg)
    mode = input("Would you like to learn a chord or play a tab?(Chord/Tab/Quit)")
    mode = mode.lower()
    if mode == "tab" or mode == "t":
        exit()
