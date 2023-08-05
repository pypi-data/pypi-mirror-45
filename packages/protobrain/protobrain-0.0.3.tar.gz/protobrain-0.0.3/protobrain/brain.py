#!/usr/bin/python
# -*- coding: utf-8 -*-
"""The top-level module for dealing with a brain instance."""


class Brain:
    """A class for handling a protobrain."""

    def __init__(self, neurons, sensor):
        """Initialize the protobrain."""
        self.neurons = neurons
        self.sensor = sensor

        neurons.input = sensor

    def compute(self, computation_function=None):
        """Compute the next brain state."""
        self.neurons.compute(computation_function)

    def learn(self, learning_function=None):
        """Learn and adapt connections."""
        learning_function(self.neurons)
