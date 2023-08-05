# Copyright 2018 PT Nodeflux Teknologi Indonesia.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
    nodeflux.cloud.transports.image_analytic_grpc_transport
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements the gRPC transport for ImageAnalytic API.
"""

import grpc

from nodeflux.cloud.auth.credentials import Credentials
from nodeflux.cloud.transports.grpc_auth import AuthMetadataPlugin
from nodeflux.cloud.v1.image_analytic_pb2 import BatchImageAnalyticRequest
from nodeflux.cloud.v1.image_analytic_pb2_grpc import ImageAnalyticStub


class ImageAnalyticGrpcTransport:  # pylint: disable=too-few-public-methods
    def __init__(
        self,
        channel: grpc.Channel = None,
        credentials: Credentials = None,
        address: str = "api.nodeflux.io",
    ):
        if channel is not None and credentials is not None:
            raise ValueError(
                "The `channel` and `credentials` arguments are mutually " "exclusive."
            )

        if credentials is None:
            credentials = Credentials()

        if channel is None:
            channel_credentials = self._create_call_credentials(credentials)
            channel = grpc.secure_channel(address, channel_credentials)

        self._channel = channel
        self._stub = ImageAnalyticStub(self._channel)

    def _create_call_credentials(
        self, credentials: Credentials
    ) -> grpc.CallCredentials:
        ssl_credentials = grpc.ssl_channel_credentials()

        metadata_plugin = AuthMetadataPlugin(credentials)
        auth_credentials = grpc.metadata_call_credentials(metadata_plugin)

        return grpc.composite_channel_credentials(ssl_credentials, auth_credentials)

    def batch_image_analytic(self, batch_request: BatchImageAnalyticRequest):
        return self._stub.BatchImageAnalytic(batch_request)
