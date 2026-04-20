#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from Alphabet import RUNES
from LPath import FILES_ALL, FILES_SOLVED, FILES_UNSOLVED, LPath
from InterruptDB import InterruptDB
from InterruptIndices import InterruptIndices

NORM_MIN = 0.40
NORM_MAX = 0.98
HIGH_MIN = 1.25
HIGH_MAX = 1.65
MEM_DB = None  # stores a DBToMem object


#########################################
#  DBToMem  :  Loads all dbs into memory so you don't need to re-read each
#########################################

class DBToMem(object):
    def __init__(self):
        lsc = InterruptDB.load_scores
        self.indices = InterruptIndices()
        self.db = {}
        for ioc_kind in ['high', 'norm']:
            prfx = 'db_' + ioc_kind
            self.db[ioc_kind] = {
                'main': lsc(prfx),
                'mod': {typ: [
                        (mod, p, lsc(prfx + f'_mod_{typ}_{mod}.{p}'))
                        for mod in range(2, 4) for p in range(mod)]
                        for typ in 'ab'},
                'mirror': {typ: lsc(prfx + f'_pattern_mirror_{typ}.0')
                           for typ in 'ab'},
                'shift': {kl: lsc(prfx + f'_pattern_shift_{kl}.0')
                          for kl in range(4, 19)},
            }

    def vertical_kl(self, tbl, iocKey, fname, irp, kl_range):
        pointer = self.db[iocKey]['main'][fname][irp]
        maxscore = 0
        bestkl = -1
        for kl in kl_range:
            try:
                score = pointer[kl][0]
                tbl[kl].append(score)
                if score > maxscore:
                    maxscore = score
                    bestkl = kl
            except KeyError:
                tbl[kl].append('–')
        return bestkl


#########################################
#  HTML helper class
#########################################

class HTML(object):
    @staticmethod
    def attr(attrib):
        txt = ''
        if attrib:
            for k, v in attrib.items():
                txt += f' {k}="{v}"'
        return txt

    @staticmethod
    def mark(x, low=0, high=1):
        if x <= low:
            return ' class="m0"'
        return f' class="m{int((min(high, x) - low) / (high - low) * 14) + 1}"'

    @staticmethod
    def p_warn(content):
        return f'<p class="red">{content}</p>\n'

    @staticmethod
    def dt_dd(title, content, attrib=None):
        return f'<dt>{title}</dt>\n<dd{HTML.attr(attrib)}>\n{content}</dd>\n'

    @staticmethod
    def num_stream(stream, score_min=0, score_max=1):
        dot2 = isinstance(score_min, float) or isinstance(score_max, float)
        txt = ''
        for x in stream:
            txt += '<div'
            if isinstance(x, tuple):
                txt += HTML.attr(x[0])
                x = x[1]
            if not isinstance(x, str):
                txt += HTML.mark(x, score_min, score_max)
            txt += f'>{x:.2f}</div>' if dot2 else f'>{x}</div>'
        return txt + '\n'

    @staticmethod
    def num_table(table, num_ranges, thr=1, thc=1):
        txt = '<table>\n'
        for r, row in enumerate(table):
            attr = ''
            if isinstance(row, tuple):
                attr = HTML.attr(row[0])
                row = row[1]
            txt += f'<tr{attr}>'
            for c, val in enumerate(row):
                td = 'th' if r < thr or c < thc else 'td'
                attr = ''
                if isinstance(val, tuple):
                    attr = HTML.attr(val[0])
                    val = val[1]
                isnum = False
                dot2 = False
                if not isinstance(val, str):
                    for sc_min, sc_max, L, T, R, B in num_ranges:
                        if c >= L and c < R and r >= T and r < B:
                            isnum = True
                            attr += HTML.mark(val, sc_min, sc_max)
                            dot2 = isinstance(sc_min, float) \
                                or isinstance(sc_max, float)
                            break
                if isnum:
                    if val <= 0:
                        txt += f'<{td}>–</{td}>'
                    elif dot2:
                        txt += f'<{td}{attr}>{val:.2f}</{td}>'
                    else:
                        txt += f'<{td}{attr}>{val}</{td}>'
                else:
                    txt += f'<{td}{attr}>{val}</{td}>'
            txt += '</tr>\n'
        return txt + '</table>\n'


#########################################
#  InterruptToWeb  :  Read interrupt DB and create html graphic / matrix
#########################################

