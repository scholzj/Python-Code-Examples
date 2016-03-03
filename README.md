# qpid.messaging

Examples in the qpid.messaging folder are using the pure Python version of the Qpid Messaging API. This API supports only AMQP 0-10. To run the examples:
- Install the Qpid Messaging API either from the repositories of your OS or from http://qpid.apache.org/download.html (http://www.apache.org/dyn/closer.lua/qpid/0.32/qpid-python-0.32.tar.gz)
- Change the hostname / IP address, port number, paths to the certificates and queue names
- Run the examples

## broadcast_receiver.py

This example connects to the AMQP broker, opens a consumer to the broadcast queue and starts consuming the broadcasts.

## request_response.py

This example connects to the broker,connects to the broker, sends a request message and wait for a response, which should be sent by the Eurex system.

# qpid_messaging

Examples in qpid_messaging folder are using the C++ version Qpid Messaging API and its Python binding. The C++ version of the API supports both AMQP 1.0 and 0-10. To run the examples:
- Install Qpid Proton C library
- Install Qpid Messaging C++ API
- Install Python binding for Qpid Messaging C++ API
- Change the hostname / IP address, port number, paths to the certificates and queue names
- Run the examples

## broadcast_receiver.py

This example connects to the AMQP broker using AMQP 0-10, opens a consumer to the broadcast queue and starts consuming the broadcasts.

## request_response.py

This example connects to the AMQP broker using AMQP 0-10, sends a request message and wait for a response, which should be sent by the Eurex system.

## 10_broadcast_receiver.py

This example connects to the AMQP broker using AMQP 1.0, opens a consumer to the broadcast queue and starts consuming the broadcasts.

## 10_request_response.py

This example connects to the AMQP broker using AMQP 1.0, sends a request message and wait for a response, which should be sent by the Eurex system.

# Documentation

More details about Python APIs and code examples can be found in the Volume B of Eurex Clearing Messaging Interfaces documentation on http://www.eurexclearing.com/clearing-en/technology/eurex-release14/system-documentation/system-documentation/861464?frag=861450
