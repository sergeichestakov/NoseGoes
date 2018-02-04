import io
import os

import google.cloud.vision

img_name = "myface.jpg"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./nosegoes.json"

vision_client = google.cloud.vision.ImageAnnotatorClient()

def getAnnotations(image):
    with io.open(image, "rb") as upload_file:
        content = upload_file.read()
    googleImage = google.cloud.vision.types.Image(content=content)
    response = vision_client.face_detection(image=googleImage)

    print ("Response: " + str(response.face_annotations))
    return response.face_annotations
