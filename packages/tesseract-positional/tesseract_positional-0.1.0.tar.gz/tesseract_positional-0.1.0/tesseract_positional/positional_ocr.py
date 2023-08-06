#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# tesseract_positional/positional_ocr.py
# v.0.1.0
# Developed in 2019 by Travis Kessler <travis.j.kessler@gmail.com>
#
# Contains function for generating a positional text file from an image
#

# Stdlib includes
import re

# 3rd party imports
import pytesseract
try:
    from PIL import Image
except ImportError:
    import Image


# RegEx's for identifying file extensions
_IMG_RE = re.compile(r'\.((jp(e)?g)|(png)|(tif(f)?))$', flags=re.IGNORECASE)
_TXT_RE = re.compile(r'\.txt$', flags=re.IGNORECASE)

# Constant scalars for applying vert/hor spacing based on image dims
_VERT_SPACING_SCALAR = 0.012
_HOR_SPACING_SCALAR = 0.018


class _Word:

    def __init__(self, word, left, top):
        ''' _Word object: houses information about a specific extracted word

        Args:
            word (str): extracted word
            left (int): position of the word's left bound, in reference to
                left side of image
            top (int): position of the word's top bound, in reference to the
                top of the image
        '''

        self.word = word
        self.left = left
        self.top = top


class _Row:

    def __init__(self, top):
        ''' _Row object: houses words within each horizontal line of the image

        Args:
            top (int): position of the row's top bound, in reference to the
                top of the image
        '''

        self.top = top
        self.words = []

    @property
    def row_min(self):
        ''' Minimum allowed value for same-row association; range of 8 below
        row's top bound is allowed
        '''

        return self.top - 8

    @property
    def row_max(self):
        ''' Maximum allowed value for same-row association; range of 8 above
        row's top bound is allowed
        '''

        return self.top + 8

    def add_word(self, word):
        ''' Adds a word to the row, sorts all words by left bound

        Args:
            word (_Word): word to add to row
        '''

        self.words.append(word)
        self.words.sort(key=lambda w: w.left)


def positional_ocr(base_file, output_file=None):
    ''' positional_ocr function: extracts text from supplied image, saves
    positional data to .txt file

    Args:
        base_file (str): image file (e.g. JPG, PNG, TIF)
        output_file (str): optional output file, .txt

    Returns:
        str: string containing extracted positional text
    '''

    # check for correct extensions
    if _IMG_RE.search(base_file) is None:
        raise ValueError('Base file `{}` is not an image'.format(base_file))

    # read image, get dimensions
    image = Image.open(base_file)
    im_width, im_height = image.size

    # extract positional data for each word in image
    data = pytesseract.image_to_data(
        image,
        output_type=pytesseract.Output.DICT
    )

    # create Word objects for each word
    words = [_Word(word, data['left'][idx], data['top'][idx])
             for idx, word in enumerate(data['text'])]

    # construct rows from position coordinates
    rows = []
    for word in words:
        row_upper_bounds = [row.row_max for row in rows]
        row_lower_bounds = [row.row_min for row in rows]
        new_row = True
        for idx, ub in enumerate(row_upper_bounds):
            if word.top < ub and word.top > row_lower_bounds[idx]:
                rows[idx].add_word(word)
                new_row = False
                break
        if new_row:
            rows.append(_Row(word.top))
            rows[-1].add_word(word)

    # convert rows to string
    text = ''
    prev_top = 0
    for row in rows:
        # add vertical spacing between rows
        for _ in range(max(int((row.top - prev_top) /
                       (_VERT_SPACING_SCALAR * im_height)), 1)):
            text += '\n'
        prev_top = row.top

        # add horizontal spacing between words
        left_start = 0
        prev_word_len = 0
        for word in row.words:
            for _ in range(max(int((word.left - left_start - prev_word_len) /
                           (_HOR_SPACING_SCALAR * im_width)), 1)):
                text += ' '
            text += word.word
            left_start = word.left
            prev_word_len = len(word.word)

    # if output file specified, save text
    if output_file is not None:
        if _TXT_RE.search(output_file) is None:
            raise ValueError('Output file `{}` is not .txt'.format(
                output_file
            ))
        with open(output_file, 'w') as out_file:
            out_file.write(text)
        out_file.close()

    # return text
    return text
