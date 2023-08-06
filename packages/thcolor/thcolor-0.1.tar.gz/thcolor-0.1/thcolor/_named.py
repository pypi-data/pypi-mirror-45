#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2019 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************
""" Named color reference, parent class. """

__all__ = ["NamedColors"]

_default_named_colors = None

class NamedColors:
	""" Color reference for named colors. """

	def __init__(self):
		pass

	def get(self, name):
		raise KeyError(f"{name}: no such color") from None

	def default():
		global _default_named_colors

		if _default_named_colors is not None:
			return _default_named_colors

		from ._builtin import CSS4NamedColors
		_default_named_colors = CSS4NamedColors()
		return _default_named_colors

# End of file.
