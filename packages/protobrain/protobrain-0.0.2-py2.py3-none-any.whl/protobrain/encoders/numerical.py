#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Module for numerical encoders."""
import math
import numpy as np
from protobrain import sensor


class NumericalEncoder(sensor.Encoder):
    """Base encoder for numerical types."""

    def __init__(self, min_value, max_value, length, sparsity=0.02):
        """Initialize the encoder.

        Args:
            min_value: The minimum value supported by this encoder
            max_value: The maximum value supported by this encoder
            length: The length of the encoded representation
            sparsity: The sparsity of the encoded representation
        """
        super().__init__(
            default_value=0,
            shape=(length,)
        )
        self.min = min_value
        self.max = max_value
        self.length = length
        self.sparsity = sparsity

    @property
    def range(self):
        """The range of values supported by this encoder."""
        return self.max - self.min


class SimpleEncoder(NumericalEncoder):
    """The simplest numerical encoder."""

    def encode(self, value):
        """Encode a value.

        The signal length is determined by the output length and the sparsity.
        The encoded value contains a band of activations of said length that
        slide across the representation.

        Args:
            value: The value to encode

        Returns:
            The encoded representation of the value
        """
        if not (self.min <= value <= self.max):
            raise ValueError('Value outside of the range of the encoder.')

        signal_length = math.ceil(self.sparsity * self.length)
        signal_range = self.length - signal_length
        signal_start = int((value - self.min) / self.range * signal_range)

        encoded_value = np.zeros(self.length)
        encoded_value[signal_start:signal_start + signal_length] = 1

        return encoded_value


class CyclicEncoder(NumericalEncoder):
    """A cyclic encoder, similar to the SimpleEncoder, but loops."""

    def encode(self, value):
        """Encode a value.

        The signal length is determined by the output length and the sparsity.
        The encoded value contains a band of activations of said length that
        slide across the representation and loop at the end.

        Args:
            value: The value to encode

        Returns:
            The encoded representation of the value
        """
        if not (self.min <= value <= self.max):
            raise ValueError('Value outside of the range of the encoder.')

        signal_length = math.ceil(self.sparsity * self.length)
        signal_range = self.length - 1
        signal_start = int((value - self.min) / self.range * signal_range)

        encoded_value = np.zeros(self.length)
        encoded_value[signal_start:signal_start + signal_length] = 1
        if signal_start + signal_length > self.length:
            spill_size = (signal_start + signal_length) % self.length
            encoded_value[:spill_size] = 1

        return encoded_value
