#!/usr/bin/env python
# encoding: utf-8

import math
import arrow


class Model(object):
    def __init__(self):
        """
        two weeks to reset
        """
        self.time_score_start = arrow.get('2019-04-15 12:30:45')

    @staticmethod
    def fit(features):
        time_score_start = arrow.get('2019-04-15 12:30:45')
        feature_score = sum(features)
        time_score = (arrow.now() - time_score_start).total_seconds()/3600/24 * (-0.1)
        gravity_score = math.e ** time_score
        rank_score = feature_score * gravity_score
        return rank_score


