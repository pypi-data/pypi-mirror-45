import click
import multiprocessing
import timeit
from halo import Halo
import os
import sys
import emoji
import json
from gradcafecli.gradcafescraper import GradCafeScraper
from gradcafecli.gradcafeconfig import GradCafeTracking
from datetime import datetime, timedelta


@click.group()
@click.pass_context
def main(ctx):
    tracking_data = get_tracking_data()
    ctx.obj = GradCafeTracking(tracking_data['colleges'], tracking_data['course'], tracking_data['last_updated'])
    """
    A little tool to track acceptance / rejections from grad schools,
    right from the command line.
    """
    #sys.stdout.write("\033[F")

def get_college_specific_data(college, course, date):
    required_data = {
        'college': college,
        'course': course,
        'acceptance': 0,
        'rejections': 0,
        'nodata': False
    }
    data = GradCafeScraper(college, course).prune_data(date)
    college_data = data['data']
    if len(college_data) == 0:
        required_data['nodata'] = True;
        #output_string+=str(emoji.emojize(':school: {0}'.format(college)))
        #output_string+="\n"
        #output_string+=str("\t 😞 No results found on gradcafe")
        #output_string+="\n"
    else:
        for college in college_data:
            college_results = college_data[college]
            accept = college_results['accept']
            reject = college_results['reject']
            required_data['acceptance'] = accept
            required_data['rejections'] = reject
    return required_data

@main.command()
@click.option('--days', '-a', type=int, default=30)
@click.pass_context
def track(ctx, days):
    spinner = Halo(text='🔍 Looking for past {0} days results...'.format(days), spinner='dots')
    spinner.start()
    pool = multiprocessing.Pool(processes=len(ctx.obj.colleges))
    datetime_now = datetime.now()
    date = datetime_now - timedelta(days=days)
    argument_map = zip(ctx.obj.colleges, [ctx.obj.course]*len(ctx.obj.colleges), [date]*len(ctx.obj.colleges))
    pool_outputs = pool.starmap(get_college_specific_data,
                        argument_map)
    pool.close()
    pool.join()
    spinner.stop()
    print_formatted_data(pool_outputs)

@click.argument('course')
@main.command()
@click.pass_context
def track_course(ctx, course):
    ctx.obj.course = course
    set_tracking_data(ctx.obj)
    ack_message = emoji.emojize(':thumbs_up: GradCLI will track all {0} results.'.format(course))
    print(ack_message)

@click.argument('college')
@main.command()
@click.pass_context
def track_college(ctx, college):
    ctx.obj.colleges.append(college)
    ctx.obj.colleges = list(set(ctx.obj.colleges))
    set_tracking_data(ctx.obj)
    ack_message = emoji.emojize(':thumbs_up: GradCLI will track all {0} results.'.format(college))
    print(ack_message)

@click.argument('course')
@main.command()
@click.pass_context
def untrack_course(ctx, course):
    ctx.obj.course = ""
    set_tracking_data(ctx.obj)
    ack_message = emoji.emojize(':thumbs_up: GradCLI will stop tracking all {0} results.'.format(course))
    print(ack_message)

@click.argument('college')
@main.command()
@click.pass_context
def untrack_college(ctx, college):
    if college in ctx.obj.colleges:
        ctx.obj.colleges.remove(college)
        set_tracking_data(ctx.obj)
        ack_message = emoji.emojize(':thumbs_up: GradCLI will stop tracking all {0} results.'.format(college))
    else:
        ack_message = "{0} is not being currently trackked by GradCLI.".format(college)
    print(ack_message)


@main.command()
@click.pass_context
def clear_tracking_data(ctx):
    ctx.obj.clear()
    set_tracking_data(ctx.obj)
    ack_message = emoji.emojize(':thumbs_up: GradCLI has deleted all your trackings.')
    print(ack_message)

@main.command()
@click.pass_context
def display_tracking_data(ctx):
    print(get_tracking_data())

def get_tracking_data():
    config_file = os.path.expanduser('~/.gradcli.cfg')
    with open(config_file) as json_file:  
        data = json.load(json_file)
    return data

def set_tracking_data(obj):
    config_file = os.path.expanduser('~/.gradcli.cfg')
    with open(config_file, 'w') as outfile: 
        json.dump(obj.to_json(), outfile)


def print_formatted_data(data):
    for college_data in data:
        print('🎓 {0} - {1}'.format(college_data['college'], college_data['course']))
        if college_data['nodata']:
            print('\t 😞 No results available on GradCafe')
        else:
            print(emoji.emojize('\t :heavy_check_mark: Acceptance : {0}'.format(college_data['acceptance'])))
            print(emoji.emojize('\t :heavy_multiplication_x: Acceptance : {0}'.format(college_data['rejections'])))


if __name__ == "__main__":
    main()