class InterruptToWeb(object):
    def __init__(self, template='templates/ioc.html'):
        with open(LPath.results(template), 'r') as f:
            self.template = f.read()

    def table_reliable(self, iocKey):
        head = [''] + [f'<div>{x}</div>' for x in FILES_ALL]
        foot = ['Total'] + [MEM_DB.indices.total(x) for x in FILES_ALL]

        tbl = [[irp] for irp in RUNES]
        for name in FILES_ALL:
            pointer = MEM_DB.db[iocKey]['main'][name]
            for irp in range(29):
                maxirp = set(maxirp for _, maxirp in pointer[irp].values())
                worst_irp_c = min(maxirp)
                if worst_irp_c == 0 and max(maxirp) != 0:
                    tbl[irp].append('?')
                    continue
                _, num = MEM_DB.indices.consider(name, irp, worst_irp_c)
                tbl[irp].append(num)

        tbl.insert(0, ({'class': 'rotate'}, head))
        tbl.append(({'class': 'small'}, foot))
        return HTML.num_table(tbl, [(384, 812, 1, 1, 99, len(tbl) - 1)])

    def table_interrupt(self, iocKey, irp, pmin, pmax):
        head = [''] + [f'<div>{x}</div>' for x in FILES_ALL]
        foot = ['best']

        tbl = [[kl] for kl in range(33)]
        for ni, name in enumerate(FILES_ALL):
            bestkl = MEM_DB.vertical_kl(tbl, iocKey, name, irp, range(1, 33))
            foot.append(bestkl)

        tbl[0] = ({'class': 'rotate'}, head)
        tbl.append(({'class': 'small'}, foot))
        return HTML.num_table(tbl, [(pmin, pmax, 1, 1, 99, len(tbl) - 1)])

    def make(self, iocKey, outfile, pmin, pmax):
        nav = ''
        txt = ''
        for i in range(29):
            nav += f'<a href="#tb-i{i}">{RUNES[i]}</a>\n'
            txt += f'<h3 id="tb-i{i}">Interrupt {i}: <b>{RUNES[i]}</b></h3>'
            txt += self.table_interrupt(iocKey, i, pmin, pmax)
        html = self.template.replace('__NAVIGATION__', nav)
        html = html.replace('__TAB_RELIABLE__', self.table_reliable(iocKey))
        html = html.replace('__INTERRUPT_TABLES__', txt)
        with open(LPath.results(outfile), 'w') as f:
            f.write(html)


#########################################
#  ChapterToWeb  :  Combine different analyses for a single chapter
#########################################

