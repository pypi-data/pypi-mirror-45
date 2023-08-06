from enum import IntEnum

from nodeflux.analytics.v1.analytic_pb2 import Analytic


class AnalyticTypes(IntEnum):
    EXTENSION = Analytic.EXTENSION
    FACE_DETECTION = Analytic.FACE_DETECTION
    FACE_DEMOGRAPHY = Analytic.FACE_DEMOGRAPHY
    FACE_ENROLLMENT = Analytic.FACE_ENROLLMENT
    FACE_RECOGNITION = Analytic.FACE_RECOGNITION
