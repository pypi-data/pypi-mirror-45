# Nodeflux APIs

[![pipeline status](https://gitlab.com/nodefluxio/nodefluxapis/badges/master/pipeline.svg)](https://gitlab.com/nodefluxio/nodefluxapis/commits/master)

This repository contains the public Nodeflux Analytics API. It uses Protocol Buffers version 3 to define the API interface and the structure of the payload messages.

You can use the Nodeflux APIs by using the generated code from this repository. We've also built several client libraries, which are the recommended way to call the Nodeflux APIs:

- [Nodeflux Cloud Client for Python](https://gitlab.com/nodefluxio/nodeflux-cloud-python)

## Generate Source Core

To generate language specific source code from this repository, you need to install Protocol Buffer, gRPC, and some language specific plugins in your machine. Then you can use `make` to generate the source code.

### TL;DR

This guides assume you have all dependencies installed. To install the dependencies, see language specific guides below.

```
git clone https://github.com/googleapis/googleapis.git
export GOOGLEAPIS_PATH=$(pwd)/googleapis

make all                                      # Run linter and build all
make CPP_OUT_DIR=/path/to/genfiles cpp        # Build c++ sources
make PYTHON_OUT_DIR=/path/to/genfiles python  # Build python sources
make GO_OUT_DIR=/path/to/genfiles go          # Build go sources
make docs                                     # Build documentation
make lint                                     # Run linter
```

### C++

To build the C++ source codes, you need to have the following dependencies:

- [Protocol Buffer](https://github.com/protocolbuffers/protobuf) ([Installation Guide](https://github.com/protocolbuffers/protobuf/tree/master/src))
- gRPC Plugin for C++ ([Installation Guide](https://github.com/grpc/grpc/tree/master/src/cpp))
- [googleapis](https://github.com/googleapis/googleapis)

Build the source code by running the following commands:

```
git clone https://github.com/googleapis/googleapis.git
export GOOGLEAPIS_PATH=$(pwd)/googleapis

make CPP_OUT_DIR=/path/to/genfiles cpp
```

### Python

To build the Python source codes, you need to have the following dependencies:

- [Protocol Buffer](https://github.com/protocolbuffers/protobuf)
- gRPC Plugin for Python
- [mypy-protobuf](https://github.com/dropbox/mypy-protobuf)
- [googleapis](https://github.com/googleapis/googleapis)

The dependencies above can be installed by running the following commands:

```
pip3 install grpcio-tools mypy-protobuf

git clone https://github.com/googleapis/googleapis.git
export GOOGLEAPIS_PATH=$(pwd)/googleapis
```

Then you can build python source codes:

Then you can build and install python source codes:

```
make python
pip install .
```

If you want to build the python sources to different directory, use the `PYTHON_OUT_DIR` argument.

```
make PYTHON_OUT_DIR=/path/to/genfiles python
```

### Go

To build the Python source codes, you need to have the following dependencies:

- [Protocol Buffer](https://github.com/protocolbuffers/protobuf) ([Installation Guide](https://github.com/protocolbuffers/protobuf/tree/master/src))
- [Protocol Buffer for Golang](https://github.com/golang/protobuf)
- [gRPC Plugin for Go](https://github.com/grpc/grpc-go)
- [googleapis](https://github.com/googleapis/googleapis)

The dependencies above can be installed by running the following commands:

```
go get -u github.com/golang/protobuf/protoc-gen-go
go get -u google.golang.org/grpc

git clone https://github.com/googleapis/googleapis.git
export GOOGLEAPIS_PATH=$(pwd)/googleapis
```

Then you can build go source codes:

```
make GO_OUT_DIR=/path/to/genfiles go
```
