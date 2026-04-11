#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os.path

FILES_SOLVED = ['0_warning', '0_welcome', '0_wisdom', '0_koan_1',
                '0_loss_of_divinity', 'jpg107-167', 'jpg229',
                'p56_an_end', 'p57_parable']
FILES_UNSOLVED = ['p0-2', 'p3-7', 'p8-14', 'p15-22', 'p23-26',
                  'p27-32', 'p33-39', 'p40-53', 'p54-55']
FILES_ALL = FILES_UNSOLVED + FILES_SOLVED

LP_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
LP_ROOT_DIR = os.path.relpath(os.path.dirname(LP_MODULE_DIR))


class LPath(object):
    @staticmethod
    def root(fname):
        return os.path.join(LP_ROOT_DIR, fname)

    @staticmethod
    def page(fname):
        return os.path.join(LP_ROOT_DIR, 'pages', fname + '.txt')

    @staticmethod
    def data(fname, ext='txt'):
        return os.path.join(LP_ROOT_DIR, 'data', f'{fname}.{ext}')

    @staticmethod
    def db(fname):
        return os.path.join(LP_ROOT_DIR, 'db', fname + '.txt')

    @staticmethod
    def results(fname):
        return os.path.join(LP_ROOT_DIR, 'results', fname)

    @staticmethod
    def tmp(fname, ext='txt'):
        return os.path.join(LP_ROOT_DIR, 'tmp', f'{fname}.{ext}')
