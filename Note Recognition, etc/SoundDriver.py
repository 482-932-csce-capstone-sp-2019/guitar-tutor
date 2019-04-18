from pysoundcard import Stream
import mido
import wave
import numpy as np
from aubio import pitch, onset

doneWithTab = False

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

def setDoneWithTab(state):
    global doneWithTab
    doneWithTab = state
	
def getDoneWithTab():
	global doneWithTab
	return doneWithTab

def getNoteDict():
	notelist = []

	file = open("noteslist.txt", "r")
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
	port = None
	portname = None
	s = None
	o = None
	p = None
	totalNotes = 0
	correctNotes = 0
	lx = 0
	def __init__(self):
		self.notelist = getNoteDict()
		#self.s = Stream(samplerate=RATE, blocksize=CHUNK)
		for i in range(0,5):
			try:

				inport = mido.open_input('LoopBe Internal MIDI ' + str(i))
				self.portname = 'LoopBe Internal MIDI ' + str(i)
				break
			except:
				print(i)
				i+=1
				continue
		self.o = onset("default", win_s, hop_s, RATE)
		self.p = pitch("yin", win_s, hop_s, RATE)
		self.p.set_unit("Hz")
		self.p.set_tolerance(tolerance)
		self.correctNotes = 0
		self.totalNotes = 0
		self.incorrectNotes = 0

	
	# while displaying the next note, wait for the new note to begin, and grade the currently held note
	def waitForOnset(self, next = []):
		print(len(next))
		self.currentNote = next
		print("cureentnote length:", len(self.currentNote))
		self.port = mido.open_input(self.portname)
		#print(next)
		print(len(next))
		totalLength = 0
		num_incorrect = 0
		#correctTone = 0
		#tp = self.notelist[self.currentNote] #target pitch		
		# In the absence of a do while loop, read, then begin looping
		#vec = self.s.read(CHUNK)
		#mono_vec = vec.sum(-1) / float(self.s.channels[0])
		# While we do not have a new onset
		# Possibly ignore onsets if they get a wrong note?
		
		while True:
			# if doneWithTab == True:
			# 	self.port.close()
			# 	exit()
			totalLength += 1
			# if we have a note, attempt to see if we are matching it
			#x = self.p(mono_vec)[0]
			#y = self.p.get_confidence()\
			ct = 1
			i = 0
			note = []
			for msg in self.port.__iter__():
				print("Length of notes played:", len(note))
				if getDoneWithTab():
					self.port.close()
					exit()
				if msg.type == 'note_on':
					print("Note played")
					note.append(msg)
					print(len(note))
					i += 1
					if i == len(self.currentNote):
						break
			print(note)
			print(self.currentNote)
			# if we are confident that we have a pitch and we have a note to compare to, start grading
			# also filter out possible silence, as this frequency is waaaay below a guitar's range
			sum_correct = 0
			if self.currentNote != [] and self.currentNote != None:
				# if they are within 10% of the target pitch, count it
				cs = self.currentNote
				
				for n in note:
					print("cs " + str(cs))
					print("Notes: " + str(list((n.note for n in note))))

					l1 = [n.note -1, n.note, n.note+1]
					intersect = set(l1).intersection(set(cs))
					if  len(intersect) >= 1:
						cs = list(set(cs) - set(intersect))
						sum_correct += 1
						print("correct:", sum_correct)
						if sum_correct == len(self.currentNote):
							print("breaking:", sum_correct)
							break
				ct += 1
				print(ct)
			if sum_correct == len(self.currentNote):
				break
			else:
				num_incorrect += 1
					
			# read again
			#vec = self.s.read(CHUNK)
			#mono_vec = vec.sum(-1) / float(self.s.channels[0])

		# advance to the currently displayed note
		self.totalNotes += 1
		# as long as the note was correct for half the time we heard it, count it
		# this can be fiddled with
		#self.lx = self.o.get_last_s()
		#port.panic()
		self.port.close()
		if totalLength != 0:
			self.correctNotes += 1
			self.incorrectNotes += num_incorrect
			return None, None, float(ct)/float(totalLength)
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