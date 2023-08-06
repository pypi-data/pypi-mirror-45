# this module provides forward-compatibility for Python 2.6 and 2.7
#  features on Python 2.5

try:
	import builtins
except ImportError:
	import builtins as builtins

# next statement
try:
	next = next
except NameError:
	class __NotSupplied(object): pass
	def next(iterable, default=__NotSupplied):
		try:
			return iterable.__next__()
		except StopIteration:
			if default is __NotSupplied:
				raise
			return default

# namedtuple
try:
	from collections import namedtuple
except ImportError:
	from .namedtuple_backport import namedtuple

# enumerate with start param
try:
	enumerate('abc', 1)
	enumerate = enumerate
except TypeError:
	def enumerate(seq, start=0):
		for index, item in builtins.enumerate(seq):
			yield index + start, item
