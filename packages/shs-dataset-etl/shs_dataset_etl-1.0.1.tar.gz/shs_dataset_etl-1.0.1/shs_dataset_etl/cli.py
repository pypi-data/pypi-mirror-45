# -*- coding: utf-8 -*-

from .__init__ import __version__
from .args import Args

import os
import logging
import requests
import re
import sqlite3

# import sys
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setting up logger
logger = logging.getLogger("shs_dataset_etl")
logger.setLevel(logging.INFO)

# Always display on console
logger.addHandler(logging.StreamHandler())

# Output version information
logger.info("Running shs_dataset_etl v." + __version__)


def update_dataset(dataset_url, filename):
    try:
        response = requests.get(dataset_url)

        # update dataset
        if response.status_code == 200:
            with open(filename, "w") as file:
                file.write(response.text)
                logger.info("Info: Dataset file has been updated successfully.")
    except Exception as e:
        logger.info(e)
        logger.info("Error: Dataset update from web failed. Using stored dataset file.")


def parse_line(line):
    """
    Does a regex search against all defined regexes and
    returns the key and match result of the first matching regex.
    """

    # set up regular expressions
    rx_dict = {
        "comment": re.compile(r"#(.*)\n"),
        "clique": re.compile(r"%(?P<a>(-)*\d+)(,*)(?P<b>\d+)*(,*)(?P<c>\d+)*(,*)(?P<title>.+)\n"),
        "track": re.compile(r"(?P<track_id>.+)<SEP>(?P<artist_id>.+)<SEP>(?P<performance_id>(-)*.+)\n"),
    }

    for key, rx in rx_dict.items():
        match = rx.search(line)

        if match:
            return key, match

    # if there are no matches
    return None, None


def conversion_w_none(x):
    """Conversion to int in case x is none, returns none."""
    if x is None:
        return None
    else:
        return int(x)


def parse_file(filepath):
    """Parses input text file and outputs cliques and tracks."""
    cliques = []
    tracks = []

    clique_counter = 0
    track_counter = 0

    skip_tracks = False  # flag to skip associated tracks if clique or one of clique track is faulty

    # open the file and read through it line by line
    with open(filepath, "r") as file:

        line = file.readline()

        while line:

            key, match = parse_line(line)

            # parse current clique
            if key == "clique":
                a = conversion_w_none(match.group("a"))
                b = conversion_w_none(match.group("b"))
                c = conversion_w_none(match.group("c"))
                title = str(match.group("title").strip())

                clique_counter += 1

                clique = (clique_counter,  # id
                          a,  # a
                          b,  # b
                          c,  # c
                          title,  # title
                          )

                cliques.append(clique)
                skip_tracks = False

            # parse tracks
            if key == "track" and not skip_tracks:
                track_counter += 1

                track_id = str(match.group("track_id"))
                artist_id = str(match.group("artist_id"))
                performance_id = int(match.group("performance_id"))

                track = (track_counter,  # id
                         clique_counter,  # clique_id
                         track_id,  # track_id
                         artist_id,  # artist_id
                         performance_id,  # performance_id
                         )

                tracks.append(track)

            # in case regex failed skip all tracks for this clique
            if match is None:
                logger.info("Error! Regular expression match error at line:" + str(line))
                logger.info("All associated tracks skipped.")
                skip_tracks = True

            line = file.readline()

    return cliques, tracks


def create_connection(db_file):
    """
    creates a database connection to the SQLite database
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        logger.info(e)

    return None


def create_table(conn, create_table_sql):
    """
    creates a table from the create_table_sql statement
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)

    except Exception as e:
        logger.info(e)


def initialize_database(database, cliques, tracks):
    """
    creates a table from the create_table_sql statement
    """

    if os.path.isfile(database):
        os.remove(database)

    sql_create_cliques_table = """ CREATE TABLE IF NOT EXISTS cliques (
                                        id integer PRIMARY KEY,
                                        a integer,
                                        b integer,
                                        c integer,
                                        title text
                                    ); """

    sql_create_tracks_table = """CREATE TABLE IF NOT EXISTS tracks (
                                    id integer PRIMARY KEY,
                                    clique_id integer NOT NULL,
                                    track_id text,
                                    artist_id text NOT NULL,
                                    performance_id integer,
                                    FOREIGN KEY (clique_id) REFERENCES cliques (id)
                                );"""
    try:
        # create a database connection
        conn = create_connection(database)
    except Exception as e:
        logger.info("Error: " + str(e))
        return False

    if conn is not None:
        try:
            create_table(conn, sql_create_cliques_table)
            create_table(conn, sql_create_tracks_table)

            c = conn.cursor()
            c.executemany("INSERT INTO cliques VALUES (?,?,?,?,?)", cliques)
            c.executemany("INSERT INTO tracks VALUES (?,?,?,?,?)", tracks)

            conn.commit()
            conn.close()

            return True

        except Exception as e:
            logger.info("Error: database transactions failed." + str(e))
            return False
    else:
        logger.info("Error: the database connection failed.")
        return False


def find_songs_per_artist(database, artist_id):
    """
    finds songs in the database by artist id
    """
    try:
        conn = create_connection(database)
        c = conn.cursor()
        t = (artist_id,)
        c.execute("""SELECT title
                    FROM cliques INNER JOIN tracks ON cliques.id=tracks.clique_id 
                    WHERE artist_id=?""", t)

        return c.fetchall()

    except Exception as e:
        logger.info("Error: " + str(e))
        return None


def main():

    # Get and parse command line arguments
    args = Args()

    current_dir = os.path.dirname(os.path.abspath(__file__))

    dataset_file = current_dir + "/data/dataset.txt"
    database = current_dir + "/data/database.db"

    # in case setup argument is used
    if args.setup:
        dataset_url = "https://raw.githubusercontent.com/tbertinmahieux/MSongsDB/master/" \
                       "Tasks_Demos/CoverSongs/shs_dataset_train.txt"

        update_dataset(dataset_url, dataset_file)
        cliques, tracks = parse_file(dataset_file)

        if tracks and cliques:
            logger.info("Info: Data extracted and transformed successfully.")
            if initialize_database(database, cliques, tracks):
                logger.info("Info: Database created and data loaded successfully.")
        else:
            logger.info("Error: dataset parsing issue.")

    if args.artist_id:

        songs = find_songs_per_artist(database, args.artist_id)  # sample string artist = "ARQFFTK1187FB4C7E1"

        if songs:
            logger.info("-----SONGS:-----")

            for s in songs:
                logger.info(s[0])

            logger.info("----------------")

        if songs == []:
            logger.info("No songs has been found for this artist id. Please check id spelling.")

        if songs is None:
            logger.info("Database issues. Please investigate error message above or/and run setup again.")


if __name__ == "__main__":
    main()

