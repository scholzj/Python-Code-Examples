[![Build Status](https://travis-ci.org/Eurex-Clearing-Messaging-Interfaces/Python-Code-Examples.svg?branch=master)](https://travis-ci.org/Eurex-Clearing-Messaging-Interfaces/Python-Code-Examples)

# pure_python

Examples in the pure_python folder are using the pure Python version of the Qpid Messaging API. This API supports only AMQP 0-10. To run the examples:
- Install the Qpid Messaging API either from the repositories of your OS or from http://qpid.apache.org/download.html (http://www.apache.org/dyn/closer.lua/qpid/0.32/qpid-python-0.32.tar.gz)
- Change the hostname / IP address, port number, paths to the certificates and account name / queue name
- Run the examples

## SSL

The public and private keys are passed to the client library in the form of file path. The client will open them and use them on its own.

## BroadcastReceiver.py

This example connects to the AMQP broker, opens a consumer to the broadcast queue and starts consuming the broadcasts. It stops consuming once the queue is empty.

## RequestResponse.py

This example connects to the broker, sends a request message and waits for a response, which should be sent by the Eurex system. It stops after receiving the response message or after time out.

# cpp_binding

Examples in cpp_binding folder are using the C++ version Qpid Messaging API and its Python binding. The C++ version of the API supports both AMQP 1.0 and 0-10. To run the examples:
- Install Qpid Proton C library (only needed for AMQP 1.0 support)
- Install Qpid Messaging C++ API
- Install Python binding for Qpid Messaging C++ API
- Change the hostname / IP address, port number, paths to the certificates and queue names
- Run the examples

## SSL

The underlying C++ libraries are using the NSS tools to handle SSL. The NSS database has to be prepared before running the client and configured using environment variables.

### Preparing the NSS database

1. Create the database: `certutil -N -d sql:<path>`
2. Load the broker public key as a trusted peer `certutil -A -d sql:<path> -t "P,," -n broker -i certutil -A -d sql:./ -t "P,," -n ecag-fixml-simu1 -i ecag-fixml-simu1_deutsche-boerse_com.crt`
3. Load the member public key `certutil -A -d sql:<path> -t ",," -n ABCFR_ABCFRALMMACC1 -i ABCFR_ABCFRALMMACC1.crt`
4. Load the member private key `pk12util -i ABCFR_ABCFRALMMACC1.p12 -d sql:<path>`
5. Create the password file `echo "<password>" > <passwordFile>`

### Configuring the Qpid libraries

The Qpid Messaging C++ libraries are using environment varible to configure the SSL certificates. There are three relevant variables:
- `QPID_SSL_CERT_DB` contains the path to the NSS database
- `QPID_SSL_CERT_PASSWORD_FILE` contains the path to the password file for the database
- `QPID_SSL_CERT_NAME` contains the nick name of the certificate which should be used for the connection

for example:
```
export QPID_SSL_CERT_DB=sql:./tests/resources/
export QPID_SSL_CERT_PASSWORD_FILE=tests/resources/pwdfile
export QPID_SSL_CERT_NAME=ABCFR_ABCFRALMMACC1
```

## BroadcastReceiver.py

This example connects to the AMQP broker using AMQP 0-10, opens a consumer to the broadcast queue and starts consuming the broadcasts. It stops consuming once the queue is empty.

## RequestResponse.py

This example connects to the broker using AMQP 0-10, sends a request message and waits for a response, which should be sent by the Eurex system. It stops after receiving the response message or after time out.

## Amqp10BroadcastReceiver.py

This example works in the same way as BroadcastReceiver.py, only using AMQP 1.0.

## Amqp10RequestResponse.py

This example works in the same way as RequestResponse.py, only using AMQP 1.0.

# proton_binding

Examples in the proton_binding folder are using the Python binding against the Apache Qpid Proton C library. This API supports only AMQP 1.0. To run the examples:
- Download and install the Qpid Proton library either from the repositories of your OS or from http://qpid.apache.org/download.html
- Download and install the Python binding for the Proton library either from the repositories of your OS or from http://qpid.apache.org/download.html
- Change the hostname / IP address, port number, paths to the certificates and account name / queue name
- Run the examples

## SSL

The public and private keys are passed to the client library in the form of file path. The client will open them and use them on its own.

## BroadcastReceiver.py

This example connects to the AMQP broker, opens a consumer to the broadcast queue and starts consuming the broadcasts. It consumes them for a predefined time interval and exits afterwards. This example is using Proton Reactor - it is written in reactive style.

## RequestResponse.py

This example connects to the broker, sends a request message and waits for a response, which should be sent by the Eurex system. It stops after receiving the response message. This example is using Proton Reactor - it is written in reactive style.

## BlockingBroadcastReceiver.py

This example connects to the AMQP broker, opens a consumer to the broadcast queue and starts consuming the broadcasts. It consumes them for a predefined time interval and exits afterwards. This example is using more traditional blocking API.

## BlockingRequestResponse.py

This example connects to the broker, sends a request message and waits for a response, which should be sent by the Eurex system. It stops after receiving the response message. This example is using more traditional blocking API.


# Integration tests

The project is using Travis-CI to run its own integration tests. The tests are executed against Docker images which contain the AMQP broker with configuration corresponding to Eurex Clearing FIXML Interface. The details of the Travis-CI integration can be found in the .travis.yml file.

# Documentation

More details about Java APIs and code examples can be found in the Volume B of Eurex Clearing Messaging Interfaces documentation on [Eurex Clearing website](http://www.eurexclearing.com/clearing-en/technology/eurex-release14/system-documentation/system-documentation/861464?frag=861450)
