#!/usr/bin/env python3
""" Filter_datum """
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Filter_datum """
    for field in fields:
        message = re.sub(f"{field}=[^{separator}]*",
                         f"{field}={redaction}", message)
    return message
