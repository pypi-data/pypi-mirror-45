# -*- coding: utf-8 -*-

import unittest
import os
from .cli import find_songs_per_artist
import logging

logging.disable(logging.CRITICAL)


class test_find_songs_per_artist(unittest.TestCase):

    current_dir = os.path.dirname(os.path.abspath(__file__))

    artist_id = "ARQFFTK1187FB4C7E1"

    database = current_dir + "/data/database.db"

    result = [('Wheel of Fortune',), ('Blue Christmas',), ("It's Only Make Believe",), ('Rock Billy Boogie',),
                    ('Suspicion',), ('Bad Boy',), ('All By Myself',)]

    def test(self):
        self.assertEqual(find_songs_per_artist(self.database, self.artist_id), self.result)


if __name__ == '__main__':
    unittest.main()
