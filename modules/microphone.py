import speech_recognition as sr
from time import sleep
from threading import Thread
from queue import Queue
import os

class MicrophoneStream:

    WIT_AI_KEY = os.environ['WIT_AI_KEY']
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.audio_queue = Queue()

    def recognize_worker(self):
        while True:
            audio = self.audio_queue.get()
            if audio is None: break
            try:
                print(self.recognizer.recognize_wit(audio, key=MicrophoneStream.WIT_AI_KEY))
            except sr.UnknownValueError:
                print('Unable to understand')
            except sr.RequestError as e:
                print("Could not request results from Wit.ai service; {0}".format(e))

            self.audio_queue.task_done()  # mark the audio processing job as completed in the queue

    def listen(self):
        # start a new thread to recognize audio, while this thread focuses on listening
        recognize_thread = Thread(target=self.recognize_worker)
        recognize_thread.daemon = True
        recognize_thread.start()
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                while True:  # repeatedly listen for phrases and put the resulting audio on the audio processing job queue
                    self.audio_queue.put(self.recognizer.listen(source))
            except KeyboardInterrupt:  # allow Ctrl + C to shut down the program
                pass

        self.audio_queue.join()  # block until all current audio processing jobs are done
        self.audio_queue.put(None)  # tell the recognize_thread to stop
        recognize_thread.join()  # wait for the recognize_thread to actually stop

if __name__ == "__main__":
    m = MicrophoneStream()
    m.listen()
