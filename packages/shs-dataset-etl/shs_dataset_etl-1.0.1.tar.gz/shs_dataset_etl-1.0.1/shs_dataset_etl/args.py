# -*- coding: utf-8 -*-

import argparse


class Args:
    """class for console argument parsing"""

    def __init__(self):
        p = argparse.ArgumentParser(prog="shs_dataset_etl")

        group = p.add_mutually_exclusive_group(required=True)
        group.add_argument("--setup",  action="store_true", help="Setup ETL process.")
        group.add_argument("--artist-id", help="Retrieve songs per the artist id.")

        args = p.parse_args()

        self.artist_id = args.artist_id
        self.setup = args.setup

