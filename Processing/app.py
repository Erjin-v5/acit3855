import connexion
import os.path
import json
import logging
import logging.config
import yaml
from apscheduler.schedulers.background import BackgroundScheduler
import requests

from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from base import Base
# from order_request import OrderRequest
# from delivery_request import DeliveryRequest
import datetime

# Your functions here
# MAX_EVENTS = 10

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')


def get_stats():
    logger.info("Get stats request start")

    if os.path.isfile('data.json'):
        with open('data.json', 'r') as f:
            data = json.load(f)
        logger.debug("Start converting")
        stats_dict = {}
        stats_dict.update({
            "order_req_received_since_last_update": data['order_req_received_since_last_update'],
            "total_order_req_today": data['total_order_req_today'],
            "delivery_req_received_since_last_update": data['delivery_req_received_since_last_update'],
            "total_delivery_req_today": data['total_delivery_req_today'],
            "last_updated": data['last_updated']
        })
        logger.info("Get stats request completed")
        return stats_dict, 200
    else:
        return logger.error("Statistics do not exist"), 404


def populate_stats():
    """ Periodically update stats """
    logger.info("Start Periodic Processing")

    current_datetime = datetime.datetime.now()
    # current_datetime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    if os.path.isfile('data.json'):
        with open('data.json', 'r') as f:
            data = json.load(f)

        last_datetime = data['last_updated']
        order_response = requests.get(app_config['eventstore']['url'] + "/order", params={"timestamp": last_datetime})
        delivery_response = requests.get(app_config['eventstore']['url'] + "/delivery",
                                         params={"timestamp": last_datetime})

        if order_response.status_code != 200:
            logger.error("Order response error")
        elif delivery_response.status_code != 200:
            logger.error("Delivery response error")
        else:
            order_list = order_response.json()
            delivery_list = delivery_response.json()

            count_order_last = len(order_list)
            count_delivery_last = len(delivery_list)
            logger.info("Totally " + str(count_delivery_last + count_order_last) + " events received")

            l_time = current_datetime.strptime(last_datetime, "%Y-%m-%dT%H:%M:%SZ")

            calculate_update(count_delivery_last, count_order_last, current_datetime, l_time, data)

    else:
        stats_dict = {}
        stats_dict.update({
            "order_req_received_since_last_update": "0",
            "total_order_req_today": "0",
            "delivery_req_received_since_last_update": "0",
            "total_delivery_req_today": "0",
            "last_updated": current_datetime
        })
        json_object = json.dumps(stats_dict, indent=4)
        with open('data.json', 'w') as f:
            f.write(json_object)
            return logger.info("data.json does not exist, create a default data.json")
    logger.info("Period processing has ended")


def calculate_update(count_delivery_last, count_order_last, current_datetime, l_time, data):
    if l_time.day != current_datetime.day:
        ctime = current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        stats_dict = {}
        stats_dict.update({
            "order_req_received_since_last_update": str(count_order_last),
            "total_order_req_today": "0",
            "delivery_req_received_since_last_update": str(count_delivery_last),
            "total_delivery_req_today": "0",
            "last_updated": ctime
        })
        json_object = json.dumps(stats_dict, indent=4)
        with open('data.json', 'w') as f:
            f.write(json_object)
            logger.debug("data.json has been updated")
    else:
        ctime = current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        stats_dict = {}
        total_order = int(data['total_order_req_today']) + count_order_last
        total_delivery = int(data['total_delivery_req_today']) + count_delivery_last
        stats_dict.update({
            "order_req_received_since_last_update": str(count_order_last),
            "total_order_req_today": str(total_order),
            "delivery_req_received_since_last_update": str(count_delivery_last),
            "total_delivery_req_today": str(total_delivery),
            "last_updated": ctime
        })
        json_object = json.dumps(stats_dict, indent=4)
        with open('data.json', 'w') as f:
            f.write(json_object)
            logger.debug("data.json has been updated")


def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
                  'interval',
                  seconds=app_config['scheduler']['period_sec'])
    sched.start()


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)
if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100, use_reloader=False)
