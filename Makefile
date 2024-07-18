# Define directories
SERVICES_DIR := src/Services
STORE_PROTO := $(SERVICES_DIR)/store/protos/StoreService.proto
WALLET_PROTO := $(SERVICES_DIR)/wallet/protos/WalletService.proto

# Define output directories
STORE_OUTPUT := $(SERVICES_DIR)/store/protos
WALLET_OUTPUT := $(SERVICES_DIR)/wallet/protos

# Define proto compiler and gRPC plugin
PROTOC := python3 -m grpc_tools.protoc
PYTHON_OUT := --python_out=
GRPC_PYTHON_OUT := --grpc_python_out=

# Define default target
all: store wallet

# StoreService proto generation
store:
	$(PROTOC) -I=$(SERVICES_DIR)/store/protos $(PYTHON_OUT)$(STORE_OUTPUT) $(GRPC_PYTHON_OUT)$(STORE_OUTPUT) $(STORE_PROTO)

# WalletService proto generation
wallet:
	$(PROTOC) -I=$(SERVICES_DIR)/wallet/protos $(PYTHON_OUT)$(WALLET_OUTPUT) $(GRPC_PYTHON_OUT)$(WALLET_OUTPUT) $(WALLET_PROTO)

# Clean generated files
clean:
	rm -f $(STORE_OUTPUT)/*_pb2*.py
	rm -f $(WALLET_OUTPUT)/*_pb2*.py

# Generate stubs in Python
stubs:
	$(PROTOC) -I=$(SERVICES_DIR)/store/protos --python_out=$(SERVICES_DIR)/store/protos --grpc_python_out=$(SERVICES_DIR)/store/protos $(STORE_PROTO)
	$(PROTOC) -I=$(SERVICES_DIR)/wallet/protos --python_out=$(SERVICES_DIR)/wallet/protos --grpc_python_out=$(SERVICES_DIR)/wallet/protos $(WALLET_PROTO)

# Run server for wallet service
run_serv_banco: wallet
	python3 $(SERVICES_DIR)/wallet/server/server.py $(arg1)

# Run client for wallet service
run_cli_banco: wallet
	python3 $(SERVICES_DIR)/wallet/client/client.py $(arg1) $(arg2)

# Run server for store service
run_serv_loja: store
	python3 $(SERVICES_DIR)/store/server/server.py

# Run client for store service
run_cli_loja: store
	python3 $(SERVICES_DIR)/store/client/client.py

.PHONY: all store wallet clean stubs run_serv_banco run_cli_banco run_serv_loja run_cli_loja
