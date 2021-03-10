import logging
import logging.config
import connexion
from connexion import NoContent
import yaml
import datetime
import json
from pykafka import KafkaClient

import requests

# Your functions here
with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')


def report_order(body):
    logger.info(f"Received event Order Request request with a unique id of {body['customer_name']}")

    # headers = {"content-type": "application/json"}
    # response = requests.post(app_config['orderRequest']['url'],
    #                          json=body, headers=headers)

    client = KafkaClient(hosts='%s:%d' % (app_config["events"]["hostname"], app_config["events"]["port"]))
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    producer = topic.get_sync_producer()

    msg = {
        "type": "or",
        "datatime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": {
            "customer_name": body['customer_name'],
            "device_id": body['device_id'],
            "order_detail": {"item": body['order_detail']['item'],
                             "quantity": body['order_detail']['quantity']},
            "order_id": body['order_id'],
            "store_id": body['store_id'],
            "timestamp": body['timestamp']
        }
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    # if response.status_code == 201:
    #     print(response.json())
    # Got error code
    # logger.info(f"Returned event Order Request response with a unique id of {body['customer_name']} - {response.status_code}")

    return NoContent, 201


def report_delivery(body):
    logger.info(f"Received event Delivery Request request with a unique id of {body['driver_id']}")

    # headers = {"content-type": "application/json"}
    # response = requests.post(app_config['deliveryRequest']['url'],
    #                          json=body, headers=headers)

    hostname = app_config["events"]["hostname"]
    port = app_config["events"]["port"]

    client = KafkaClient(hosts='%s:%d' % (hostname, port))
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    producer = topic.get_sync_producer()

    msg = {
        "type": "dr",
        "datatime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": {
            "customer_name": body['customer_name'],
            "device_id": body['device_id'],
            "driver_id": body['driver_id'],
            "order_detail": {"item": body['order_detail']['item'],
                             "quantity": body['order_detail']['quantity']},
            "order_id": body['order_id'],
            "store_id": body['store_id'],
            "timestamp": body['timestamp']
        }
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    # if response.status_code == 201:
    #     print(response.json())
    # logger.info(f"Returned event Delivery Request response with a unique id of {body['driver_id']} - {response.status_code}")
    #
    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)
if __name__ == "__main__":
    app.run(port=8080)
