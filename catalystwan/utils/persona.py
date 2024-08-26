# Copyright 2024 Cisco Systems, Inc. and its affiliates

from enum import Enum


class Persona(str, Enum):
    COMPUTE_AND_DATA = "COMPUTE_AND_DATA"
    COMPUTE = "COMPUTE"
    DATA = "DATA"
