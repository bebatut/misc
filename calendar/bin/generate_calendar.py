#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import pandas as pd
from pathlib import Path
from pikepdf import Pdf
from subprocess import Popen


def waitForResponse(x):
    ''''''
    out, err = x.communicate()
    if x.returncode < 0:
        r = "Popen returncode: " + str(x.returncode)
        raise OSError(r)


def get_day_number(day, group):
    ''''''
    v = group.loc[group.day == day, 'n']
    if len(v) == 1:
        return int(v)
    else:
        return ''


def create_week(group, w):
    '''Create week dictionary'''
    week = {
        'id': w,
        'month': ' - '.join(list(pd.unique(group.month))),
        'mon': get_day_number('Monday', group),
        'tue': get_day_number('Tuesday', group),
        'wed': get_day_number('Wednesday', group),
        'thu': get_day_number('Thursday', group),
        'fri': get_day_number('Friday', group),
        'sat': get_day_number('Saturday', group),
        'sun': get_day_number('Sunday', group)
    }
    return week


def create_week_files(week, template, output_dp, pdf):
    '''Create week SVG'''
    # replace content in template
    content = template
    content = content.replace("%month%", week['month'])
    content = content.replace("%week%", "%s" % week['id'])
    content = content.replace("%mon%", "%s" % week['mon'])
    content = content.replace("%tue%", "%s" % week['tue'])
    content = content.replace("%wed%", "%s" % week['wed'])
    content = content.replace("%thu%", "%s" % week['thu'])
    content = content.replace("%fri%", "%s" % week['fri'])
    content = content.replace("%sat%", "%s" % week['sat'])
    content = content.replace("%sun%", "%s" % week['sun'])
    # generate svg file
    svg_fp = Path(output_dp) / Path("%s.svg" % week['id'])
    pdf_fp = Path(output_dp) / Path("%s.pdf" % week['id'])
    with open(svg_fp, 'w') as week_f:
        week_f.write(content)
    # generate pdf file
    x = Popen([
        '/usr/bin/inkscape',
        svg_fp,
        '--export-pdf=%s' % pdf_fp])
    try:
        waitForResponse(x)
    except OSError:
        return False
    # add pdf
    src = Pdf.open(pdf_fp)
    pdf.pages.extend(src.pages)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate weekly calendar')
    parser.add_argument('--start', '-s', required=True, help="Start date in format Y-M-D")
    parser.add_argument('--end', '-e', required=True, help="End date in format Y-M-D")
    parser.add_argument('--template', '-t', required=True, help="Path to SVG template file")
    parser.add_argument('--output', '-o', required=True, help="Output folder")
    args = parser.parse_args()

    # load template SVG
    template_fp = Path(args.template)
    with open(template_fp, 'r') as template_f:
        template = template_f.read()

    # create week details
    date_df = (pd.DataFrame({"date": pd.date_range(args.start, args.end)})
        .assign(
            week=lambda x: x['date'].dt.week,
            day=lambda x: x['date'].dt.strftime('%A'),
            month=lambda x: x['date'].dt.strftime('%B'),
            n=lambda x: x['date'].dt.strftime("%d")
        ))


    # create week svg
    week_group = date_df.groupby(["week"])
    pdf = Pdf.new()
    for w, group in week_group:
        if w == 52:
            # december
            group1 = group[group.month == 'December']
            week = create_week(group1, 52)
            create_week_files(week, template, args.output, pdf)
            # january
            group1 = group[group.month == 'January']
            week = create_week(group1, 0)
            create_week_files(week, template, args.output, pdf)
        else:
            week = create_week(group, w)
            create_week_files(week, template, args.output, pdf)

    # generate final PDF
    pdf.save(Path(args.output) / Path('calendar.pdf'))
