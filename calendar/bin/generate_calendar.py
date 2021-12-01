#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import pandas as pd
from pathlib import Path


def create_week_svg(week, template, output_dp):
    '''
    Create week SVG
    '''
    content = template
    content = content.replace("%month%", week['month'])
    content = content.replace("%week%", "%s" % week['id'])
    print(week['mon'])
    content = content.replace("%mon%", "%s" % week['mon'])
    content = content.replace("%tue%", "%s" % week['tue'])
    content = content.replace("%wed%", "%s" % week['wed'])
    content = content.replace("%thu%", "%s" % week['thu'])
    content = content.replace("%fri%", "%s" % week['fri'])
    content = content.replace("%sat%", "%s" % week['sat'])
    content = content.replace("%sun%", "%s" % week['sun'])

    week_fp = Path(output_dp) / Path("%s.svg" % week['id'])
    with open(week_fp, 'w') as week_f:
        week_f.write(content)


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
    print(date_df)

    week_group = date_df.groupby(["week"])
    for w, group in week_group:
        print(w)
        print(group)
        if w == 52:
            continue
            group1 = group[group.month == 'December']
            week = {
                'id': w,
                'month': 'December',
                'mon': group1[group1.day == 'Monday'].n,
                'tue': group1[group1.day == 'Tuesday'].n,
                'wed': group1[group1.day == 'Wednesday'].n,
                'thu': group1[group1.day == 'Thursday'].n,
                'fri': group1[group1.day == 'Friday'].n,
                'sat': group1[group1.day == 'Saturday'].n,
                'sun': group1[group1.day == 'Sunday'].n
            }
            create_week_svg(week, template)
            group1 = group[group.month == 'January']
            week = {
                'id': w,
                'month': 'January',
                'mon': group1[group1.day == 'Monday'].n,
                'tue': group1[group1.day == 'Tuesday'].n,
                'wed': group1[group1.day == 'Wednesday'].n,
                'thu': group1[group1.day == 'Thursday'].n,
                'fri': group1[group1.day == 'Friday'].n,
                'sat': group1[group1.day == 'Saturday'].n,
                'sun': group1[group1.day == 'Sunday'].n
            }
            create_week_svg(week, template)
        else:
            week = {
                'id': w,
                'month': ' - '.join(list(pd.unique(group.month))),
                'mon': int(group.loc[group.day == 'Monday', 'n']),
                'tue': int(group.loc[group.day == 'Tuesday', 'n']),
                'wed': int(group.loc[group.day == 'Wednesday', 'n']),
                'thu': int(group.loc[group.day == 'Thursday', 'n']),
                'fri': int(group.loc[group.day == 'Friday', 'n']),
                'sat': int(group.loc[group.day == 'Saturday', 'n']),
                'sun': int(group.loc[group.day == 'Sunday', 'n'])
            }
            create_week_svg(week, template, args.output)
