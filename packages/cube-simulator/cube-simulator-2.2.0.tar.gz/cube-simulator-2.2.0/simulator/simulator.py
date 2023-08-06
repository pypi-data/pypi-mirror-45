__author__ = 'SHASHANK'

from datetime import datetime
from .date_utils import DateUtils
from .flows import flows


calender = DateUtils()


def getdate(mode, t_date, scheme_id, gateway=0, toacc=""):

    if t_date < datetime.strptime("2019-01-01", "%Y-%m-%d") < datetime.strptime("2020-01-01", "%Y-%m-%d"):
        raise ValueError("Transaction Date is out of 1 year window")

    if gateway in [0, 1, 3, 4]:
        order_delay = 0
        partner_credit_date = calender.get_next_date(t_date)
    elif gateway == 2:
        order_delay = 3 if t_date.hour < 10 else 4
        partner_credit_date = t_date = calender.get_next_date(t_date, 3 if t_date.hour < 10 else 4)
    else:
        raise ValueError("Gateway Not Implemented")

    func = "flow_" + mode + "bank" if toacc == "bank" else ""
    final_date, _ = getattr(flows, func)(t_date, order_delay, partner_credit_date, calender, scheme_id)
    return final_date
