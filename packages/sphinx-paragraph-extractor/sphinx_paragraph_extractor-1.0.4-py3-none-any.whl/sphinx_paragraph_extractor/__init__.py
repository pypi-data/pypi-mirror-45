#!/usr/bin/env python3

import re
import sphinx
from docutils import nodes

_VERSION = '1.0.3'

_PATTERN_SPACES = re.compile('[\s]+')


def setup(app):
    app.add_builder(Builder)

    return {
        'version': _VERSION,
    }


class Builder(sphinx.builders.Builder):
    name = 'paragraph-extractor'

    def get_target_uri(self, docname, typ=None):
        return '{}.txt'.format(docname)

    def get_outdated_docs(self):
        return ''

    def prepare_writing(self, docnames):
        pass

    def write_doc(self, docname, doctree):
        from pathlib import Path

        name_output = self.get_target_uri(docname)
        path_dest = Path(self.outdir)
        path_output = Path(self.outdir).joinpath(name_output)
        path_output.parent.mkdir(parents=True, exist_ok=True)

        with path_output.open('w') as f:
            visitor = DocumentVisitor(doctree.document, f)
            doctree.walk(visitor)


class DocumentVisitor(nodes.NodeVisitor):
    def __init__(self, document, io):
        super(DocumentVisitor, self).__init__(document)

        self.__io = io

    def dispatch_visit(self, node):
        name_node = node.__class__.__name__
        if name_node != 'paragraph':
            raise nodes.SkipDeparture()

        return super(DocumentVisitor, self).dispatch_visit(node)

    def visit_paragraph(self, node):
        paragraph_visitor = ParagraphVisitor(self.document, self.__io)
        node.walk(paragraph_visitor)
        self.__io.write('\n')

    def unknown_visit(self, node):
        raise nodes.SkipNode()


class ParagraphVisitor(nodes.NodeVisitor):
    def __init__(self, document, io):
        super(ParagraphVisitor, self).__init__(document)

        self.__io = io

    def visit_Text(self, node):
        text = re.sub(_PATTERN_SPACES, ' ', node.astext())
        self.__io.write(text)

    def unknown_visit(self, node):
        raise nodes.SkipDeparture()
