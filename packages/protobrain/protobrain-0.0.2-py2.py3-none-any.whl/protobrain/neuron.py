#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Module dealing with Neurons."""
import numpy as np
import logging
from protobrain import computation
from protobrain import synapses


log = logging.getLogger(__name__)


class Neurons(object):
    """Class representing neurons."""

    MAIN_INPUT = 'main'

    def __init__(self, units, computation_function=None):
        """Initialize the neurons.

        Args:
            units: Either a number of internal units or a list of layers
            computation_function: The computation to use to obtain the outputs
        """
        self.passthrough = isinstance(units, (list, tuple, Neurons))
        if self.passthrough:
            self.layers = getattr(units, 'layers', units)
            self.inputs = self.layers[0].inputs
            if self.inputs[Neurons.MAIN_INPUT].connected:
                log.warning(
                    'Creating Neurons with pre-connected input'
                )

            self.output = self.layers[-1].output

            internal_computations = self.recursive_retrieve_computations()
            if computation_function and any(internal_computations):
                log.warning(
                    'Overriding computation functions: [\n\t%s]->%s',
                    '\n\t'.join([repr(c) for c in internal_computations]),
                    computation_function
                )
        else:
            self.inputs = {
                Neurons.MAIN_INPUT: synapses.Input(
                    Neurons.MAIN_INPUT,
                    shape=(units,)
                )
            }
            self.output = synapses.Output(shape=(units,))

        self._computation = computation_function

    def recursive_retrieve_computations(self):
        """Get the computations used in the sub-layers."""
        computations = []
        if self.passthrough:
            for layer in self.layers:
                computations.extend(layer.recursive_retrieve_computations())
        else:
            computations.append(self._computation)

        return computations

    @property
    def input(self):
        """Get the main input."""
        return self.get(Neurons.MAIN_INPUT)

    @input.setter
    def input(self, output):
        """Connect the main input to the given output."""
        self.set(Neurons.MAIN_INPUT, output)

    def get(self, name):
        """Get an input to these neurons by name."""
        if name not in self.inputs:
            raise IndexError(
                '{0} not set as an input for {1}'.format(
                    name, repr(self)
                ))
        return self.inputs[name]

    def set(self, name, output):
        """Connect an input to the given output."""
        if name not in self.inputs:
            self.inputs[name] = synapses.Input(name, shape=self.input.shape)

        self.inputs[name].connect(output)

    def compute(self, computation_function=None):
        """Compute the output of this neuron."""
        computation_function = computation_function or self._computation
        if self.passthrough:
            for layer in self.layers:
                layer.compute(computation_function)
        else:
            if computation_function is None:
                log.critical('Missing computation function')
            self.output.values = computation_function(**self.inputs)

    @property
    def values(self):
        """The values at the output of these neurons."""
        return self.output.values

    @property
    def shape(self):
        """The shape of the output of these neurons."""
        return self.output.shape


def FeedForward(layers, input_name='main'):
    """Connect all the layers in a feed forward fashion.

    Each layer's output will be connected to the next layer's input
    matching the given name.

    Args:
        input_name: The input to which to connect

    Returns:
        A Neurons object containing the layers
    """
    for i, layer in enumerate(layers[:-1]):
        layers[i + 1].set(input_name, layer)

    return Neurons(layers)


def FeedBackward(layers, input_name=None):
    """Connect all the layers in a feed backward fashion.

    Each layer's output will be connected to the previous layer's input
    matching the given name.

    Args:
        input_name: The input to which to connect

    Returns:
        A Neurons object containing the layers
    """
    for i, layer in enumerate(layers[:-1]):
        layer.set(input_name, layers[i + 1])

    return Neurons(layers)


def LoopBack(layers, input_name=None):
    """Connect all the layers in a loop back fashion.

    Each layer's output will be connected to their own input
    matching the given name.

    Args:
        input_name: The input to which to connect

    Returns:
        A Neurons object containing the layers
    """
    for layer in layers:
        layer.set(input_name, layer)

    return Neurons(layers)
