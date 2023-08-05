import pandas as pd
import json

from nav_dataverk.connectors import JSONStatConnector


class SSBConnector(JSONStatConnector):
    """SSB JSONStat API Connection
    
    """

    def __init__(self, source='https://data.ssb.no/api/v0/no'):
        super(SSBConnector, self).__init__()
        self.source = source
