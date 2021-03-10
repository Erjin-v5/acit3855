import connexion
import swagger_ui_bundle
from pykafka import KafkaClient
from pykafka.common import OffsetType
import yaml
import logging.config
import json

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')


def get_order_request_reading(index):
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
                                         consumer_timeout_ms=2000)

    logger.info("Retrieving OR at index %d" % index)

    count = 0
    reading = None
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)

            # Find the event at the index you want and
            # return code 200
            # i.e., return event, 200

            if msg["type"] == "or":

                if count == int(index):
                    reading = msg["payload"]
                    return reading, 200

                count += 1
    except:
        logger.error("No more messages found")

    logger.error("Could not find OR at index %d" % index)
    return {"message": "Not Found"}, 404


def get_delivery_request_reading(index):
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
                                         consumer_timeout_ms=2000)

    logger.info("Retrieving DR at index %d" % index)

    count = 0
    reading = None
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)

            # Find the event at the index you want and
            # return code 200
            # i.e., return event, 200

            if msg["type"] == "dr":

                if count == int(index):
                    reading = msg["payload"]
                    return reading, 200

                count += 1
    except:
        logger.error("No more messages found")

    logger.error("Could not find DR at index %d" % index)
    return {"message": "Not Found"}, 404


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)
if __name__ == "__main__":
    app.run(port=8110)
