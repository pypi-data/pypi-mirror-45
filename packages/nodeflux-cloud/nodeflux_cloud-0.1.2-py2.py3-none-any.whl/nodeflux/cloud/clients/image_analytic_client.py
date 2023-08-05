import random
import time
from dataclasses import dataclass
from typing import List

from nodeflux.analytics.v1.analytic_pb2 import Analytic
from nodeflux.cloud.requests.types import AnalyticTypes
from nodeflux.cloud.transports import image_analytic_grpc_transport as ia
from nodeflux.cloud.v1 import image_analytic_pb2


@dataclass
class ImageAnalyticRequest:
    image: bytes
    analytics: List[AnalyticTypes]


class ImageAnalyticClient:
    def __init__(self, transport: ia.ImageAnalyticGrpcTransport = None) -> None:
        if transport:
            self.transport = transport
        else:
            self.transport = ia.ImageAnalyticGrpcTransport()

    def batch_image_analytic(self, requests: List[ImageAnalyticRequest]):
        batch = ia.BatchImageAnalyticRequest()
        for r in requests:
            image_analytic_request = batch.requests.add()
            image_analytic_request.image.data = r.image
            image_analytic_request.analytics.extend(
                [Analytic(type=a) for a in r.analytics]
            )

        return self.transport.batch_image_analytic(batch)
