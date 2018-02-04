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

    #Validate response
    if(len(response.face_annotations)):
        firstFace = response.face_annotations[0]
    else:
        return (0, 0) #Return 0 if face not detected

    pan_angle = firstFace.pan_angle #side to side
    tilt_angle = firstFace.tilt_angle #up and down

    return (pan_angle, tilt_angle)
