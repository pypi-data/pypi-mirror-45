from nodeflux.cloud.clients import ImageAnalyticClient
from nodeflux.cloud.requests import ImageAnalyticRequest, AnalyticTypes

client = ImageAnalyticClient()

with open("some-image.jpg", "rb") as image_file:
    image_content = image_file.read()

requests = [
    ImageAnalyticRequest(
        image_content,
        [
            AnalyticTypes.FACE_DETECTION,
            AnalyticTypes.FACE_DEMOGRAPHY,
            AnalyticTypes.FACE_RECOGNITION,
        ],
    )
]

response = client.batch_image_analytic(requests)
face_detections = response.face_detections
face_demographics = response.face_demographics
face_recognition = response.face_recognition
