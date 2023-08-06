import logging

import pytest
import kafka
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import NoBrokersAvailable

from kafka_handler import KafkaLogHandler


def mock_check_version(*args, **kwargs):
    """Necessary mock for KafkaProducer not to connect on init."""
    return 0, 10


def test_handler_can_be_created(topic, mock_kafka_producer):
    handler = KafkaLogHandler(topic=topic)
    assert handler

    handler = KafkaLogHandler(topic=topic, key="testing_key")
    assert handler

    handler = KafkaLogHandler(topic=topic, partition=0)
    assert handler

    handler = KafkaLogHandler(topic=topic, key="testing_key", partition=0)
    assert handler

    handler = KafkaLogHandler(topic=topic, bootstrap_servers="127.0.0.1:9092")
    assert handler
    assert handler.producer
    assert handler.producer.config.get("bootstrap_servers") == "127.0.0.1:9092"


def test_message_payload_does_not_contain_none_values(
    topic, capsys, mock_kafka_producer
):
    log_message = logging.LogRecord(
        "name", "level", "pathname", "lineno", "message", ["args"], "exc_info"
    )

    handler = KafkaLogHandler(topic=topic, key=None, partition=2)
    handler.emit(log_message)

    out = capsys.readouterr().out
    assert "key" not in out
    assert "None" not in out

    handler = KafkaLogHandler(topic=topic, key="testing_key")
    handler.emit(log_message)

    out = capsys.readouterr().out
    assert "key" in out
    assert "None" not in out


def test_handlers_are_isolated_per_topic(topic, mock_kafka_producer, capsys):
    msg_one = "message_one"
    msg_two = "message_two"

    handler_one = KafkaLogHandler(topic=topic + "_1")
    handler_two = KafkaLogHandler(topic=topic + "_2")

    logger_one = logging.getLogger("logger_one")
    logger_one.addHandler(handler_one)
    logger_one.setLevel(logging.INFO)

    logger_two = logging.getLogger("logger_two")
    logger_two.addHandler(handler_two)
    logger_two.setLevel(logging.INFO)

    logger_one.info(msg_one)
    out_one = capsys.readouterr().out

    logger_two.info(msg_two)
    out_two = capsys.readouterr().out

    assert "message_one" in out_one
    assert "message_one" not in out_two
    assert "message_two" not in out_one
    assert "message_two" in out_two


def test_raw_logs_print_linenumber_and_pathname(topic, mock_kafka_producer, capsys):
    msg = logging.LogRecord("", "", "pathname", "lineno_for_real", "message", [], "")

    handler = KafkaLogHandler(topic=topic, raw_logging=True)
    handler.emit(msg)
    emitted_output = capsys.readouterr().out

    assert isinstance(emitted_output, str)
    assert "lineno_for_real" in emitted_output
    assert "pathname" in emitted_output
    assert "b'message - lineno_for_real: pathname'" in emitted_output
