# protobrain
This is an experimental project for machine learning techniques.

Loosely based on Hierarchical Temporal Memory by [Numenta](http://numenta.org/).

## Building the protobuf files
To use this project you'll need to build the protobuf files.
```
protoc -I=. --python_out=. protobrain/proto/*.proto
```

For more information on Protocol buffers, read the [official documentation](https://developers.google.com/protocol-buffers/).

## Testing
This project uses pytest and the tests can be run from the repository root.
```
python -m pytest
```

## License
protobrain is a project licensed under GNU GPLv3.
