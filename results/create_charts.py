# from brokenaxes import brokenaxes
import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def create_chart(spec, output_md):
    print('Processing {} "{}"'.format(spec['data'], spec['title']))

    plt.style.use('ggplot')

    png_file = os.path.splitext(spec['data'])[0] + ".png"

    output_md += "\n# {}\n\n".format(spec['title'])
    output_md += "(tested by {} on {})\n\n".format(spec['by'], spec['date'])

    df = pd.read_csv(spec['data'])
    m = df.mean().sort_values(ascending=False)

    output_md += '![{}]({}?raw=true "{}")\n\n'.format(png_file, png_file, png_file)

    output_md += "Details:\n"
    output_md += "| Test   | Time (ms) | \n"
    output_md += "|--------| --------: |\n"

    for i in range(len(m.index)):
        output_md += "| {} | {} |\n".format(m.index[i], "%.3f" % m[i])

    output_md += "\n"

    # Remove outliers as we don't support broken/discontinuous axis yet
    notes = ""
    for i in range(len(m) - 1):
        if m[i] / m[i + 1] > 20:
            # print('** Warning: removing outlier "%s" from the chart' % m.index[i])
            notes += '- outliner "{}" is removed from the chart\n'.format(m.index[i])
        else:
            break

    if notes:
        output_md += "\nNotes:\n" + notes

    m = m[i:]

    tests = m.index
    y_pos = np.arange(len(tests))
    y = m
    error = None
    xlims = None

    fig = plt.figure(figsize=(8, 1.5 + 0.6 * len(m)))
    if xlims:
        ax = brokenaxes(xlims=xlims, hspace=.05)
    else:
        ax = plt.subplot(111)

    ax.barh(y_pos, y, xerr=error, align='center', color='green', ecolor='black')
    for i, v in enumerate(y):
        ax.text(v + 3, i + .25, '%.3f' % v)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(tests)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Time (ms)')
    ax.set_title(spec['title'])

    ax.grid(color='w')
    plt.savefig(png_file)

    output_md += "\n\n"
    return output_md


README_MD = """
# Results

This is autogenerated page from the results recorded in CSV and [result_specs.json](result_specs.json)
file. To submit a result:
1. Record your test results in a CSV file. Repeat a test by at least 5 times. See other csv files for samples.
2. Create an entry in result_specs.json
3. Create pull request
"""

if __name__ == "__main__":
    specs = json.loads(open('result_specs.json').read())
    output_md = README_MD

    for spec in specs:
        output_md = create_chart(spec, output_md)

    print('Writing README.md..')
    f = open('README.md', 'w')
    f.write(output_md)
    f.close()
