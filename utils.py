def progress_bar(completed, total, prefix=None, sufix=None, finish_message=None):
    
    prefix = ' ' + prefix + ':' if prefix is not None else ''
    sufix = ' ' + sufix if sufix is not None else ''

    percentage = 100 * (completed / float(total))
    scaled_perc = int(50 * (percentage / 100.0))
    bar = ' |' + '█' * (scaled_perc - 1 ) + '-' * (50 - scaled_perc) + '| '

    if completed == total:
        print(prefix + '\t' + bar + f'[{completed}/{total}] {percentage:.1f}%' + sufix)
        if finish_message is not None:
            print(' ' + finish_message)
    else:
        print(prefix + '\t' + bar + f'[{completed}/{total}] {percentage:.1f}%', end='\r')


def sanitize_name(dirty_name):
    clean_name = dirty_name.replace(' ', '_').replace('/', '_').replace('\'', '').replace('\"', '')
    return clean_name

