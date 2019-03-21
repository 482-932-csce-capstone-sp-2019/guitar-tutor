import mido 

print(mido.get_input_names())
inport = mido.open_input('KOMPLETE KONTROL M32 MIDI 1')

for msg in inport.poll():
    print(msg)
    mode = input("Would you like to learn a chord or play a tab?(Chord/Tab/Quit)")
    mode = mode.lower()
    if mode == "tab" or mode == "t":
        exit()
