#!/usr/bin/python
# -*- coding: utf-8 -*-
"""A module for defining different kinds of neuronal learning."""
import abc
import numpy as np


class Learning(abc.ABC):
    """The base class for all learning functions."""

    @abc.abstractmethod
    def __call__(self, neurons):
        """Make the neurons learn.

        Args:
            neurons: The neurons to update
        """
        raise NotImplementedError()


class HebbianLearning(Learning):
    """A kind of learning that favors the connection of co-occurrenct neurons.

    'Neurons that fire together, wire together.'
    'Neurons that fire apart, wire apart'
    """

    def __init__(self, increase=0.05, decrease=0.002):
        """Initialize the Hebbian learning with appropriate constants.

        Args:
            increase: The amount by which to increase the synapse strengths
            decrease: The amount by which to decrease the synapse strengths
        """
        self.increase = increase
        self.decrease = decrease

    def __call__(self, neurons):
        """Make the neurons learn.

        Increase the weights on synapses where input and output were active.
        Decrease the weights on synapses where only the output was active.

        Args:
            neurons: The neurons to update
        """
        if neurons.passthrough:
            for layer in neurons.layers:
                self(layer)
            return

        output_values = neurons.output.values
        active_neurons = output_values == 1
        for input_name, input_unit in neurons.inputs.items():
            input_unit.synapses -= self.decrease
            input_unit.synapses[active_neurons,...] += self.increase
            input_unit.synapses = np.clip(input_unit.synapses, 0, 1)
