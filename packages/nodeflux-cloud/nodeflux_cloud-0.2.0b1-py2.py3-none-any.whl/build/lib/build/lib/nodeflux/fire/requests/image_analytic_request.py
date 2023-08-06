from datetime import datetime
from typing import List, Dict

from nodeflux.fire.requests.types import AnalyticTypes


class ImageAnalyticRequest:
    def __init__(
        self,
        image: bytes,
        analytics: List[AnalyticTypes],
        labels: Dict[str, str],
        timestamp: datetime,
    ):
        self.image = image
        self.analytics = analytics
        self.labels = labels
        self.timestamp = timestamp
