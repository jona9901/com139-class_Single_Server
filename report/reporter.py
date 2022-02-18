from analysis.analyzer import *
from simulation.config import *
from assets.status import Status

import matplotlib.pyplot as plt
import numpy as np
import sys

# TODO: Create report of multiple executions
default_out = './report.txt'

status_values = list()

def report_all_by_field_obj(my_objs: list, my_field: str, w_filter: bool = False, val: float = 0.0) -> None:
    print('\n === Report for %s field ===' % my_field)
    is_status = isinstance(getattr(my_objs[0], my_field), Status)
    if not is_status:
        max_time = get_max_obj(my_objs, my_field, w_filter, val)
        min_time = get_min_obj(my_objs, my_field, w_filter, val)
        print('Max %s: %5.3f by %s' %
              (my_field, max_time, objects_as_str(get_matching_value_obj(my_objs, my_field, max_time))))
        print('Min %s: %5.3f by %s' %
              (my_field, min_time, objects_as_str(get_matching_value_obj(my_objs, my_field, min_time))))
        print('Mean %s: %5.3f' % (my_field, get_mean_obj(my_objs, my_field, w_filter, val)))
        print('Median %s: %5.3f' % (my_field, get_median_obj(my_objs, my_field, w_filter, val)))
        try:
            print('Mode %s: %5.3f' % (my_field, get_mode_obj(my_objs, my_field, w_filter, val)))
        except Exception:
            print('No mode found in data')
        print('Stdev %s: %5.3f' % (my_field, get_stdev_obj(my_objs, my_field, w_filter, val)))
        print('Variance %s: %5.3f' % (my_field, get_variance_obj(my_objs, my_field, w_filter, val)))
        # TODO: Calculate the percentage of minimal value
        matchingVal = get_matching_value_obj(my_objs, my_field, min_time)
        minimal_p = len(matchingVal) / NEW_CUSTOMERS
        print('Percentage of minimal value: %f' % minimal_p)
        # TODO: Group std dev customers and display the list
    else:
        #print(is_status)
        values = get_map_values(my_objs, my_field)
        
        undefined = 0
        success = 0
        wait = 0
        reneged = 0

        for value in values:
            if (value == Status.UNDEFINED):
                undefined += 1
            elif (value == Status.SUCCESS):
                success += 1
            elif (value == Status.WAIT):
                wait += 1
            elif (value == Status.RENEGED):
                reneged += 1
        

        status_values.append(undefined)
        status_values.append(success)
        status_values.append(wait)
        status_values.append(reneged)

        print("Undefined: %d" % undefined)
        print("Success: %d" % success)
        print("Wait: %d" % wait)
        print("Reneged: %d" % reneged)

        # TODO: get a histogram count on every status
        # TODO: graph the histogram
        # TODO: get success rate
        success_rate = success * 100 / len(values)
        print('success_rate %f' % success_rate)

        #bar_plot([undefined, success, wait, reneged])
        #status_values = [undefined, success,  wait, reneged]
        if CREATE_SIM_GRAPHS:
            # Plot Histogram
            bar_plot(status_values)

        report_multiple_runs(success, undefined, wait, reneged)


def report_all_by_ts(my_ts: list, my_label: str, total_time: float) -> None:
    print('\n === Report for %s resource ===' % my_label)
    if my_ts:
        # print_ts(my_ts, my_label)
        # print('Min queue: %4.3f' % get_min_ts(my_ts))
        print('Max queue: %4.3f' % get_max_ts(my_ts))
        service_vals = get_cumulative_time_ts(my_ts, total_time)
        percent_vals = get_bin_percent_ts(service_vals, total_time, my_label)
        if CREATE_SIM_GRAPHS:
            plot_ts(my_ts, total_time, my_label)
            evolution_bar_ts(my_ts, total_time, my_label)
            cumulative_time_ts(service_vals, my_label)
            hist_bar_ts(my_ts, 'value', my_label)
    else:
        print('%s not used' % my_label)

def report_multiple_runs(success: int, undefined:int, wait:int, reneged:int) -> None:
    out = default_out
    if len(sys.argv) > 1:
        out = sys.argv[1]
    file = open(out, 'a')
    
    file.write('Number of customers: {}\nNumber of cashiers: {}\n\n'.format(NEW_CUSTOMERS, CAPACITY))
    file.write(' === Report for Status field ===\n' )
    file.write('Success count: {}\nUndefined count: {}\nWait count: {}\nReneged count: {}\n'.format(success, undefined, wait, reneged))
    print('Success rate: {}%'.format(success))
    file.write('Success rate: {}%\n'.format(success))
    file.write('----------------------------\n')
    file.close() 
