# -*- coding: utf-8 -*-

main = None


class MicroOrm(object):
    def __init__(self, db_name, db_host, db_user, db_password, connect_timeout=5, charset="utf8mb4"):
        global main
        self.db_name = db_name
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.connect_timeout = connect_timeout
        self.charset = charset
        main = self
