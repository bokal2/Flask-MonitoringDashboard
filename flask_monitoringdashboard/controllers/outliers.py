import ast

from flask_monitoringdashboard.core.colors import get_color
from flask_monitoringdashboard.core.timezone import to_local_datetime
from flask_monitoringdashboard.core.utils import simplify
from flask_monitoringdashboard.database import row2dict
from flask_monitoringdashboard.database.outlier import get_outliers_cpus, get_outliers_sorted


def get_outlier_graph(db_session, endpoint_id):
    """
    :param db_session: session for the database
    :param endpoint_id: id of the endpoint
    :return: a list with data about each CPU performance
    """
    all_cpus = get_outliers_cpus(db_session, endpoint_id)
    cpu_data = [ast.literal_eval(cpu) for cpu in all_cpus]

    return [{
        'name': 'CPU core %d' % idx,
        'values': simplify(data, 50),
        'color': get_color(idx)
    } for idx, data in enumerate(zip(cpu_data))]


def get_outlier_table(db_session, endpoint_id, offset, per_page):
    """
    :param db_session: session for the database
    :param endpoint_id: id of the endpoint
    :param offset: number of items to be skipped
    :param per_page: maximum number of items to be returned
    :return: a list of length at most 'per_page' with data about each outlier
    """
    table = get_outliers_sorted(db_session, endpoint_id, offset, per_page)
    for idx, row in enumerate(table):
        row.request.time_requested = to_local_datetime(row.request.time_requested)
        try:
            row.request_url = row.request_url.decode('utf-8')
        except:
            pass
        dict_request = row2dict(row.request)
        table[idx] = row2dict(row)
        table[idx]['request'] = dict_request
    return table