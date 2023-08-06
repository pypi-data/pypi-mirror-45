import argparse, gzip, os, os.path, re, shutil, subprocess, sys

__all__ = ('wtime',)

_round = round
_body = re.compile(r'\n*(?:([^\n]+)\n(=+)\n{2,})?(.+?)(?:\n{2,}--\n{2,}(.+?))?\n*', re.S).fullmatch
_days = re.compile(r'([^\n]+)\n(-+)\n(.*?)\n{3,}', re.S).findall
_zones = re.compile(r'\n{2}').split
_jobs = re.compile(r'(\d+)(?::(\d+))?\s+(\d+)(?::(\d+))?(?:\s+(-??)([+-]\d+))?(?:\s+#(\d+))?(?:\s+(.+?))?\s*$', re.M).findall
_legend = re.compile(r'(\S+)(?:\s+([^:\n]+))?(?:\s*:(.+))?\s*$', re.M).findall

def wtime(file, flags='', background=None, font='Liberation Sans', gap=None, height=None, round=1, size=8, width=None):
	def log(message, status=0):
		nonlocal flags
		if 'q' not in flags and (status or 'v' in flags):
			print(message, file=sys.stderr)
		return status

	if not os.path.exists(file):
		return log('missing file: ' + file, 1)

	if not ('k' in flags or 'z' in flags):
		inkscape = (shutil.which('inkscape') or shutil.which('inkscape.exe', path='C:\\Program Files\\Inkscape') or
			shutil.which('inkscape.exe', path='C:\\Program Files (x86)\\Inkscape'))
		if not inkscape:
			return log('missing Inkscape', 2)
		if (width or height) and 'o' not in flags:
			optipng = shutil.which('optipng')
			if not optipng:
				return log('missing OptiPNG', 2)

	log('parse to SVG')
	with open(file, encoding='utf-8') as f:
		src = f.read()

	title, under, pars, legend_ = _body(src).groups()

	if title and len(title) != len(under):
		return log('syntax error: ' + title, 2)

	legend, style, words = [], [], {}
	cls = 1
	for color, text, words_ in _legend(legend_):
		legend.append(f'<tspan class="c{cls}">&#9632; ' + text.replace(' - ', ' &#8211; ') + '</tspan> &#8194;')
		style.append(f'.c{cls} {{ fill:{color}; }}')
		for w in words_.split():
			words[w] = cls
		cls += 1

	hours = set()
	days = []
	step = _round(size/3, 1)
	size = 3*step
	for day, under, z_pars in _days(pars + 3*'\n'):
		if len(day) != len(under):
			return log('syntax error: ' + day, 2)
		zones, y_max = [], []
		for zone in _zones(z_pars):
			y, ys, jobs = 0, [], []
			for h1, m1, h2, m2, keep, dy, cls, text in _jobs(zone):
				h1, m1 = int(h1), int(m1 or 0)
				h2, m2 = int(h2), int(m2 or 0)
				hours.add((h1, h2 + bool(m2)))
				t1 = 40*h1 + 2*_round(m1/3)
				t2 = 40*h2 + 2*_round(m2/3)
				for j in jobs:
					if y - j[0] < size and t1 < j[2] and j[1] < t2:
						y = j[0] + size
				dy = int(dy or 0)
				y += dy*step
				if not keep and dy < -1:
					for j in jobs:
						if abs(y - j[0]) < 4 and t1 < j[2] and j[1] < t2:
							c = j[3]
							for i in range(len(c)):
								if t1 <= c[i][0] and c[i][1] <= t2:
									del c[i]
								elif c[i][0] < t1 and t2 < c[i][1]:
									c[i:i+1] = [c[i][0], t1], [t2, c[i][1]]
								elif c[i][0] < t1 < c[i][1]:
									c[i][1] = t1
								elif c[i][0] < t2 < c[i][1]:
									c[i][0] = t2
				ys.append(y)
				if not cls:
					cls = 1
					for w in words:
						if w in text:
							cls = words[w]
							break
				jobs.append([y, t1, t2, [[t1, t2]], cls, text])
			y_min = min(ys)
			if y_min:
				for j in jobs:
					j[0] -= y_min
			y_max.append(max(ys) - y_min)
			zones.append(jobs)
		day_height = max(y_max)
		for i in range(len(zones)):
			offset = (day_height - y_max[i])//2
			if offset:
				for j in zones[i]:
					j[0] += offset
		days.append((day, day_height, zones))

	hours = sorted(hours)
	start, end = hours[0]
	g1, g2, hgap = 0, 0, 0
	for h1, h2 in hours:
		if hgap < h1 - end:
			g1, g2 = end, h1
			hgap = h1 - end
		end = max(end, h2)
	if 'c' in flags:
		hgap = 0

	jobs = []
	offset, width_ = 0, 40*(end - start) + (-40*(hgap-2) if hgap else 0 if 'd' in flags else 60)
	gap = gap or size
	for day, day_height, zones in days:
		for zone in zones:
			for j in zone:
				dx = 40*start + ((0 if 'd' in flags else -60) if not hgap else 40*(hgap-2) if 40*g1<j[1] else 0)
				c = 0, 0
				for c_ in j[3]:
					if c[1] - c[0] < c_[1] - c_[0]:
						c = c_
				jobs.append(
					f'<rect class="c{j[4]}" x="{j[1] - dx}" y="{offset + j[0]:.1f}" width="{j[2] - j[1]}" height="{size:.1f}" rx="{round}"/>'
					f'<text x="{(c[0] + c[1])//2 - dx}" y="{offset + j[0] + .8*size:.2f}">{j[5]}</text>')
		offset += day_height + size + gap

	def h_to_x(h):
		nonlocal start, end, g1, g2, hgap
		return 40*((h if h<g2 else h-hgap+2) - start) if hgap else 40*(h-start) + (0 if 'd' in flags else 60)

	rule_half = list(range(start, g1)) + list(range(g2, end)) if hgap else list(range(start, end))
	rule_full = list(range(start, g1+1)) + list(range(g2, end+1)) if hgap else list(range(start, end+1))

	y0 = -(gap//2 + 2)
	rest = f'{y0} v{offset+4:.1f}'
	half = '<path class="half" d="' + ' '.join([f'M{20+h_to_x(r)} {rest}' for r in rule_half]) + '"/>'
	even = ['<path d="' + ' '.join([f'M{h_to_x(r)} {rest}' for r in rule_full if not r%2]) + '"/>']
	odd = ['<path d="' + ' '.join([f'M{h_to_x(r)} {rest}' for r in rule_full if r%2]) + '"/>']
	for y in y0-2, y0+offset+11:
		even += [f'<text x="{h_to_x(r)}" y="{y:.1f}">{r}</text>' for r in rule_full if not r%2]
		odd += [f'<text x="{h_to_x(r)}" y="{y:.1f}">{r}</text>' for r in rule_full if r%2]

	day_column = []
	if 'd' not in flags:
		x = 40*(g1-start+1) if hgap else 20
		y = 0
		if title:
			day_column.append(f'<text x="{x}" y="{y0-2}">{title}</text>')
		for day, day_height, _ in days:
			dy = day_height + size
			day_column.append(f'<text x="{x}" y="{y + (dy+size)/2:.1f}">{day}</text>')
			y += dy + gap

	rx, ry, rwidth, rheight = -20, -(gap//2+20), width_ + 40, y0 + offset + gap + 55
	back = f'<rect x="{rx}" y="{ry}" width="{rwidth}" height="{rheight:.1f}"'

	svg = f'''\
<svg viewBox="{rx} {ry} {rwidth} {rheight:.1f}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
	<style>
		rect {{ stroke:white; stroke-width:.5; }}
		text {{ fill:white; font-family:{font}; font-size:{.7*size:.2f}pt; text-anchor:middle; }}
		path {{ stroke:gray; stroke-width:.6; }}
		path.half {{ stroke-dasharray:1; stroke-width:.2; }}
		g.odd path {{ stroke-width:.3; }}
		g.even text, g.odd text, g.days text {{ fill:gray; font-size:{.6*size:.2f}pt; }}
		g.odd text {{ font-size:{.5*size:.2f}pt; }}
		rect.back {{ opacity:0; }}
		''' + '\n\t\t'.join(style) + f'''
	</style>

	<defs>
		<filter id="shadow" x="0" y="0" width="1" height="1">
			<feOffset in="SourceAlpha" dx="2" dy="2"/>
			<feColorMatrix values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 .3 0"/>
			<feGaussianBlur stdDeviation="1"/>
		</filter>

		<g id="jobs">
			<rect class="back" x="{rx}" y="{ry}" width="{rwidth}" height="{rheight:.1f}"/>
			''' + '\n\t\t\t'.join(jobs) + f'''
		</g>
	</defs>

	<use xlink:href="#jobs" filter="url(#shadow)"/>

	<g class="even">
		''' + '\n\t\t'.join(even) + '''
	</g>
	<g class="odd">
		''' + '\n\t\t'.join(odd) + '''
	</g>
	''' + half + '''
	<g class="days">
		''' + '\n\t\t'.join(day_column) + f'''
	</g>

	<use xlink:href="#jobs"/>

	<text x="{width_//2}" y="{rheight+ry-10:.1f}">
		''' + '\n\t\t'.join(legend) + '''
	</text>
</svg>'''

	file = os.path.splitext(file)[0]

	if 'z' in flags:
		log('compress to SVGZ')
		with gzip.open(file + '.svgz', 'wt', encoding='utf-8', newline='\n') as f:
			f.write(svg)
	else:
		with open(file + '.svg', 'w', encoding='utf-8', newline='\n') as f:
			f.write(svg)
		if 'k' not in flags:
			if width or height:
				log('render to PNG: inkscape -e')
				subprocess.run([inkscape, file + '.svg', '-e', file + '.png'] +
					(['-w', str(width)] if width else []) + (['-h', str(height)] if height else []) +
					(['-b', background] if background else []))
				if 'o' not in flags:
					log('optimize PNG: optipng -o7 -strip all')
					subprocess.run([optipng, '-o7', '-strip', 'all', file + '.png'], stderr=subprocess.DEVNULL)
			else:
				log('render to PDF: inkscape -A')
				subprocess.run([inkscape, file + '.svg', '-A', file + '.pdf'])
			log('delete SVG')
			os.remove(file + '.svg')

def main():
	a = argparse.ArgumentParser(None, 'wtime [-cdkoqvz] [-b B] [-f F] [-g G] [-h H] [-r R] [-s S] [-w W] file',
		'Week Time 0.3', add_help=False)
	a.add_argument('file', nargs='?', help='*.txt input file')
	a.add_argument('-b', '--background', metavar='B', help='PNG background color (transparent)')
	a.add_argument('-c', '--no-compact', action='store_true', help='days always to the left')
	a.add_argument('-d', '--no-days', action='store_true', help='no days column')
	a.add_argument('-f', '--font', metavar='F', default='Liberation Sans', help='font family (Liberation Sans)')
	a.add_argument('-g', '--gap', metavar='G', type=int, help='gap height (size)')
	a.add_argument('-h', '--height', metavar='H', type=int, help='PNG height, otherwise PDF')
	a.add_argument('-k', '--keep', action='store_true', help='keep SVG, do not run Inkscape')
	a.add_argument('-o', '--no-optipng', action='store_true', help='do not run OptiPNG')
	a.add_argument('-q', '--quiet', action='store_true', help='no output')
	a.add_argument('-r', '--round', metavar='R', type=int, default=1, help='box radius (1)')
	a.add_argument('-s', '--size', metavar='S', type=int, default=8, help='box height (8)')
	a.add_argument('-v', '--verbose', action='store_true', help='show actions')
	a.add_argument('-w', '--width', metavar='W', type=int, help='PNG width, otherwise PDF')
	a.add_argument('-z', '--zip', action='store_true', help='compress to SVGZ, do not run Inkscape')
	args = a.parse_args()
	if args.file:
		return wtime(args.file, ('c' if args.no_compact else '') + ('d' if args.no_days else '') +
			('k' if args.keep else '') + ('o' if args.no_optipng else '') +
			('q' if args.quiet else '') + ('v' if args.verbose else '') + ('z' if args.zip else ''),
			args.background, args.font, args.gap, args.height, args.round, args.size, args.width)
	a.print_help()

if __name__ == '__main__':
	exit(main())