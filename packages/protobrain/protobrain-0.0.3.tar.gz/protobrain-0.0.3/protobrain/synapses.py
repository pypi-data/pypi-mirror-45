#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Module for handling neuron connections."""
import numpy as np
import logging


log = logging.getLogger(__name__)


class Input(object):
    """An input connection with synapses.

    Inputs are identified by a name and set up their synapses when connected
    to an output.
    """

    def __init__(self, name, shape):
        """Initialize the input.

        Args:
            name: The name of the input
            shape: The shape of the neurons this input is feeding
        """
        self.name = name
        self.shape = np.zeros(shape).shape  # TODO: Not the most efficient
        self.synapses = None
        self._connected_output = None

    @property
    def connected(self):
        """Whether the input is connected to an output."""
        return self._connected_output is not None

    # TODO: Allow providing the function for synapse creation
    def connect(self, output):
        """Connect this input to an output.

        Creates the synapses to match the output's dimensions.

        Args:
            output: The output to connect to
        """
        if self._connected_output is output:
            log.warning('Skipping reconnection of input-output pair')
            return  # Skip

        self.synapses = Input._create_synapses(self.shape, output.shape)
        self._connected_output = output

    @property
    def values(self):
        """The values available to this input.

        These are taken from the connected output."""
        if not self._connected_output:
            raise IndexError('No input set for {1}'.format(repr(self)))
        return self._connected_output.values

    @classmethod
    def _create_synapses(cls, input_shape, output_shape, symmetric=False):
        """Create the synapses between an input and an output.

        Args:
            input_shape: The shape of the input
            output_shape: The shape of the output
            symmetric: Whether to enforce symmetric weights

        Returns:
            A numpy tensor with the right shape and random weights
        """
        shape = input_shape + output_shape
        strength = np.random.uniform(0, 1, shape)

        return (
            (strength + strength.T) / 2
            if symmetric
            else strength
        )


class Output(object):
    """An output to which an input can connect."""

    def __init__(self, shape):
        """Initialize the output.

        Args:
            shape: The output's shape
        """
        self._values = np.zeros(shape)
        self.shape = self._values.shape

    @property
    def values(self):
        """The values available at this output."""
        return self._values

    @values.setter
    def values(self, vals):
        """Set the values on the output, verifying the shape is right."""
        if vals.shape != self.shape:
            raise ValueError(
                'Dimension mismatch when specifying output values. '
                'Expected {0}, but got {1}'.format(self.shape, vals.shape)
            )
        self._values = vals

    def __getitem__(self, idxs):
        """Slice the Output."""
        if isinstance(idxs, slice) or isinstance(idxs, tuple):
            return OutputSlice(self, idxs)
        elif isinstance(idxs, int):
            return OutputSlice(self, slice(idxs))
        else:
            raise IndexError('Invalid slicing of an Output: {0}'.format(idxs))


class OutputMerge(Output):
    """Output that merges two or more outputs."""

    def __init__(self, outputs, axis=None):
        """Initialize the output.

        Args:
            outputs: Outputs to merge
            axis: Axis along which to concatenate them
        """
        if not outputs:
            raise ValueError('Need at least two outputs to merge')

        if axis is None:
            axis = self.pick_axis(outputs)

        self._axis = axis
        self._outputs = outputs
        self.shape = np.concatenate(
            [output.values for output in self._outputs],
            axis=axis
        ).shape

    def merge(self, outputs, axis):
        """Merge the output values.

        Args:
            outputs: The outputs to merge
            axis: The axis along which to concatenate
        """
        return np.concatenate(
            [output.values for output in outputs],
            axis=axis
        )

    def pick_axis(self, outputs):
        """Pick an axis for concatenating the outputs.

        Args:
            outputs: The outputs that need to be merged

        Returns:
            An axis along which they can be concatenated

        Throws:
            ValueError if no axis allows concatenation
        """
        axis_options = range(len(outputs[0].shape))
        for axis in axis_options:
            try:
                self.merge(outputs, axis)
                return axis
            except:
                pass
        raise ValueError(
            'No single axis can be used to merge outputs of shapes {}'.format(
                [output.shape for output in outputs]
            ))

    @property
    def values(self):
        """Concatenate the values from the merged outputs."""
        return self.merge(self._outputs, self._axis)


class OutputSlice(Output):
    """A slice of an output."""

    def __init__(self, output, slice):
        """Initialize the output.

        Args:
            output: The original output
            slice: A slice object representing the part of the output to take.
        """
        self._output = output
        self._slice = slice

    @property
    def shape(self):
        """The shape of the output."""
        return self.values.shape

    @property
    def values(self):
        """Slice the values from the internal output."""
        return self._output.values[self._slice]
