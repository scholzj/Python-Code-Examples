#! /usr/bin/python

import sys
import time
from qpid_messaging import *

request_address = "request.ABCFR_ABCFRALMMACC1/request; { node: { type: topic }, create: never }"
reply_adress = "response/response.ABCFR_ABCFRALMMACC1.response_queue_1; { create: receiver, node: { type: topic } }"
response_address = "response.ABCFR_ABCFRALMMACC1.response_queue_1; {create: receiver, assert: never, node: { type: queue, x-declare: { auto-delete: true, exclusive: false, arguments: {'qpid.policy_type': ring, 'qpid.max_count': 1000, 'qpid.max_size': 1000000}}, x-bindings: [{exchange: 'response', queue: 'response.ABCFR_ABCFRALMMACC1.response_queue_1', key: 'response.ABCFR_ABCFRALMMACC1.response_queue_1'}]}}";

timeout = 60

try:
  connection = Connection("amqp:ssl:ecag-fixml-simu1.deutsche-boerse.com:10170")
  connection.setOption("sasl_mechanisms", "EXTERNAL")
  connection.setOption("transport", "ssl")
  connection.setOption("heartbeat", 60)

  connection.open()
  session = connection.session()
  receiver = session.receiver(response_address)
  receiver.capacity = 1000
  sender = session.sender(request_address)

  message = Message("<FIXML>...</FIXML>", durable=True, reply_to=reply_adress)
  sender.send(message, sync=False);

  try:
    message = receiver.fetch(timeout=timeout)
    session.acknowledge(sync=False)

    print "-I- Response received with content: ", message.content

  except Empty:
    print "-E- No response received for ", timeout, " seconds"

  session.sync(timeout=None)

  sender.close()
  receiver.close()
  session.close()
  connection.close()
except MessagingError,m:
  print m
