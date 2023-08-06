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
            warehouse="LAMBDA",
            database=config["SNOWFLAKE"]["DATABASE"],
            schema=config["SNOWFLAKE"]["SCHEMA"])
        self.cs = ctx.cursor()
        self.cs.execute("create table if not exist {} (src variant)").format(
            config["SNOWFLAKE"]["TABLE"])


    def close(self):
        self.cs.close()
        self.ctx.close()


    def insert(self, message):
        self.cs.execute("insert into test_json_load (select PARSE_JSON('%s'))" % message)
        self.log.info('Ingested Message into Snowflake: {}'.format(self.ctx))




