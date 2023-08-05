# Copyright (c) 2019 Civic Knowledge. This file is licensed under the terms of the
# MIT License, included in this distribution as LICENSE

"""
Function for processing labels from the SAS file
"""

import re

def yield_sps_labels(cdb_file):
    """Extract value labels from the .sps file"""

    with open(cdb_file) as f:

        in_labels = False
        in_label_set = False
        var_id = None

        for line in f.readlines():
            line = line.rstrip()

            if line == '* value labels':
                in_labels = True
                continue

            if in_labels and line == '.':
                in_labels = False
                continue

            if in_labels:

                if not in_label_set and re.match('\s\w+', line):
                    in_label_set = True
                    var_id = line.strip()
                    continue
                elif in_label_set and line.strip() == '/':
                    var_id = None
                    in_label_set = False
                    continue
                elif in_label_set:
                    g = re.match('(-?\d+)\s\"([^\"]+)\"', line.strip())

                    value = g[1]
                    label = g[2]
                    yield var_id, value, label




if __name__ == '__main__':
    f = '/Users/eric/proj/virt-proj/data-project/sdrdl-data-projects/nlsinfo.org/nlsy97_all_1997-2013/' \
        'nlsy97_all_1997-2013.sps'

    extract_labels(f)

