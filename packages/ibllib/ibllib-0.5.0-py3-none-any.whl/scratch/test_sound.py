import sounddevice as sd
import numpy as np
import time
devices = sd.query_devices()
#sd.default.device = [(i, d) for i, d in enumerate(devices) if 'XONAR SOUND CARD(64)' in d['name']][0][0]
#sd.default.device = 6
sd.default.latency = 'low'
sd.default.channels = 2
sd.default.samplerate = 192000

myarray = np.ones((19200,2))*0.99
tone_duration = 2

tvec = np.linspace(0, tone_duration, tone_duration * 192000)
tone = 0.05 * np.sin(2 * np.pi * 5000 * tvec)  # tone vec

sd.play(np.array([tone, tone]).T)