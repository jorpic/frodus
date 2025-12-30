import unittest
import parsel
from parser import x, ParseErr

sel = parsel.Selector(text='''
<body>
    <none></none>
    <only>
        <p>
            <a href="./one">one</a>
            hello, <b>world!</b>
        </p>
    </only>
    <many>
        <p>
            <a href="./one">one</a>
            hello, <b>beautiful</b> world!
        </p>
        <p>
            <a href="./two">two</a>
            bye, <b>cruel</b> world!
        </p>
    </many>
</body>
''')

# TODO: check strings on attrs

class TestParser(unittest.TestCase):

    ## Node

    def test_maybe_node_with_default(self):
        self.assertEqual(len(x(sel, '!n//none/p')), 0)
        self.assertEqual(len(x(sel, '!n//only/p')), 1)
        with self.assertRaises(ParseErr):
            x(sel, '!n//many/p')

    def test_maybe_node(self):
        self.assertEqual(x(sel, '?n//none/p', '<any>'), None)
        self.assertEqual(len(x(sel, '?n//only/p')), 1)
        with self.assertRaises(ParseErr):
            x(sel, '?n//many/p')

    def test_some_node(self):
        with self.assertRaises(ParseErr):
            x(sel, '+n//none/p')
        self.assertEqual(len(x(sel, '+n//only/p')), 1)
        self.assertEqual(len(x(sel, '+n//many/p')), 2)

    def test_any_node(self):
        self.assertEqual(len(x(sel, '*n//none/p')), 0)
        self.assertEqual(len(x(sel, '*n//only/p')), 1)
        self.assertEqual(len(x(sel, '*n//many/p')), 2)

    ## String with href
    ## String with text? == get/getall

    def test_maybe_string_with_default(self):
        self.assertEqual(x(sel, '!s//none//a/@href'), '')
        self.assertEqual(x(sel, '!s//only//a/@href'), './one')
        with self.assertRaises(ParseErr):
            x(sel, '!s//many//a/@href')

    def test_maybe_string(self):
        self.assertEqual(x(sel, '?s//none//a/@href'), None)
        self.assertEqual(x(sel, '?s//only//a/@href'), './one')
        with self.assertRaises(ParseErr):
            x(sel, '?s//many//a/@href')

    def test_some_string(self):
        with self.assertRaises(ParseErr):
            x(sel, '+s//none//a/@href')
        self.assertEqual(x(sel, '+s//only//a/@href'), ['./one'])
        self.assertEqual(x(sel, '+s//many//a/@href'), ['./one', './two'])

    def test_any_string(self):
        self.assertEqual(x(sel, '*s//none//a/@href'), [])
        self.assertEqual(x(sel, '*s//only//a/@href'), ['./one'])
        self.assertEqual(x(sel, '*s//many//a/@href'), ['./one', './two'])

    ## Text

    def test_maybe_text_with_default(self):
        self.assertEqual(x(sel, '!t//none/p'), '')
        self.assertEqual(x(sel, '!t//only/p'), 'one hello, world!')
        with self.assertRaises(ParseErr):
            x(sel, '!t//many/p')

    def test_maybe_text(self):
        self.assertEqual(x(sel, '?t//none/p'), None)
        self.assertEqual(x(sel, '?t//only/p'), 'one hello, world!')
        with self.assertRaises(ParseErr):
            x(sel, '?t//many/p')

    def test_some_text(self):
        with self.assertRaises(ParseErr):
            x(sel, '+t//none/p')
        self.assertEqual(x(sel, '+t//only/p'), ['one hello, world!'])
        self.assertEqual(x(sel, '+t//many/p'), [
            'one hello, beautiful world!',
            'two bye, cruel world!'])

    def test_any_text(self):
        self.assertEqual(x(sel, '*t//none/p'), [])
        self.assertEqual(x(sel, '*t//only/p'), ['one hello, world!'])
        self.assertEqual(x(sel, '*t//many/p'), [
            'one hello, beautiful world!',
            'two bye, cruel world!'])

    ## Seq

    def test_sequence_from_none(self):
        self.assertEqual(x(sel, '!n//none/p', '0n.'), [])
        self.assertEqual(x(sel, '?n//none/p', '1n.'), None)
        self.assertEqual(x(sel, '*n//none/p', '1n.'), [])

#           0           1           2
# !n    [], cont        res         FAIL
# ?n    None, stop      res         FAIL
# +n        FAIL        res         res
# *n        res         res         res

# !s        ""      getall, join    FAIL
# ?s       None     getall, join
# +s       FAIL    [getall, join]   --//--
# +s  [getall, join]   --//--       --//--

# !t.//div
#           ""     ' '.join(//text) FAIL
# ?t.//div
#          None    ' '.join(//text) FAIL
# +t.//div   => array of texts
#          FAIL  [' '.join(x.//text() for x in res]
# *t.//div   => array of texts
#            [' '.join(x.//text() for x in res]

# !s.//a/@href
#           ""      getall,join      FAIL
# ?s.//a/@href
#          None     getall, join     FAIL


if __name__ == '__main__':
    unittest.main()
