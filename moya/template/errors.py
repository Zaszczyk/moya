from __future__ import unicode_literals
from ..compat import implements_to_string, text_type


class MoyaRuntimeError(Exception):
    def __init__(self):
        pass


@implements_to_string
class MissingTemplateError(Exception):
    hide_py_traceback = True
    error_type = "Missing Template Error"

    def __init__(self, path, diagnosis=None):
        self.path = path
        self.diagnosis = diagnosis or """The referenced template doesn't exists in the templates filesystem. Run the following to see what templates are installed:\n\n **$ moya fs templates --tree**"""

    def __str__(self):
        return 'Missing template "{}"'.format(self.path)

    __repr__ = __str__


@implements_to_string
class BadTemplateError(MissingTemplateError):

    def __str__(self):
        return 'Unable to load template "%s"' % self.path


@implements_to_string
class RecursiveTemplateError(Exception):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return "Template '{}' has already been used in an extends directive".format(self.path)


@implements_to_string
class TemplateError(Exception):
    def __init__(self, msg, path, lineno, start, end,
                code=None,
                raw_path=None,
                diagnosis=None,
                original=None,
                trace_frames=None):
        self.msg = msg
        self.path = path
        self.lineno = lineno
        self.start = start
        self.end = end
        self._code = code
        self.raw_path = raw_path
        self.diagnosis = diagnosis
        self.original = original
        self.trace_frames = trace_frames or []
        super(TemplateError, self).__init__()

    def __str__(self):
        return self.msg

    def __repr__(self):
        return 'File "%s", line %s: %s' % (self.path, self.lineno, self.msg)

    def get_moya_error(self):
        return 'File "%s", line %s: %s' % (self.path, self.lineno, self.msg)

    def get_moya_frames(self):
        return self.trace_frames[:]


@implements_to_string
class NodeError(Exception):
    def __init__(self, msg, node, lineno, start, end, diagnosis=None):
        self.msg = msg
        self.node = node
        self.lineno = lineno
        self.start = start
        self.end = end
        self.diagnosis = diagnosis

    def __str__(self):
        return self.msg

class UnmatchedComment(NodeError):
    """Begin comments don't manage end comments"""
    pass


class UnknownTag(NodeError):
    pass


class UnmatchedTag(NodeError):
    pass


class TagSyntaxError(NodeError):
    pass


class RecursiveExtends(NodeError):
    pass


class TokenizeError(Exception):
    pass


class UnmatchedComment(TokenizeError):
    def __init__(self, msg, lineno, start, end, diagnosis=None):
        self.msg = msg
        self.lineno = lineno
        self.start = start
        self.end = end
        self.diagnosis = diagnosis

@implements_to_string
class TagError(Exception):
    def __init__(self, msg, node, diagnosis=None):
        self.msg = msg
        self.node = node
        self.diagnosis = diagnosis
        super(TagError, self).__init__("{} {}".format(msg, text_type(node)))

    def __str__(self):
        return self.msg
