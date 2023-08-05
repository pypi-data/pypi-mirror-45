import time

import cv2

from nodeflux.cloud.clients import ImageAnalyticClient
from nodeflux.cloud.requests import ImageAnalyticRequest, AnalyticTypes


def periodic_image_analytic(stream: str, interval: int):
    cap = cv2.VideoCapture(stream)
    client = ImageAnalyticClient()

    analytics = [
        AnalyticTypes.FACE_DETECTION,
        AnalyticTypes.FACE_DEMOGRAPHY,
        AnalyticTypes.FACE_RECOGNITION,
    ]
    last_retrieve = time.time()

    while True:
        cap.grab()

        if time.time() - last_retrieve > interval:
            _, frame = cap.retrieve()
            encoded_frame = cv2.imencode(".jpg", frame)[1].tostring()

            request = ImageAnalyticRequest(encoded_frame, analytics)
            response = client.batch_image_analytic([request])

            last_retrieve = time.time()


if __name__ == "__main__":
    periodic_image_analytic("some-video-stream", interval=1)
