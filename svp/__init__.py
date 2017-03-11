#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
svp module access is done by 
get_players() / add_player / remove_player
get_displays() / add_display / remove_display
"""

import numpy as np
import cv2
import os

from player import Player

__players__ = []
def add_player(name='Untitled'):
	player = Player(name)
	__players__.append(player)
	return player

def get_players():
	return __players__