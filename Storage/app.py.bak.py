import connexion
import os.path
import json
import logging
import logging.config
import yaml

from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from order_request import OrderRequest
from delivery_request import DeliveryRequest
import datetime
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread

# Your functions here
# MAX_EVENTS = 10

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

"""SQL DB"""
# DB_ENGINE = create_engine("sqlite:///readings.sqlite")
# Base.metadata.bind = DB_ENGINE
# DB_SESSION = sessionmaker(bind=DB_ENGINE)

"""MySQL DB"""
USER = app_config['datastore']['user']
PASSWORD = app_config['datastore']['password']
HOSTNAME = app_config['datastore']['hostname']
PORT = app_config['datastore']['port']
DB = app_config['datastore']['db']

DB_ENGINE = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOSTNAME}:{PORT}/{DB}')
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def report_order(body):
    """ Receives a order request reading """

    # write_request_max_10_events(body)
    logger.info("Connecting to DB. Hostname:kafka-acit3855-erjin.eastus.cloudapp.azure.com, Port:3306")

    session = DB_SESSION()

    order_req = OrderRequest(body['customer_name'],
                             body['device_id'],
                             body['order_detail']['item'],
                             body['order_detail']['quantity'],
                             body['order_id'],
                             body['store_id'],
                             body['timestamp'])

    session.add(order_req)

    session.commit()
    session.close()

    logger.debug(f"Stored event Order Request request with a unique id of {body['customer_name']}")

    return NoContent, 201


def report_delivery(body):
    """ Receives a delivery request reading """

    # write_request_max_10_events(body)
    logger.info("Connecting to DB. Hostname:kafka-acit3855-erjin.eastus.cloudapp.azure.com, Port:3306")

    session = DB_SESSION()

    delivery_req = DeliveryRequest(body['customer_name'],
                                   body['device_id'],
                                   body['driver_id'],
                                   body['order_detail']['item'],
                                   body['order_detail']['quantity'],
                                   body['order_id'],
                                   body['store_id'],
                                   body['timestamp'])

    session.add(delivery_req)

    session.commit()
    session.close()

    logger.debug(f"Stored event Delivery Request request with a unique id of {body['driver_id']}")

    return NoContent, 201


def get_order(timestamp):
    """ Gets new order request after the timestamp """

    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    print(timestamp_datetime)
    readings = session.query(OrderRequest).filter(OrderRequest.date_created >= timestamp_datetime)
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()

    logger.info("Query for Order Request after %s returns %d results" %
                (timestamp, len(results_list)))
    return results_list, 200


def get_delivery(timestamp):
    """ Gets new delivery request after the timestamp """

    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp,
                                                    "%Y-%m-%dT%H:%M:%SZ")
    print(timestamp_datetime)
    readings = session.query(DeliveryRequest).filter(DeliveryRequest.date_created >= timestamp_datetime)
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()

    logger.info("Query for Delivery Request after %s returns %d results" %
                (timestamp, len(results_list)))
    return results_list, 200


# def write_request_max_10_events(body):
#     json_str = json.dumps(body)
#     os.path.isfile("EVENT_FILE.txt")
#     file_handle = open("EVENT_FILE.txt", "a")
#     file_handle.write(json_str + "\n")
#     file_handle.close()
#     counter = 0
#     file_read = open("EVENT_FILE.txt", "r")
#     file_contents = file_read.read().splitlines(True)
#     for line in file_contents:
#         if line:
#             counter += 1
#     file_read.close()
#     if counter > MAX_EVENTS:
#         file_dline = open("EVENT_FILE.txt", "w")
#         file_dline.writelines(file_contents[1:])
#
#         file_dline.close()
#     print("O: " + str(counter))


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)
if __name__ == "__main__":
    app.run(port=8090)

