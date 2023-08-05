"""
@author huongnhd
"""

import os


class ByeBaseConf:
  BASE_DIR = os.path.dirname(os.path.realpath(__file__))
  #   BASE_DIR = os.path.dirname(os.path.abspath(__file__))

  ELASTICSEARCH = {
      'host_name': 'localhost',
      # 'http_auth': ('', '********'),
      'port': 9200
  }
  # link for monitor amqp: https://eagle.rmq.cloudamqp.com/#/connections
  # AMQPURL = 'amqp://sbeftlyb:b7aSqyzBjHmZo-H5s8G7mM1bW8u55e0V@eagle.rmq.cloudamqp.com/sbeftlyb'
  AMQPURL = 'amqp://guest:guest@localhost:5672/%2F'
  # folder storage file downloaded from google storage
  GLOBAL_MAIN_TEMP_DIR = '/tmp'
