import mido 
print(mido.get_input_names())
inport = mido.open_input('LoopBe Internal MIDI 1')
while True:
    for msg in inport.__iter__():
        print(msg)
    mode = input("Would you like to learn a chord or play a tab?(Chord/Tab/Quit)")
    mode = mode.lower()
    if mode == "tab" or mode == "t":
        exit()