#!/usr/bin/python
# -*- coding: utf-8 -*-
"""A module for defining different kinds of neuronal computations."""
import abc
import numpy as np


class Computation(abc.ABC):
    """Base class for all other computations to inherit from."""

    @abc.abstractmethod
    def __call__(self):
        """Compute the neurons' output."""
        raise NotImplementedError()

    def __repr__(self):
        """The name of this computation."""
        return self.__class__.__name__


class StandardComputation(Computation):
    """The standard computation is a thresholded dot product."""

    def __init__(self, threshold):
        """Initialize the computation.

        Args:
            threshold: The cut-off threshold for the binary output
        """
        self.threshold = threshold

    def __call__(self, main):
        """Compute the neurons' output.

        For each neuron, adds up the weight of the active synapses,
        then applies a threshold to get the activations.

        Args:
            main: The main input

        Returns:
            Binary values from the computation
        """
        activations = np.dot(main.synapses, main.values)
        return activations > self.threshold


class SparseComputation(Computation):
    """A computation with a limited number of active units."""

    def __init__(self, n):
        """Initialize the computation.

        Args:
            n: The number of neurons to have active in the end
        """
        self.n = n

    def __call__(self, main):
        """Compute the neurons' output.

        For each neuron, adds up the weight of the active synapses,
        then sets the top n to be active.

        Args:
            main: The main input

        Returns:
            Binary values from the computation
        """
        activations = np.dot(main.synapses, main.values)
        top_indices = activations.argsort()[-self.n:]

        result = np.zeros(len(activations))
        result[top_indices] = 1
        return result
