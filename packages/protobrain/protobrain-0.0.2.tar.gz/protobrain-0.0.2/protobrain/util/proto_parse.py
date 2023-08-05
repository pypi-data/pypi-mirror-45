#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Module for dealing with protobuf parsing.

Ths handles protobuf encoding and decoding for classes in the project.
"""
import numpy as np
from protobrain import neuron
from protobrain.encoders import numerical
from protobrain.proto import encoder_pb2
from protobrain.proto import experiment_pb2
from protobrain.proto import sdr_pb2
from protobrain.proto import snapshot_pb2


def decode_encoder(encoder_proto):
    """Obtain an instance of Encoder from a protobuf.

    Args:
        encoder_proto: The protobuf instance representing the encoder

    Returns:
        The encoder decoded from the protobuf
    """
    encoder = None
    if encoder_proto.type == encoder_pb2.Encoder.NUMERICAL_CYCLIC:
        ext = encoder_pb2.CyclicEncoder.cyclic_encoder
        encoder = numerical.CyclicEncoder(
            length=encoder_proto.shape[0],
            min_value=encoder_proto.Extensions[ext].min_value,
            max_value=encoder_proto.Extensions[ext].max_value
        )
    elif encoder_proto.type == encoder_pb2.Encoder.NUMERICAL_SIMPLE:
        ext = encoder_pb2.SimpleEncoder.simple_encoder
        encoder = numerical.SimpleEncoder(
            length=encoder_proto.shape[0],
            min_value=encoder_proto.Extensions[ext].min_value,
            max_value=encoder_proto.Extensions[ext].max_value
        )
    else:
        raise ValueError('Invalid configuration:\n' + str(encoder_proto))

    return encoder


def decode_neurons(neurons_proto):
    """Obtain an instance of Neurons from a protobuf.

    Args:
        neurons_proto: The protobuf instance representing the neurons

    Returns:
        The neurons decoded from the protobuf
    """
    layers = [neuron.Neurons(n) for n in neurons_proto.layer]
    return neuron.FeedForward(layers)


def decode_input(input_proto):
    """Obtain an instance of Input from a protobuf.

    Args:
        input_proto: The protobuf instance representing the input

    Returns:
        The input decoded from the protobuf
    """
    for inp in input_proto:
        yield getattr(inp, inp.WhichOneof('value'))


def encode_brain(brain, out=None):
    """Create a protobuf encoding a Brain snapshot.

    Args:
        brain: The brain to take a snapshot from
        out: An optional protobuf instance to populate

    Returns:
        The protobuf
    """
    brain_snapshot = out or snapshot_pb2.Snapshot()
    encode_sensor(brain.sensor, brain_snapshot.sensor)
    encode_neurons(brain.neurons, brain_snapshot.cortex)
    return brain_snapshot


def encode_sensor(sensor, out=None):
    """Create a protobuf encoding a Sensor snapshot.

    Args:
        sensor: The sensor to take a snapshot from
        out: An optional protobuf instance to populate

    Returns:
        The protobuf
    """
    sensor_snapshot = out or snapshot_pb2.SensorSnapshot()
    encode_sdr(sensor.values, sensor_snapshot.sdr)

    return sensor_snapshot


def encode_neurons(neurons, out=None):
    """Create a protobuf encoding a Neurons snapshot.

    Args:
        neurons: The neurons to take a snapshot from
        out: An optional protobuf instance to populate

    Returns:
        The protobuf
    """
    cortex = out or snapshot_pb2.CortexSnapshot()
    if neurons.passthrough:
        for layer in neurons.layers:
            encode_sdr(layer.values, cortex.sdr.add())
    else:
        encode_sdr(neurons.values, cortex.sdr.add())

    return cortex


def encode_sdr(values, out=None):
    """Create a protobuf encoding an SDR.

    Args:
        values: The binary values to convert into an SDR
        out: An optional protobuf instance to populate

    Returns:
        The protobuf
    """
    sdr = out or sdr_pb2.SparseDistributedRepresentation()
    sdr.shape.extend(values.shape)

    on_bits = np.flatnonzero(values)
    sdr.on_bits.extend(on_bits)

    return sdr
