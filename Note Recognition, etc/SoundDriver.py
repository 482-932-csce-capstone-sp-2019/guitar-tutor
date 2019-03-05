from pysoundcard import Stream
import wave
import numpy as np
from aubio import pitch, onset

# Just using global constants for now
# Magic numbers be damned, this is easier for right now
CHUNK = 1024
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10

tolerance = 0.15
tuningTolerance = 0.02
downsample = 1
win_s = 4096 // downsample # fft size
hop_s = 1024  // downsample # hop size

def getNoteDict():
	notelist = []

	file = open("../noteslist.txt", "r")
	for line in file:
		x = line.split()
		notelist.append(float(x[1]))
	file.close()
	i = 0
	for a in notelist:
		#print("%f Hz at index %d" % (a, i))
		i += 1
	return notelist

class NoteRecognizer():
	notelist = []
	currentNote = -1
	s = None
	o = None
	p = None
	totalNotes = 0
	correctNotes = 0
	lx = 0
	def __init__(self):
		self.notelist = getNoteDict()
		self.s = Stream(samplerate=RATE, blocksize=CHUNK)
		self.o = onset("default", win_s, hop_s, RATE)
		self.p = pitch("yin", win_s, hop_s, RATE)
		self.p.set_unit("Hz")
		self.p.set_tolerance(tolerance)
		self.correctNotes = 0
		self.totalNotes = 0

	
	# while displaying the next note, wait for the new note to begin, and grade the currently held note
	def waitForOnset(self, next = -1):
		totalLength = 0
		correctTone = 0
		tp = self.notelist[self.currentNote] #target pitch		
		# In the absence of a do while loop, read, then begin looping
		vec = self.s.read(CHUNK)
		mono_vec = vec.sum(-1) / float(self.s.channels[0])
		# While we do not have a new onset
		# Possibly ignore onsets if they get a wrong note?
		while not ((self.o(mono_vec) and max(mono_vec) >= 0.07)):
			# if we have a note, attempt to see if we are matching it
			x = self.p(mono_vec)[0]
			y = self.p.get_confidence()
			
			# if we are confident that we have a pitch and we have a note to compare to, start grading
			# also filter out possible silence, as this frequency is waaaay below a guitar's range
			if self.currentNote != -1 and self.currentNote != None and y >= 0.9 and x >= 10.0:
				totalLength += 1
				# if they are within 10% of the target pitch, count it
				if tp - tp*tuningTolerance <= x <= tp + tp*tuningTolerance:
					correctTone += 1
					
			# read again
			vec = self.s.read(CHUNK)
			mono_vec = vec.sum(-1) / float(self.s.channels[0])

		# advance to the currently displayed note
		self.currentNote = next
		self.totalNotes += 1
		# as long as the note was correct for half the time we heard it, count it
		# this can be fiddled with
		self.lx = self.o.get_last_s()
		if totalLength != 0:
			self.correctNotes += 1
			return totalLength, correctTone, float(correctTone)/float(totalLength)
		return None, None, None
		
if __name__ == "__main__":
	a = NoteRecognizer()
	x = 0
	a.s.start()
	while True:
		b, c, d = a.waitForOnset(28)
		if b != None:
			print("Info")
			print(b)
			print(c)
			print(d)			
		print(x)
		x += 1
		print("Listening")
	a.s.stop()