class ChapterToWeb(object):
    def __init__(self, template='templates/pages.html'):
        with open(LPath.results(template), 'r') as f:
            self.template = f.read()

    def sec_ioc(self, fname):
        tbl = [[x] for x in range(33)]
        foot = ['best']
        for typ in ['high', 'norm']:
            for irp in [0, 28]:
                bestkl = MEM_DB.vertical_kl(tbl, typ, fname, irp, range(1, 33))
                foot.append(bestkl)

        for irp in [0, 28]:
            for kl in range(1, 33):
                score, maxirp = MEM_DB.db['high']['main'][fname][irp][kl]
                _, num = MEM_DB.indices.consider(fname, irp, maxirp)
                tbl[kl].append(num // kl)

        tbl[0] = ['',
                  ({'colspan': 2}, 'IoC-<a href="./ioc/high.html">high</a>'),
                  ({'colspan': 2}, 'IoC-<a href="./ioc/norm.html">norm</a>'),
                  ({'colspan': 2}, 'Runes / keylen')]
        tbl.insert(1, [''] + [RUNES[irp] for irp in [0, 28]] * 3)
        tbl.append(({'class': 'small'}, foot))
        return HTML.num_table(tbl, [
            (HIGH_MIN, HIGH_MAX, 1, 2, 3, len(tbl) - 1),
            (NORM_MIN, NORM_MAX, 3, 2, 5, len(tbl) - 1),
            (28, 100, 5, 2, 7, len(tbl) - 1)
        ], thr=2)

    def sec_ioc_mod(self, fname):
        def add_line():
            res = []
            for kl, (score, maxirp) in scores[fname][irp].items():
                if kl > len(res):
                    res += [''] * (kl - len(res))
                res[kl - 1] = score
            if typ == 'a':
                _, num = MEM_DB.indices.consider(fname, irp, maxirp)
                num = num // mod + (1 if off < num % mod else 0)
            else:
                _, num = MEM_DB.indices.consider_mod_b(
                    fname, irp, maxirp, mod)
                num = num[off]
            return num, res

        txt = '<dl>\n'
        for typ, title, min_kl in [('a', 'Interrupt first, then mod', 1),
                                   ('b', 'Mod first, then interrupt', 2)]:
            for kind, pmin, pmax in [('high', HIGH_MIN, HIGH_MAX),
                                     ('norm', NORM_MIN, NORM_MAX)]:
                tbl = []
                max_kl = 0
                for irp in [0, 28]:
                    for mod, off, scores in MEM_DB.db[kind]['mod'][typ]:
                        num, line = add_line()
                        max_kl = max(max_kl, len(line))
                        line = line[min_kl - 1:]
                        tbl.append([f'{RUNES[irp]}.{mod}.{off}', num] + line)

                head = [['', 'runes'] + [i for i in range(min_kl, max_kl + 1)]]
                tbl = HTML.num_table(head + tbl, [(pmin, pmax, 2, 1, 99, 99)])
                ttl = f'{title} (IoC-<a href="../ioc/{kind}.html">{kind}</a>):'
                txt += HTML.dt_dd(ttl, tbl)
        return txt + '</dl>\n'

    def sec_ioc_pattern(self, fname):
        def sub_table(title, key, variants, cols):
            txt = ''
            per_kl = key == 'shift'
            for kind, pmin, pmax in [('high', HIGH_MIN, HIGH_MAX),
                                     ('norm', NORM_MIN, NORM_MAX)]:
                tbl = []
                for irp in [0, 28]:
                    for typ in variants:
                        pointer = MEM_DB.db[kind][key][typ][fname][irp]
                        scores = []
                        for kl in cols:
                            try:
                                scores.append(pointer[kl][0])
                            except KeyError:
                                break
                        _, num = MEM_DB.indices.consider(fname, irp, 20)
                        if per_kl:
                            actual_kl = int(typ)
                            num //= actual_kl
                        tbl.append([f'{RUNES[irp]}.{typ}', num] + scores)
                head = [['', 'runes'] + [i for i in cols]]
                colors = [(pmin, pmax, 2, 1, 99, 99)]
                if per_kl:
                    colors.append((28, 100, 1, 1, 2, 99))
                tbl = HTML.num_table(head + tbl, colors)
                ttl = f'{title} (IoC-<a href="../ioc/{kind}.html">{kind}</a>):'
                txt += HTML.dt_dd(ttl, tbl)
            return txt

        txt = '<dl>\n'
        txt += sub_table('Mirror Pattern', 'mirror', 'ab', range(4, 19))
        txt += sub_table('Shift Pattern', 'shift', range(4, 19), range(1, 18))
        return txt + '</dl>\n'

    def make(self, fname, outfile):
        html = self.template.replace('__FNAME__', fname)
        if fname.startswith('solved_'):
            ref = f'<a href="./{fname[7:]}.html">“unsolved” page</a>'
            html = html.replace('__SEC_IOC__', HTML.p_warn(
                f'IoC is disabled on solved pages. Open the {ref} instead.'))
        else:
            html = html.replace('__SEC_IOC__', self.sec_ioc(fname))
        if fname in FILES_UNSOLVED:
            html = html.replace('__SEC_IOC_MOD__', self.sec_ioc_mod(fname))
            html = html.replace('__SEC_IOC_PATTERN__',
                                self.sec_ioc_pattern(fname))
        else:
            html = html.replace('__SEC_IOC_MOD__', HTML.p_warn(
                'Mod-IoC is disabled on solved pages'))
            html = html.replace('__SEC_IOC_PATTERN__', HTML.p_warn(
                'Pattern-IoC is disabled on solved pages'))
        with open(LPath.results(outfile), 'w') as f:
            f.write(html)


#########################################
#  IndexToWeb  :  Creates the index page with links to all other analysis pages
#########################################

class IndexToWeb(object):
    def __init__(self, template='templates/index.html'):
        with open(LPath.results(template), 'r') as f:
            self.template = f.read()

    def make(self, the_links, outfile='index.html'):
        html = self.template
        for key, links in the_links.items():
            html = html.replace(
                key, ' '.join(f'<a href="./{x}">{y}</a>' for x, y in links))
        with open(LPath.results(outfile), 'w') as f:
            f.write(html)


#########################################
#  main entry
#########################################

if __name__ == '__main__':
    links = {
        '__A_IOC__': [('ioc/high.html', 'Highest (bluntly)'),
                      ('ioc/norm.html', 'Normal english (1.7767)')],
        '__A_CHAPTER__': [(f'pages/{x}.html', x) for x in FILES_UNSOLVED],
        '__A_SOLVED__': [(f'pages/{x}.html', x) for x in FILES_SOLVED],
    }
    MEM_DB = DBToMem()
    iocweb = InterruptToWeb()
    iocweb.make('high', 'ioc/high.html', HIGH_MIN, HIGH_MAX)
    iocweb.make('norm', 'ioc/norm.html', NORM_MIN, NORM_MAX)
    ctw = ChapterToWeb()
    for x, y in links['__A_CHAPTER__'] + links['__A_SOLVED__']:
        ctw.make(y, x)
    IndexToWeb().make(links)
