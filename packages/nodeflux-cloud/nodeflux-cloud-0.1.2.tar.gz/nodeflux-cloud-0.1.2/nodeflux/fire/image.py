from datetime import datetime
from typing import Dict

from nodeflux.fire.v1 import image_analytic_pb2


class Image:
    def __init__(
        self,
        data: bytes,
        labels: Dict[str, str] = None,
        timestamp: datetime = datetime.now(),
    ):
        metadata = image_analytic_pb2.ImageMetadata()
        metadata.labels = labels
        metadata.timestamp.FromDatetime(timestamp)

        self._image = image_analytic_pb2.Image(data=data, metadata=metadata)
