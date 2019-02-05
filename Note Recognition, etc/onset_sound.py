#! /usr/bin/env python


def onsetActivator():
	from pysoundcard import Stream
	import wave
	import numpy as np
	from aubio import pitch, onset
	CHUNK = 1024
	CHANNELS = 1
	RATE = 44100
	RECORD_SECONDS = 10

	s = Stream(samplerate=RATE, blocksize=CHUNK)

	print("* recording")

	# Pitch
	tolerance = 0.8
	downsample = 1
	win_s = 4096 // downsample # fft size
	hop_s = 1024  // downsample # hop size

	o = onset("default", win_s, hop_s, RATE)
	lastTime = 0.00
	num_on = 0
	s.start()
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		vec = s.read(CHUNK)
		# mix down to mono
		mono_vec = vec.sum(-1) / float(s.channels[0])
		
		if o(mono_vec) and max(mono_vec) >= 0.07:
			x = o.get_last_s()
			if lastTime < x:
				num_on += 1
				lastTime = x
				print("%f" % num_on)

	print("* done recording")

	s.stop
	
if __name__ == "__main__":
    onsetActivator()