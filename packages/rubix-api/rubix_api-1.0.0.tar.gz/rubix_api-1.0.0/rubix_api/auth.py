import requests
import json
import logging
import sqlite3
from datetime import datetime

class RubixAuth(requests.auth.AuthBase):
    """Attaches HTTP Rubix Authentication to the given Request object."""

    def __init__(
        self,
        url,
        client_id,
        client_secret,
        grant_type,
        audience):
        self.token = None
        self.url = url
        self.client_id = client_id
        self.client_secret = client_secret
        self.grant_type = grant_type
        self.audience = audience

        self.file_name = "rubix_cache.db"
        self.table_name = "tokens"
        self.sqlite_conn = sqlite3.connect(self.file_name)
        self.sqlite_conn.row_factory = sqlite3.Row
        self._create_cache_db()

    def __call__(self, r):
        # modify and return the request
        token = self._get_token()
        r.headers['Authorization'] = "Bearer " + token
        return r
    
    def _get_token(self):
        if self.token is None:
            self.token = self._select_latest_token()

        if self.token is None:
            token_expired = True
        else:
            created_on = datetime.strptime(self.token['datetime'], "%Y-%m-%d %H:%M:%S")
            token_expired = (abs((datetime.now() - created_on).total_seconds()) / 3600) >= self.token['expires_in']

        if token_expired:
            logging.debug("Requesting new token.")

            data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': self.grant_type,
                'audience': self.audience
            }

            r = requests.post(self.url, data=data)
            r.raise_for_status
            self._insert(r.json())
            self.token = r.json()
        
        else: 
            logging.debug("Cached token found.")

        return self.token['access_token']

    def _create_cache_db(self):
        with self.sqlite_conn:
            self.sqlite_conn.execute("""CREATE TABLE IF NOT EXISTS {table_name}(
                access_token TEXT, 
                expires_in INTEGRER, 
                token_type TEXT, 
                datetime TEXT)""".format(table_name=self.table_name))

    def _insert(self, r):
        with self.sqlite_conn:
            self.sqlite_conn.execute("""INSERT INTO {table_name}
            (access_token, expires_in, token_type, datetime) VALUES (?,?,?,?)""".format(table_name=self.table_name),
            (r['access_token'], r['expires_in'], r['token_type'], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    def _select_latest_token(self):
        with self.sqlite_conn:
            return self.sqlite_conn.execute("""SELECT * FROM {table_name} ORDER BY datetime DESC""".format(table_name=self.table_name)).fetchone()