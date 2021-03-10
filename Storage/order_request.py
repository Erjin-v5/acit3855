from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class OrderRequest(Base):
    """Order Request"""

    __tablename__ = "order_request"

    id = Column(Integer, primary_key=True)
    customer_name = Column(String(250), nullable=False)
    device_id = Column(String(250), nullable=False)
    item = Column(String(250), nullable=False)
    quantity = Column(Integer, nullable=False)
    order_id = Column(String(250), nullable=False)
    store_id = Column(String(250), nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, customer_name, device_id, item, quantity, order_id, store_id, timestamp):
        """ Initializes a order request reading """

        self.customer_name = customer_name
        self.device_id = device_id
        self.item = item
        self.quantity = quantity
        self.order_id = order_id
        self.store_id = store_id
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a order request reading """
        dict = {}
        dict['id'] = self.id
        dict['customer_name'] = self.customer_name
        dict['device_id'] = self.device_id
        dict['order_detail'] = {}
        dict['order_detail']['item'] = self.item
        dict['order_detail']['quantity'] = self.quantity
        dict['order_id'] = self.order_id
        dict['store_id'] = self.store_id
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created

        return dict
