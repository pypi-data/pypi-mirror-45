# Nodeflux Cloud Client Library for Python

### Installation

```
pip install nodeflux-cloud
```

### Usage

Set the environment variable `NODEFLUX_ACCESS_KEY` and `NODEFLUX_SECRET_KEY` to your keys.

```python
from nodeflux.cloud.clients import ImageAnalyticClient
from nodeflux.cloud.requests import ImageAnalyticRequest, AnalyticTypes

client = cloud.ImageAnalyticClient()

with open("some-image.jpg", "rb") as image_file:
    image_content = image_file.read()

requests = [
    ImageAnalyticRequest(
        image=image_content,
        analytics=[
            AnalyticTypes.FACE_DETECTION,
            AnalyticTypes.FACE_DEMOGRAPHY,
        ]
    )
]

response = client.batch_image_analytic(requests)
print(response)
```

## API Reference

#### class ImageAnalyticClient(transport=None)

Service that performs Nodeflux Cloud image analytics.

| Parameters  | Type                         | Description                                                           |
| ----------- | ---------------------------- | --------------------------------------------------------------------- |
| `transport` | `ImageAnalyticGrpcTransport` | Transport for the API call. The default transport uses gRPC protocol. |

**`batch_image_analytic`**

Run analytics to a batch of images.

| Parameters | Type                         | Description                                       |
| ---------- | ---------------------------- | ------------------------------------------------- |
| `requests` | `List[ImageAnalyticRequest]` | A batch of Nodeflux Cloud image analytic request. |

#### class ImageAnalyticRequest(image: bytes, analytics: List[AnalyticTypes])

Individual image request to be analyzed by Nodeflux Cloud.

| Parameters  | Type                  | Description                                       |
| ----------- | --------------------- | ------------------------------------------------- |
| `image`     | `bytes`               | Image to be analyzed in the Nodeflux Cloud.       |
| `analytics` | `List[AnalyticTypes]` | A list of analytics to be performed to the image. |

#### class AnalyticTypes

Enums of analytic types supported by Nodeflux Cloud.

| Enums                       | Description                                                |
| --------------------------- | ---------------------------------------------------------- |
| `FACE_DETECTION`            | Detect faces from an image.                                |
| `FACE_DEMOGRAPHY`           | Predict age and gender from faces in the image.            |
| `FACE_RECOGNITION`          | Search for similar faces in the face recognition database. |
| `VEHICLE_RECOGNITION`       | Detect vehicles from an image.                             |
| `LICENSE_PLATE_RECOGNITION` | Recognize license plate number of vehicles in an image.    |

#### class BatchmageAnalyticResponse

Response from Nodeflux Cloud image analytic request.

**`face_detections: List[FaceDetection]`**

If present, face detection analytic has completed successfully.

**`face_demographics: List[FaceDemography]`**

If present, face demography analytic has completed successfully.

**`face_recognitions: List[FaceRecognition]`**

If present, face recognition analytics has completed successfully.

**`vehicle_detections: List[VehicleDetection]`**

If present, vehicle detection analytics has completed successfully.

**`license_plate_recognitions: List[LicensePlateRecognition]`**

If present, license plate recognition analytics has completed successfully.

#### class FaceDetection

**`bounding_box: BoundingBox`**

Bounding box around the detected face.

**`confidence: float`**

Confidence of the face detection.

#### class FaceDemography

**`gender: Gender`**

Detected gender from a face.

**`gender_confidence: float`**

Confidence of gender detection

**`age_range: AgeRange`**

The estimated age range.

#### class FaceRecognition

**`candidates: List[FaceCandidate]`**

List of candidates that matches the requested face. If candidates is set, the face recognition analytic has been successful.

#### class FaceCandidate

**`id: int64`**

Unique id of the recognized face.

**`confidence: float`**

Confidence of the recognition.
