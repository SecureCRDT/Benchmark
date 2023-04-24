#!/usr/bin/env python3
import glob
import pathlib
from typing import Dict

import pandas as pd

modes = ["BASELINE", "SMPC"]

operations = ["query", "update"]

nusers = ["1", "2", "4", "8", "16", "32", "64"]


def generate_gnuplot(df, crdts, operations):

    for mode in modes:
        for crdt in crdts:
            for operation in operations:
                p = pathlib.Path(f"gnuplot/data/{mode}/{crdt}")
                p.mkdir(parents=True, exist_ok=True)
                filepath = p / f"{operation}.dat"
                with filepath.open("w", encoding="utf-8") as f:
                    for user in nusers:
                        rows = df.query(
                            f"crdt == '{crdt}' and encryption == '{mode}' and crdt_op == '{operation}' and nclients == '{user}' ")
                        if len(rows) == 1:
                            row = rows.iloc[0]
                            latency = row['Average Response Time']
                            thr = row['Requests/s']
                            f.write(f"{thr} {latency}\n")


def generate_gnuplot_inc_dec_counters(df):
    crdts = ["minboundedcounter", "pncounter"]
    operations = ['update']
    for mode in modes:
        for crdt in crdts:
            for operation in operations:

                p = pathlib.Path(f"gnuplot/data/{mode}/{crdt}")
                p.mkdir(parents=True, exist_ok=True)
                inc_filepath = p / f"increment.dat"
                dec_filepath = p / f"decrement.dat"

                inc_file = inc_filepath.open("w", encoding="utf-8")
                dec_file = dec_filepath.open("w", encoding="utf-8")
                file = None

                for user in nusers:
                    rows = df.query(
                        f"crdt == '{crdt}' and encryption == '{mode}' and crdt_op == '{operation}' and nclients == '{user}' ")
                    for index, row in rows.iterrows():
                        if 'inc' in row['Name']:
                            file = inc_file
                        elif 'dec' in row['Name']:
                            file = dec_file

                        latency = row['Average Response Time']
                        thr = row['Requests/s']
                        file.write(f"{thr} {latency}\n")

                inc_file.close()
                dec_file.close()


def parse_files(path: str) -> Dict:
    # csv files in the path
    # Results folder without number of clients
    # files = glob.glob(path + "/*/*/*/*.csv_stats.csv")
    # Results folder with number of clients
    files = glob.glob(path + "/*/*/*/*/*.csv_stats.csv")
    # defining an empty list to store
    # content
    data_frame = pd.DataFrame()
    content = []

    # checking all the csv files in the
    # specified path
    for filename in files:
        # reading content of csv file
        # content.append(filename)
        df = pd.read_csv(filename, index_col=None)
        # name = "/".join(filename.split("/")[1:4])
        filepath = filename.split("/")
        # print(filepath)
        encryption_mode = filepath[1]
        crdt = filepath[2]
        crdt_operation = filepath[3]
        nclients = filepath[4]
        if  "minboundcounter" in filename:
            continue

        # print(encryption_mode)
        # print(crdt)
        # print(crdt_operation)
        # print(nclients)

        if crdt_operation in ['propagate', 'merge']:
            continue

        df['encryption'] = encryption_mode
        df['crdt'] = crdt
        df['nclients'] = nclients
        df['crdt_op'] = crdt_operation

        content.append(df)

    # converting content to data frame
    data_frame = pd.concat(content)
    data_frame = data_frame[
        data_frame['Name'].isin(['on_start', 'on_start_inc', 'on_start_setup', 'Aggregated']) == False]
    data_frame.groupby(by=['crdt', 'crdt_op', 'encryption'])
    # print(data_frame)
    print(data_frame[["nclients", "crdt", "encryption", "crdt_op", "Average Response Time", "Requests/s"]].to_string(
        index=False))
    data_frame[["nclients", "crdt", "encryption", "crdt_op", "Average Response Time", "Requests/s"]].to_excel(
        'results_bounded_counter.xlsx', index=False, header=True)
    data_frame.to_excel('results_bounded_counter_full.xlsx', index=False, header=True)

    #generate_gnuplot(data_frame, ["gcounter", "register", "maxvalue", "minboundedcounter", "pncounter"], ["query"])
    #generate_gnuplot(data_frame, ["gcounter", "register", "maxvalue"], ["update"])
    #generate_gnuplot_inc_dec_counters(data_frame)

    return data_frame


if __name__ == '__main__':
    parse_files("results_bounded_counter")
