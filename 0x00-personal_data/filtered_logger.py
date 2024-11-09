#!/usr/bin/env python3
"""
Provides functions to filter sensitive data and create a logging mechanism with redaction capabilities.
"""
from typing import List
import re
import logging
import os
import mysql.connector

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')  # Fields to be obfuscated

def obfuscate_message(fields_to_redact: List[str], redaction_text: str,
                      log_message: str, field_separator: str) -> str:
    """
    Obfuscates specified fields in a log message.
    
    Args:
        fields_to_redact (list): List of field names to obfuscate.
        redaction_text (str): Text to replace sensitive fields with.
        log_message (str): The log message containing fields.
        field_separator (str): The character separating fields in the message.
    
    Returns:
        str: The obfuscated log message.
    """
    for field in fields_to_redact:
        log_message = re.sub(field + r'=.*?' + field_separator,
                             field + '=' + redaction_text + field_separator, log_message)
    return log_message

class SensitiveDataFormatter(logging.Formatter):
    """
    A logging Formatter that redacts sensitive fields from log messages.
    """
    REDACTION_TEXT = "***"
    LOG_FORMAT = "[APPLICATION] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    FIELD_SEPARATOR = ";"

    def __init__(self, fields_to_redact: List[str]):
        super(SensitiveDataFormatter, self).__init__(self.LOG_FORMAT)
        self.fields_to_redact = fields_to_redact

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a LogRecord, redacting sensitive data.
        
        Args:
            record (logging.LogRecord): A record containing the log message.
        
        Returns:
            str: The redacted log message.
        """
        original_message = super(SensitiveDataFormatter, self).format(record)
        redacted_message = obfuscate_message(self.fields_to_redact, self.REDACTION_TEXT,
                                             original_message, self.FIELD_SEPARATOR)
        return redacted_message

def create_logger() -> logging.Logger:
    """
    Creates and configures a logger for handling user data.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("user_data_logger")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = SensitiveDataFormatter(PII_FIELDS)

    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger

def connect_to_database() -> mysql.connector.connection.MySQLConnection:
    """
    Establishes a connection to the database using environment variables.
    
    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object.
    """
    db_user = os.getenv('PERSONAL_DATA_DB_USERNAME') or "root"
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ""
    db_host = os.getenv('PERSONAL_DATA_DB_HOST') or "localhost"
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    connection = mysql.connector.connect(user=db_user,
                                         password=db_password,
                                         host=db_host,
                                         database=db_name)
    return connection

def main():
    """
    Main function to retrieve and log user data from the database.
    """
    db_connection = connect_to_database()
    logger = create_logger()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users;")
    column_names = cursor.column_names

    for record in cursor:
        log_message = "".join(f"{field}={value}; " for field, value in zip(column_names, record))
        logger.info(log_message.strip())

    cursor.close()
    db_connection.close()

if __name__ == "__main__":
    main()
