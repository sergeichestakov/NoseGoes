import argparse
import datetime
import time
import cv2
import numpy as np
import modules.google_cloud_platform_query as gc_query
import modules.opencvTracking as tracker
from modules.gestureEngine import updateGesture
from modules.controlBrowser import Browser
from modules.speech import MicrophoneStream
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from threading import Thread

#Constant stream of video with browser actions and API calls based on gestures

RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

def processSpeech(browser, stream, client, streaming_config):
    audio_generator = stream.generator()
    requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

    responses = client.streaming_recognize(streaming_config, requests)
    try:
        for response in responses:
            if not response.results:
                continue

            # The `results` list is consecutive. For streaming, we only care about
            # the first result being considered, since once it's `is_final`, it
            # moves on to considering the next utterance.
            result = response.results[0]
            if not result.alternatives:
                continue

            # Display the transcription of the top alternative.
            transcript = result.alternatives[0].transcript
            if result.is_final:
                print(transcript)
                if "open" in transcript and "tab" in transcript:
                    browser.openTab()
                elif "go" in transcript:
                    if "to" in transcript:
                        words = transcript.lstrip().split(' ')
                        name = (' ').join(words[2:len(words)])
                        browser.openWebsite(name)
                    elif "back" in transcript:
                        browser.back()
                    elif "forward" in transcript:
                        browser.forward()
                elif "search" in transcript:
                    words = transcript.lstrip().split(' ')
                    words.remove("search")
                    query = (' ').join(words)
                    browser.search(query)
    except Exception as e:
        print(e)
    processSpeech(browser, stream, client, streaming_config)

def run(camera, browser, current_time, microphone, client, streaming_config):
    prevDirection = ''
    horizontal = ['left', 'right']
    vertical = ['up', 'down']
    with microphone as stream:
        speechProcessor = Thread(target=processSpeech, args=(browser, stream, client, streaming_config))
        speechProcessor.start()
        while(True):
            # capture frame-by-frame
            ret, frame = camera.read()
            delta = time.time() - current_time
            # Display the resulting frame
            cv2.imwrite("./assets/videoframe.jpg", frame)
            #Detect the face and look for changes in gestures
            try:
                rect = tracker.faceDetect(frame)
                direction = updateGesture(frame, rect)

                if prevDirection is "up" or prevDirection is "down":
                    if delta > 0.5:
                        browser.scroll(prevDirection)
                        current_time = time.time()
                #Determine browser action based on gesture
                if direction is not prevDirection and direction is not "":
                    if direction in horizontal:
                        browser.switchTabs(direction)
                    elif direction in vertical:
                        browser.scroll(direction)
                        current_time = time.time()

                if direction is not "":
                    prevDirection = direction

            except Exception as e:
                print('ERROR:', e)

            cv2.imshow('frame', frame)

            #Quit with 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return

def close(camera, browser):
    browser.close()
    camera.release()
    cv2.destroyAllWindows()

def main():
    #open browser
    language_code = 'en-US'  # a BCP-47 language tag
    browser = Browser()
    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    microphone = MicrophoneStream(RATE, CHUNK)

    camera = cv2.VideoCapture(0)
    #modules.speech.main()
    run(camera, browser, time.time(), microphone, client, streaming_config)

    close(camera, browser)

if __name__ == "__main__":
    main()
