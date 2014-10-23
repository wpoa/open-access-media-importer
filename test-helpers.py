#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from helpers import make_datestring, filename_from_url, template
from helpers.autovividict import countdict, autovividict

class TestMakeDatestring(unittest.TestCase):
    def test_datestring(self):
        """Test that make_datestring produces output in the right form."""
        a = make_datestring(1, 2, 3)
        self.assertTrue(a == '0001-02-03')
        b = make_datestring(11, 12, 13)
        self.assertTrue(b == '0011-12-13')
        c = make_datestring(111, 12, 13)
        self.assertTrue(c == '0111-12-13')
        d = make_datestring(1111, 12, 13)
        self.assertTrue(d == '1111-12-13')

class TestFilenameFromURL(unittest.TestCase):
    def test_quoting(self):
        """Test that filename_from_url quotes URLs properly."""
        url = 'http://example.org/123#%23'
        filename = filename_from_url(url)
        self.assertTrue(filename == 'http%3A%2F%2Fexample.org%2F123%23%2523')

class TestCountdict(unittest.TestCase):
    def test_addition(self):
        """Test that a countdict serves as neutral element for addition."""
        c = countdict()
        c += 1
        self.assertTrue(c == 1)

    def test_dictionary(self):
        """Test that a countdict serves as a dictionary."""
        c = countdict()
        c['k'] = 'v'
        self.assertTrue('k' in c.keys())
        self.assertTrue('v' in c.values())
        self.assertTrue(('k', 'v') in c.items())

class TestAutovividict(unittest.TestCase):
    def test_autovivication(self):
        """Test that autovividict creates countdict as needed."""
        a = autovividict()
        a['k1'] += 1111
        a['k2']['k2'] += 2222
        self.assertTrue('k1' in a.keys())
        self.assertTrue(1111 in a.values())
        self.assertTrue(('k1', 1111) in a.items())
        self.assertTrue('k2' in a.keys())
        self.assertTrue('k2' in a['k2'].keys())
        self.assertTrue(2222 in a['k2'].values())
        self.assertTrue(('k2', 2222) in a['k2'].items())

class TestMediaWikiTemplate(unittest.TestCase):
    def test_escape(self):
        """Test that template._escape escapes “=” and “|” as needed."""
        a_o = 'abc = 123'
        a_e = template._escape(a_o)
        self.assertTrue(a_e == 'abc {{=}} 123')
        b_o = 'def | ghi'
        b_e = template._escape(b_o)
        self.assertTrue(b_e == 'def {{!}} ghi')

    def test_trim(self):
        """Test that template._trim removes whitespace properly."""
        a0 = "The quick brown fox jumps over the lazy dog."
        a1 = template._trim("The quick brown fox jumps over the lazy dog.")
        self.assertTrue(a0 == a1)
        a2 = template._trim("The quick brown fox jumps over the lazy dog. ")
        self.assertTrue(a0 == a2)
        a3 = template._trim(" The quick brown fox jumps over the lazy dog.")
        self.assertTrue(a0 == a3)
        a4 = template._trim(" The quick brown fox jumps over the lazy dog. ")
        self.assertTrue(a0 == a4)

    def test_capitalize_properly(self):
        """Test that template._capitalize_properly capitalizes properly."""
        for (word, expected_output) in (
            ('a', 'a'),
            ('A', 'A'),
            ('ape', 'ape'),
            ('Ape', 'ape'),
            ('DNA', 'DNA'),
            ('HeLa', 'HeLa')
            ):
            calculated_output = template._capitalize_properly(word)
            self.assertTrue(calculated_output == expected_output)

    def test_postprocess_category(self):
        """Test for proper category postprocessing."""
        for (category, expected_output) in (
            # example categories
            ('blurb (blarb)', 'Blurb'),
            ('blurb, blarbed', 'Blarbed blurb'),
            ('blarb-Based blurb', 'Blarb-based blurb'),
            # real categories taken from <http://commons.wikimedia.org/wiki/File:-Adrenergic-Inhibition-of-Contractility-in-L6-Skeletal-Muscle-Cells-pone.0022304.s001.ogv>
            ('CHO Cells', 'CHO cells'),
            ('Beta-2 Adrenergic Receptors', 'Beta-2 adrenergic receptors'),
            ('Protein Kinases, Cyclic AMP-Dependent', 'Cyclic AMP-dependent protein kinases'),
            ):
            calculated_output = template._postprocess_category(category)
            self.assertTrue(calculated_output == expected_output)

    def test_get_license_template(self):
        for (url, expected_output) in (
            (u'http://creativecommons.org/licenses/by/2.0/',
             '{{cc-by-2.0}}'),
            (u'http://creativecommons.org/licenses/by-sa/2.0/',
             '{{cc-by-sa-2.0}}'),
            (u'http://creativecommons.org/licenses/by/2.5/',
             '{{cc-by-2.5}}'),
            (u'http://creativecommons.org/licenses/by-sa/2.5/',
             '{{cc-by-sa-2.5}}'),
            (u'http://creativecommons.org/licenses/by/3.0/',
             '{{cc-by-3.0}}'),
            (u'http://creativecommons.org/licenses/by-sa/3.0/',
             '{{cc-by-sa-3.0}}'),
            (u'http://creativecommons.org/licenses/by/4.0/',
             '{{cc-by-4.0}}'),
            (u'http://creativecommons.org/licenses/by-sa/4.0/',
             '{{cc-by-sa-4.0}}')
            ):
            calculated_output = template.get_license_template(url)
            self.assertTrue(calculated_output == expected_output)

    def test_make_description(self):
        for (title, caption, expected_output) in (
            ('foo', 'bar', 'foo bar'),
            ('Supplementary Data', 'foo', 'foo'),
            ('Supplementary material', 'bar', 'bar'),
            ('Additional file 1', 'baz', 'baz')
            ):
            calculated_output = template.make_description(title, caption)
            self.assertTrue(calculated_output == expected_output)

if __name__ == '__main__':
    unittest.main()