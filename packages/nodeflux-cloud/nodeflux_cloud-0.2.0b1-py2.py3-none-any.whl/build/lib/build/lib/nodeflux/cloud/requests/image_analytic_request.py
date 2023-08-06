from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional

from nodeflux.cloud.requests.types import AnalyticTypes


@dataclass
class ImageAnalyticRequest:
    image: bytes
    analytics: List[AnalyticTypes]
    labels: Optional[Dict[str, str]] = None
    timestamp: datetime = datetime.now()
