"""Upload Client for AWS Event Data to S3."""
# -*- coding: utf-8 -*-
import snowflake.connector

class SnowflakeJsonInsert(object):
    """A Snowflake Json Insert Operator."""

    def __init__(self, config):
        """A handler init."""
        self.log = config["LOG"]
        self.ctx = snowflake.connector.connect(
            user=config["SNOWFLAKE"]["USER"],
            password=config["SNOWFLAKE"]["PASSWORD"],
            account=config["SNOWFLAKE"]["ACCOUNT"],
            warehouse="STITCH",
            database=config["SNOWFLAKE"]["DATABASE"],
            schema=config["SNOWFLAKE"]["SCHEMA"])
        self.table = config["SNOWFLAKE"]["TABLE"]
        self.ctx.execute_string(
            "create table if not exists %s (scr variant)" % self.table)


    def close(self):
        self.ctx.close()


    def insert(self, message):
        self.ctx.execute_string("insert into %s (select PARSE_JSON('%s'))" % (self.table, message))
        self.log.info('Ingested Message into Snowflake: {}'.format(self.ctx))




