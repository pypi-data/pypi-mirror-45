#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Entry point for running experiments.

Creates the setup defined by the experiment protobuf instance that is received
and then proceeds to run the experiment by feeding the inputs to the sensor.

Outputs snapshots on every iteration and saves them to the provided file.

*******************************************
usage: experiment.py [-h] experiment output

positional arguments:
  experiment  Path to a binary protobuf file with the experiment
  output      Path to a binary file for the output

optional arguments:
  -h, --help  show this help message and exit
"""
import argparse
from protobrain import brain
from protobrain import computation
from protobrain import learning
from protobrain import sensor
from protobrain.proto import experiment_pb2
from protobrain.util import proto_io
from protobrain.util import proto_parse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'experiment',
        help='Path to a binary protobuf file with the experiment',
        type=str
    )
    parser.add_argument(
        'output',
        help='Path to a binary file for the output',
        type=str
    )

    args = parser.parse_args()
    experiment_path = args.experiment
    output_path = args.output

    exp = experiment_pb2.Experiment()
    with open(experiment_path, 'rb') as input_file:
        exp.ParseFromString(input_file.read())

    _computation = computation.SparseComputation(5)
    _learning = learning.HebbianLearning()

    senz = sensor.Sensor(proto_parse.decode_encoder(exp.encoder))
    brain = brain.Brain(
        sensor=senz,
        neurons=proto_parse.decode_neurons(exp.cortex)
    )

    with open(output_path, 'wb') as output_file:
        writer = proto_io.ProtoWriter(output_file)
        for value in proto_parse.decode_input(exp.input):
            senz.feed(value)
            brain.compute(_computation)
            brain.learn(_learning)
            writer.write(proto_parse.encode_brain(brain))


if __name__ == '__main__':
    main()
