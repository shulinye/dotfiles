import markdown
import re
import sys

headers = re.compile(r'(=+)(.*?)\1')
checkboxes = re.compile(r'\[[ *x]\]')
newlines = re.compile(r'\n')
strike = re.compile(r'~~(.*?)~~')

states = {' ': r'&#x2610;',
          '*': r'&#x2611;',
          'x': r'&#x2612;'}


def prettify_checkbox(match):
    return '<span class="checkable">%s</span>' % states[match.group()[1]]

intake = sys.stdin.read()
output = headers.sub(lambda x: '#'* max(1,(6-len(x.groups()[0]))) + x.groups()[1], intake)
output = checkboxes.sub(lambda x: '* ' + x.group(), output)

marked_down = markdown.markdown('[TOC]\n\n' + output, extensions=['markdown.extensions.toc'])
marked_down = strike.sub(r'<strike>\1</strike>', marked_down)
marked_down = marked_down.replace('<ul>\n<li>[', '<ul class="checklist">\n<li>[')
marked_down = checkboxes.sub(prettify_checkbox, marked_down)

final = ['<html><head><link rel="stylesheet" type="text/css" href="style.css"></head><body>', marked_down, '</body></html>']
print('\n'.join(final))
