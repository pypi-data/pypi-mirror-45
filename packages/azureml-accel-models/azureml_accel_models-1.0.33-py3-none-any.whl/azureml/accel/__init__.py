# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Accelerate deep neural networks on FPGAs with Project Brainwave."""
from azureml.accel.accel_container_image import AccelImageConfiguration, AccelContainerImage
from azureml.accel.accel_onnx_converter import AccelOnnxConverter
from azureml.accel.client import PredictionClient
from azureml.accel._version import VERSION

__version__ = VERSION

__all__ = [
    "AccelImageConfiguration",
    "AccelContainerImage",
    "AccelOnnxConverter",
    "PredictionClient"
]
