"""
Tools for writing a nexus file
"""

import collections

TEMPLATE = """
#NEXUS
%(datablock)s
%(treeblock)s
"""

DATA_TEMPLATE = """
%(comments)s
BEGIN DATA;
    DIMENSIONS NTAX=%(ntax)d NCHAR=%(nchar)d;
    FORMAT DATATYPE=%(datatype)s MISSING=%(missing)s GAP=%(gap)s %(interleave)s SYMBOLS="%(symbols)s";
    %(charblock)s
MATRIX
%(matrix)s
;
END;
"""

TREE_TEMPLATE = """
BEGIN TREES;
%(trees)s
END;
"""


class NexusWriter(object):

    MISSING = '?'
    GAP = '-'
    DATATYPE = 'STANDARD'

    def __init__(self):
        self.comments = []
        self._taxa = None
        self.data = collections.defaultdict(dict)
        self.is_binary = False
        self.trees = []

    def clean(self, s):
        """Removes unsafe characters"""
        _EMPTY = ''
        replacements = {
            ' ': _EMPTY, '\\': _EMPTY, ':': _EMPTY,
            '/': _EMPTY, '?': _EMPTY, '-': _EMPTY,
            '(': '_', ')': _EMPTY,
        }
        for f, t in replacements.items():
            s = s.replace(f, t)
        return s
    
    @property
    def characters(self):
        return self.data.keys()
    
    @property
    def ntrees(self):
        return len(self.trees)
    
    @property
    def taxa(self):
        if self._taxa is None:
            self._taxa = set()
            [self._taxa.update(self.data[c].keys()) for c in self.data]
        return self._taxa
    
    @property
    def symbols(self):
        symbols = set()
        [symbols.update(self.data[c].values()) for c in self.data]
        symbols = [s for s in symbols if s not in ('-', '?')]
        return symbols
    
    def _make_charlabel_block(self):
        """Generates a character label block"""
        out = ["CHARSTATELABELS"]
        for i, char in enumerate(sorted(self.characters), 1):
            out.append("\t\t%d %s," % (i, self.clean(str(char))))
        out[-1] = out[-1].strip(',')  # remove trailing comma
        out.append(";")
        return "\n".join(out)

    def _make_matrix_block(self, interleave):
        """Generates a matrix block"""
        max_taxon_size = max([len(t) for t in self.taxa]) + 3
        
        out = []
        if interleave:
            for c in sorted(self.characters):
                for t in self.taxa:
                    out.append(
                        "%s %s" % (t.ljust(max_taxon_size),
                                   self.data[c].get(t, self.MISSING))
                    )
                out.append("")
        else:
            for t in sorted(self.taxa):
                s = []
                for c in sorted(self.characters):
                    value = self.data[c].get(t, self.MISSING)
                    if len(value) > 1:  # wrap equivocal states in ()'s
                        value = "(%s)" % value
                    s.append(value)
                out.append("%s %s" % (t.ljust(max_taxon_size), ''.join(s)))
        return "\n".join(out)

    def make_treeblock(self):
        return "\n".join(["    %s" % t.lstrip().strip() for t in self.trees])

    def _make_comments(self):
        """Generates a comments block"""
        return "\n".join(["[%s]" % c.ljust(70) for c in self.comments])

    def add_comment(self, comment):
        """Adds a `comment` into the nexus file"""
        self.comments.append(comment)
    
    def add(self, taxon, character, value):
        """Adds a `character` for the given `taxon` and sets it to `value`"""
        assert self.is_binary is False, \
            "Unable to add data to a binarised nexus form"
        value = str(value)
        # have multiple entries
        if taxon in self.data[character]:
            self.data[character][taxon] += value
        else:
            self.data[character][taxon] = value
    
    def remove(self, taxon, character):
        """Removes a `character` for the given `taxon` and sets it to empty"""
        del(self.data[character][taxon])
    
    def remove_taxon(self, taxon):
        """Removes a given `taxon` from the nexus file"""
        for char in self.data:
            del(self.data[char][taxon])
        
    def remove_character(self, character):
        """Removes a given `character` from the nexus file"""
        del(self.data[character])
        
    def write(self, interleave=False, charblock=False):
        """
        Generates a string representation of the nexus
        (basically a wrapper around make_nexus)

        :param interleave: Generate interleaved matrix or not
        :type interleave: Boolean
        :param charblock: Include a characters block or not
        :type charblock: Boolean

        :return: String
        """
        return self.make_nexus(interleave, charblock)

    def _is_valid(self):
        """Checks the nexus is valid to write (i.e. not empty)"""
        valid = False
        if self.data and self.taxa:
            valid = True
        elif self.ntrees:
            valid = True
        return valid

    def make_nexus(self, interleave=False, charblock=False):
        """
        Generates a string representation of the nexus

        :param interleave: Generate interleaved matrix or not
        :type interleave: Boolean
        :param charblock: Include a characters block or not
        :type charblock: Boolean

        :return: String
        """
        
        if not self._is_valid():
            raise ValueError("Nexus has no data!")
        
        if self.data:
            datablock = DATA_TEMPLATE % {
                'ntax': len(self.taxa),
                'nchar': len(self.characters),
                'charblock': self._make_charlabel_block() if charblock else '',
                'matrix': self._make_matrix_block(interleave=interleave),
                'interleave': 'INTERLEAVE' if interleave else '',
                'comments': self._make_comments(),
                'symbols': ''.join(sorted(self.symbols)),
                'missing': self.MISSING,
                'gap': self.GAP,
                'datatype': self.DATATYPE,
            }
        else:
            datablock = ""
        
        treeblock = TREE_TEMPLATE % {'trees': self.make_treeblock()} if self.ntrees else ""
        return TEMPLATE % {'datablock': datablock, 'treeblock': treeblock}

    def write_to_file(self, filename="output.nex", interleave=False,
                      charblock=False):
        """
        Generates a string representation of the nexus
        
        :param filename: Filename to store nexus as
        :type filename: String
        :param interleave: Generate interleaved matrix or not
        :type interleave: Boolean
        :param charblock: Include a characters block or not
        :type charblock: Boolean
        
        :return: None
        """
        nexus = self.make_nexus(interleave, charblock)
        with open(filename, 'w+') as handle:
            handle.write(nexus)

    def write_as_table(self):
        """
        Generates a simple table of the nexus
        """
        out = []
        for t in sorted(self.taxa):
            s = []
            for c in sorted(self.characters):
                value = self.data[c].get(t, self.MISSING)
                if len(value) > 1:  # wrap equivocal states in ()'s
                    value = "(%s)" % value
                s.append(value)
            out.append("%s %s" % (t.ljust(25), ''.join(s)))
        return "\n".join(out)

    def _convert_to_reader(self):
        """
        This is a hack to convert a NexusWriter object to a NexusReader
        instance.
        
        One day I'll refactor this all so Reader and Writer subclass something,
        which will make this unnecessary.
        """
        from .reader import NexusReader
        n = NexusReader()
        out = self.make_nexus(interleave=False, charblock=True)
        n.read_string(out)
        return n
        