#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Module for writing and reading multiple protobufs to a file."""


class ProtoWriter:
    """Class for writing multiple protobufs to a file."""

    def __init__(self, open_file):
        """Initialize the ProtoWriter.

        Args:
            open_file: An open binary file for writing the protobufs
        """
        self.open_file = open_file

    def write(self, proto):
        """Write the protobuf to the file.

        Args:
            proto: A protobuf object to write.
        """
        proto_bytes = proto.SerializeToString()
        length_bytes = len(proto_bytes).to_bytes(4, 'big')
        self.open_file.write(length_bytes)
        self.open_file.write(proto_bytes)


class ProtoReader:
    """Class for reading multiple protobufs of the same type from a file."""

    def __init__(self, open_file, proto_class):
        """Initialize the ProtoReader.

        Args:
            open_file: An open binary file to read the protobufs from
            proto_class: The class of the protobufs to decode
        """
        self.open_file = open_file
        self.proto_class = proto_class

    def __iter__(self):
        """Iterate over the protobufs in the file."""
        while True:
            length_bytes = self.open_file.read(4)
            if not length_bytes:
                break

            length = int.from_bytes(
                length_bytes,
                byteorder='big',
                signed=False
            )

            proto_bytes = self.open_file.read(length)
            yield self.proto_class.FromString(proto_bytes)




