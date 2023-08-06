"""Upload Client for AWS Event Data to S3."""
# -*- coding: utf-8 -*-
import snowflake.connector

class SnowflakeJsonInsert(object):
    """A Snowflake Json Insert Operator."""

    def __init__(self, config):
        """A handler init."""
        self.log = config["LOG"]
        self.user = config["SNOWFLAKE"]["USER"]
        self.account = config["SNOWFLAKE"]["ACCOUNT"]
        self.warehouse="STITCH"
        self.database=config["SNOWFLAKE"]["DATABASE"]
        self.schema=config["SNOWFLAKE"]["SCHEMA"]
        self.table = config["SNOWFLAKE"]["TABLE"]
        self.ctx = snowflake.connector.connect(
            user=self.user,
            password=config["SNOWFLAKE"]["PASSWORD"],
            account=self.account,
            warehouse=self.warehouse,
            database=self.database,
            schema=self.schema)
        self.ctx.execute_string(
            "create table if not exists %s (scr variant)" 
            % self.table, return_cursors=False)


    def close(self):
        self.ctx.close()


    def insert(self, message):
        self.ctx.execute_string(
            "insert into %s (select PARSE_JSON('%s'))" 
             % (self.table, message), return_cursors=False)
        self.log.info('Ingestion into Snowflake. ' 
                       'User: {}, '
                       'Account: {}, ' 
                       'Warehouse: {}, ' 
                       'Database: {}, ' 
                       'Schema: {}, ' 
                       'Table: {}.'.format(
            self.user, self.account, self.warehouse,
            self.database, self.schema, self.table))




