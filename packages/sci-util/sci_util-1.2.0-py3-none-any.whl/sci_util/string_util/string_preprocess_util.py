#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: violinsolo
# Created on 28/09/2018


FILTER_TOKENS = {
    ' ': '',
    '\n': '',
    '\t': '',
    '\r': '',
    '󾠮': '',
    '🏻': '',
    '🏼': '',
    '𓆟': '',
}


def filter_string(target: str) -> str:
    """
    do filtering for target string
    :param target:
    :return:
    """
    result = target

    for key, value in FILTER_TOKENS.items():
        result = result.replace(key, value)

    return result




if __name__ == '__main__':
    filter_string('')