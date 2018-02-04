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

    bigIndex = 0
    bigArea = 0
    #Search for correct face
    for i in len(response.face_annotations):
        box = response.face_annotations[i].bounding_poly.vertices
        area = (box[2].x - box[0].x) * (box[2].y - box[0].y) 
        if area > bigArea:
            bigArea = area
            bigIndex = i

            
    firstFace = response.face_annotations[i]

    pan_angle = firstFace.pan_angle #side to side
    tilt_angle = firstFace.tilt_angle #up and down

    return (pan_angle, tilt_angle)
