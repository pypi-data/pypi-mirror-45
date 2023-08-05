#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging


FORMAT = (
    '%(asctime)s %(levelname)s %(message)s '
    '(%(filename)s %(funcName)s:%(lineno)s)'
)
logging.basicConfig(format=FORMAT)
