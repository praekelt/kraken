# A module for doing tsung things (yeah..)

import time
import re
import json

def parse_stats(logfile):
    """
    Takes a tsung stats log, returns JSON in some more useful structure
    """

    stats = open(logfile)

    block_marker = re.compile(r'^# stats: dump at (\d+)')

    stats_marker = re.compile(r'^stats: (\w+) (.+)$')

    start_time = None
    block_time = None

    data = {}

    for ln in stats:
        # Construct a more compact time-series
        mark = block_marker.match(ln)
        if mark:
            if not start_time:
                start_time = int(mark.groups()[0])

            block_time = int(mark.groups()[0]) - start_time

        elif stats_marker.match(ln):
            stats = stats_marker.match(ln).groups()
            stat_name = stats[0]
            stat_data = []

            for num in stats[1].split():
                if '.' in num:
                    stat_data.append(float(num))
                else:
                    stat_data.append(int(num))
            
            if not stat_name in data:
                data[stat_name] = []
            data[stat_name].append((block_time, stat_data))

    json_data = {
        'start_time': start_time, 
        'data': data
    }

    return json.dumps(json_data)
