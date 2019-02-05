#! /usr/bin/env python

def record_sink(sink_path):
    """Record an audio file using pysoundcard."""

    from aubio import sink, pitch
    from pysoundcard import Stream

    hop_size = 256
    duration = 5 # in seconds
    s = Stream(blocksize = hop_size, channels = 1)
    g = sink(sink_path, samplerate = int(s.samplerate))
    tolerance = 0.8
    downsample = 1
    win_s = 4096 // downsample # fft size
    hop_s = 512  // downsample # hop size
    pitch_o = pitch("yin", win_s, hop_s, s.samplerate)
    pitch_o.set_unit("Hz")
    pitch_o.set_tolerance(tolerance)

    s.start()
    total_frames = 0
    try:
        while total_frames < duration * s.samplerate:
            vec = s.read(hop_size)
            # mix down to mono
            mono_vec = vec.sum(-1) / float(s.channels[0])
            g(mono_vec, hop_size)
            pitch = pitch_o(mono_vec)[0]
            print("%f", pitch)
            total_frames += hop_size
    except KeyboardInterrupt:
        duration = total_frames / float(s.samplerate)
        print("stopped after %.2f seconds" % duration)
    s.stop()

if __name__ == '__main__':
    import sys
    record_sink(sys.argv[1])