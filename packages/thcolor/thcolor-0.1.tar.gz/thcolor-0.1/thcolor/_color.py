#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2019 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the thcolor project, which is MIT-licensed.
#******************************************************************************
""" HTML/CSS like color parsing, mainly for the `[color]` tag.
	Defines the `get_color()` function which returns an rgba value.
"""

import re as _re
import math as _math

from enum import Enum as _Enum

from ._named import NamedColors as _NamedColors
from ._sys import hls_to_rgb as _hls_to_rgb, hwb_to_rgb as _hwb_to_rgb

__all__ = ["Color"]

# ---
# Color decoding elements.
# ---

_cr = _re.compile(r"""
	rgba?\s*\(
		\s* ((?P<rgb_r>[0-9]{1,3})
			|(?P<rgb_r_per> ([0-9]+\.?|[0-9]*\.[0-9]+)) \s*%) \s* ([,\\s]
		\s* ((?P<rgb_g>[0-9]{1,3})
			|(?P<rgb_g_per> ([0-9]+\.?|[0-9]*\.[0-9]+)) \s*%) \s* ([,\\s]
		\s* ((?P<rgb_b>[0-9]{1,3})
			|(?P<rgb_b_per> ([0-9]+\.?|[0-9]*\.[0-9]+)) \s*%) \s* ([,\\s/]
		\s* ((?P<rgb_a_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<rgb_a_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*
		)?)?)?
	\)|
	rbga?\s*\(
		\s* ((?P<rbg_r>[0-9]{1,3})
			|(?P<rbg_r_per> ([0-9]+\.?|[0-9]*\.[0-9]+)) \s*%) \s* ([,\\s]
		\s* ((?P<rbg_b>[0-9]{1,3})
			|(?P<rbg_b_per> ([0-9]+\.?|[0-9]*\.[0-9]+)) \s*%) \s* ([,\\s]
		\s* ((?P<rbg_g>[0-9]{1,3})
			|(?P<rbg_g_per> ([0-9]+\.?|[0-9]*\.[0-9]+)) \s*%) \s* ([,\\s/]
		\s* ((?P<rbg_a_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<rbg_a_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*
		)?)?)?
	\)|
	brga?\s*\(
		\s* ((?P<brg_b>[0-9]{1,3})
			|(?P<brg_b_per> ([0-9]+\.?|[0-9]*\.[0-9]+)) \s*%) \s* ([,\\s]
		\s* ((?P<brg_r>[0-9]{1,3})
			|(?P<brg_r_per> ([0-9]+\.?|[0-9]*\.[0-9]+)) \s*%) \s* ([,\\s]
		\s* ((?P<brg_g>[0-9]{1,3})
			|(?P<brg_g_per> ([0-9]+\.?|[0-9]*\.[0-9]+)) \s*%) \s* ([,\\s/]
		\s* ((?P<brg_a_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<brg_a_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*
		)?)?)?
	\)|
	bgra?\s*\(
		\s* ((?P<bgr_b>[0-9]{1,3})
			|(?P<bgr_b_per> ([0-9]+\.?|[0-9]*\.[0-9]+)) \s*%) \s* ([,\\s]
		\s* ((?P<bgr_g>[0-9]{1,3})
			|(?P<bgr_g_per> ([0-9]+\.?|[0-9]*\.[0-9]+)) \s*%) \s* ([,\\s]
		\s* ((?P<bgr_r>[0-9]{1,3})
			|(?P<bgr_r_per> ([0-9]+\.?|[0-9]*\.[0-9]+)) \s*%) \s* ([,\\s/]
		\s* ((?P<bgr_a_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<bgr_a_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*
		)?)?)?
	\)|
	grba?\s*\(
		\s* ((?P<grb_g>[0-9]{1,3})
			|(?P<grb_g_per> ([0-9]+\.?|[0-9]*\.[0-9]+)) \s*%) \s* ([,\\s]
		\s* ((?P<grb_r>[0-9]{1,3})
			|(?P<grb_r_per> ([0-9]+\.?|[0-9]*\.[0-9]+)) \s*%) \s* ([,\\s]
		\s* ((?P<grb_b>[0-9]{1,3})
			|(?P<grb_b_per> ([0-9]+\.?|[0-9]*\.[0-9]+)) \s*%) \s* ([,\\s/]
		\s* ((?P<grb_a_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<grb_a_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*
		)?)?)?
	\)|
	gbra?\s*\(
		\s* ((?P<gbr_g>[0-9]{1,3})
			|(?P<gbr_g_per> ([0-9]+\.?|[0-9]*\.[0-9]+)) \s*%) \s* ([,\\s]
		\s* ((?P<gbr_b>[0-9]{1,3})
			|(?P<gbr_b_per> ([0-9]+\.?|[0-9]*\.[0-9]+)) \s*%) \s* ([,\\s]
		\s* ((?P<gbr_r>[0-9]{1,3})
			|(?P<gbr_r_per> ([0-9]+\.?|[0-9]*\.[0-9]+)) \s*%) \s* ([,\\s/]
		\s* ((?P<gbr_a_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<gbr_a_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*
		)?)?)?
	\)|
	lab\s*\(
		\s* (?P<lab_l>-?[0-9]{1,3}) \s* [,\\s]
		\s* (?P<lab_a>-?[0-9]{1,3}) \s* [,\\s]
		\s* (?P<lab_b>-?[0-9]{1,3}) \s* ([,\\s/]
		\s* ((?P<lab_a_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<lab_a_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*
		)?
	\)|
	lch\s*\(
		\s* (?P<lch_l>-?[0-9]{1,3}) \s* [,\\s]
		\s* (?P<lch_ch>-?[0-9]{1,3}) \s* [,\\s]
		\s* (?P<lch_hue>-? ([0-9]+\.?|[0-9]*\.[0-9]+) )
			(?P<lch_agl>deg|grad|rad|turn|) \s* ([,\\s/]
		\s* ((?P<lch_a_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<lch_a_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*
		)?
	\)|
	gray\s*\(
		\s* (?P<gray_l>-?[0-9]{1,3}) \s* ([,\\s/]
		\s* ((?P<gray_a_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<gray_a_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*
		)?
	\)|
	hsla?\s*\(
		\s* (?P<hsl_hue>-? ([0-9]+\.?|[0-9]*\.[0-9]+) )
			(?P<hsl_agl>deg|grad|rad|turn|) \s*[,\\s]
		\s* ((?P<hsl_sat_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<hsl_sat_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*[,\\s]
		\s* ((?P<hsl_lgt_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<hsl_lgt_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*([,\\s/]
		\s* ((?P<hsl_aph_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<hsl_aph_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*
		)?
	\)|
	hlsa?\s*\(
		\s* (?P<hls_hue>-? ([0-9]+\.?|[0-9]*\.[0-9]+) )
			(?P<hls_agl>deg|grad|rad|turn|) \s*[,\\s]
		\s* ((?P<hls_lgt_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<hls_lgt_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*[,\\s]
		\s* ((?P<hls_sat_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<hls_sat_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*([,\\s/]
		\s* ((?P<hls_aph_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<hls_aph_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*)?
	\)|
	hwb\s*\(
		\s* (?P<hwb_hue>-? ([0-9]+\.?|[0-9]*\.[0-9]+) )
			(?P<hwb_agl>deg|grad|rad|turn|) \s*[,\\s]
		\s* ((?P<hwb_wht_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<hwb_wht_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*[,\\s]
		\s* ((?P<hwb_blk_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<hwb_blk_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*([,\\s/]
		\s* ((?P<hwb_aph_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<hwb_aph_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*)?
	\)|
		\# (?P<hex_digits> [0-9a-f]+)
	|
		(?P<legacy_chars> [0-9a-z]+)
""", _re.VERBOSE | _re.I | _re.M)

_rgb = ('rgb', 'rbg', 'brg', 'bgr', 'grb', 'gbr')

# ---
# Formats.
# ---

def _byte(name, value):
	try:
		assert value == int(value)
		assert 0 <= value < 256
	except (AssertionError, TypeError, ValueError):
		raise ValueError(f"{name} should be a byte between 0 and 255") \
			from None

	return value

def _percentage(name, value):
	try:
		assert value == float(value)
		assert 0.0 <= value <= 1.0
	except (AssertionError, TypeError, ValueError):
		raise ValueError(f"{name} should be a proportion between 0 " \
			"and 1.0") from None

	return value

def _hue(name, value):
	raise ValueError(f"{name} is not a valid hue") from None

# ---
# Color class definition.
# ---

class _ColorType(_Enum):
	""" The color type. """

	""" Invalid color. """
	INVALID = 0

	""" RGB/A color. """
	RGB     = 1

	""" HSL/A color. """
	HSL     = 2

	""" HWB/A color. """
	HWB     = 3

class Color:
	""" Represent a color with all of its available formats. """

	# Properties to work with:
	#
	# `_type`: the type as one of the Color.Type constants.
	# `_alpha`: alpha value.
	# `_r`, `_g`, `_b`: rgb components, as bytes.
	# `_hue`: hue for HSL and HWB notations.
	# `_sat`, `_lgt`: saturation and light for HSL.
	# `_wht`, `_blk`: whiteness and blackness for HWB.

	Type = _ColorType

	def __init__(self, *args, **kwargs):
		self._type = Color.Type.INVALID
		self.set(*args, **kwargs)

	def __repr__(self):
		args = (('type', self._type),)
		if   self._type == Color.Type.RGB:
			args += (('red', self._r), ('green', self._g), ('blue', self._b))
		elif self._type == Color.Type.HSL:
			args += (('hue', self._hue), ('saturation', self._sat),
				('lightness', self._lgt))
		elif self._type == Color.Type.HWB:
			args += (('hue', self._hue), ('whiteness', self._wht),
				('blackness', self._blk))

		argtext = ', '.join(f'{key}: {repr(value)}' for key, value in args)
		return f"{self.__class__.__name__}({argtext})"

	# ---
	# Management methods.
	# ---

	def set(self, *args, **kwargs):
		""" Set the color. """

		args = list(args)

		def _decode_varargs(*keys):
			# Check for each key.

			results = ()

			for names, convert_func, *value in keys:
				for name in names:
					if name in kwargs:
						if args:
							raise TypeError(f"{self.__class__.__name__}() " \
								f"got multiple values for argument {name}")

						raw_result = kwargs.pop(name)
						break
				else:
					name = names[0]
					if args:
						raw_result = args.pop(0)
					elif value:
						raw_result = value[0] if len(value) == 1 else value
					else:
						raise TypeError(f"{self.__class__.__name__}() " \
							"missing a required positional argument: " \
							f"{name}")

				result = convert_func(name, raw_result)
				results += (result,)

			# Check for keyword arguments for which keys are not in the set.

			if kwargs:
				raise TypeError(f"{next(iter(kwargs.keys()))} is an invalid " \
					f"keyword argument for type {type}")

			return results

		# ---
		# Main function body.
		# ---

		# Check for the type.

		if args:
			try:
				type = kwargs.pop('type')
			except:
				type = args.pop(0)
			else:
				if isinstance(args[0], Color.Type):
					raise TypeError(f"{self.__class__.__name__}() got " \
						"multiple values for argument 'type'")
		else:
			try:
				type = kwargs.pop('type')
			except:
				type = self._type
				if type == Color.Type.INVALID:
					raise TypeError(f"{self.__class__.__name__}() missing " \
						"required argument: 'type'")

		try:
			type = Color.Type(type)
		except:
			type = Color.Type.RGB

		# Initialize the properties.

		if   type == Color.Type.RGB:
			self._r, self._g, self._b, self._alpha = _decode_varargs(\
				(('r', 'red'),   _byte),
				(('g', 'green'), _byte),
				(('b', 'blue'),  _byte),
				(('a', 'alpha'), _percentage, 1.0))
		elif type == Color.Type.HSL:
			self._hue, self._sat, self._lig, self._alpha = _decode_varargs(\
				(('h', 'hue'),                       _hue),
				(('s', 'sat', 'saturation'),         _percentage),
				(('l', 'lig', 'light', 'lightness'), _percentage),
				(('a', 'alpha'),                     _percentage, 1.0))
		elif type == Color.Type.HWB:
			self._hue, self._wht, self._blk, self._alpha = _decode_varargs(\
				(('h', 'hue'),                _hue),
				(('w', 'white', 'whiteness'), _percentage),
				(('b', 'black', 'blackness'), _percentage),
				(('a', 'alpha'),              _percentage, 1.0))
		else:
			raise ValueError(f"invalid color type: {type}")

		# Once the arguments have been tested to be valid, we can set the
		# type.

		self._type = type

	# ---
	# Properties.
	# ---

	@property
	def alpha(self):
		""" Get the alpha. """

		return self._alpha

	@property
	def a(self):
		""" Alias for the `alpha` property. """

		return self.alpha

	@property
	def red(self):
		""" Get the red component. """

		r, _, _ = self.rgb()
		return r

	@property
	def r(self):
		""" Alias for the `red` property. """

		return self.r

	@property
	def green(self):
		""" Get the green component. """

		_, g, _ = self.rgb()
		return g

	@property
	def g(self):
		""" Alias for the `green` property. """

		return self.green

	@property
	def blue(self):
		""" Get the blue component. """

		_, _, b = self.rgb()
		return b

	@property
	def b(self):
		""" Alias for the `blue` property. """

		return self.blue

	# ---
	# Conversion methods.
	# ---

	def rgb(self):
		""" Get the (red, green, blue) components of the color. """

		if   self._type == Color.Type.RGB:
			return (self._r, self._g, self._b)
		elif self._type == Color.Type.HSL:
			r, g, b = _hls_to_rgb(self._hue, self._lgt, self._sat)
			return (r, g, b)
		elif self._type == Color.Type.HWB:
			r, g, b = _hwb_to_rgb(self._hue, self._wht, self._blk)
			return (r, g, b)

		raise ValueError(f"color type {self._type} doesn't translate to rgb")

	def rgba(self):
		""" Get the (red, green, blue, alpha) components of the color. """

		r, g, b = self.rgb()
		alpha = self._alpha

		return (r, g, b, alpha)

	# ---
	# Static methods for decoding.
	# ---

	def from_str(*args, **kwargs):
		""" Alias for `from_text()`. """

		return Color.from_text(value)

	def from_string(*args, **kwargs):
		""" Alias for `from_text()`. """

		return Color.from_text(value)

	def from_text(value, named = None):
		""" Get a color from a string. """

		if named is None:
			named = _NamedColors.default()
		if not isinstance(named, _NamedColors):
			raise ValueError("named is not a NamedColors instance")

		# Check if is a named color.

		value = value.strip()

		try:
			return named.get(value)
		except:
			pass

		# Initialize the alpha.

		alpha = 1.0

		# Get the match.

		match = _cr.fullmatch(value)
		if not match:
			raise ValueError("invalid color string")

		match = match.groupdict()

		if   match['hex_digits'] or match['legacy_chars']:
			# Imitate the Netscape behaviour. Find more about this here:
			# https://stackoverflow.com/a/8333464
			#
			# I've also extended the thing as I could to introduce more
			# modern syntaxes described on the dedicated MDN page:
			# https://developer.mozilla.org/en-US/docs/Web/CSS/color_value
			#
			# First of all, depending on our source, we will act differently:
			# - if we are using the `hex_digits` source, then we use the modern
			#   behaviour and do the fancy things such as `#ABC -> #AABBCC`
			#   management and possible alpha decoding;
			# - if we are using the `legacy_chars` source, then we sanitize our
			#   input by replacing invalid characters by '0' characters (the
			#   0xFFFF limit is due to how UTF-16 was managed at the time).
			#   We shall also truncate our input to 128 characters.
			#
			# After these sanitization options, we will keep the same method as
			# for legacy color decoding. It should work and be tolerant enough…

			members = 3
			if match['hex_digits']:
				hx = match['hex_digits'].lower()

				# RGB and RGBA (3 and 4 char.) notations.

				if len(hx) in (3, 4):
					hx = hx[0:1] * 2 + hx[1:2] * 2 + hx[2:3] * 2 + hx[3:4] * 2

				# Check if there is transparency or not.

				if len(hx) % 3 != 0 and len(hx) % 4 == 0:
					members = 4

			else: # our source is `legacy_chars`
				hx = match['legacy_chars'].lower()
				hx = ''.join(c if c in '0123456789abcdef' \
					else ('0', '00')[ord(c) > 0xFFFF] for c in hx[:128])[:128]

			# First, calculate some values we're going to need.
			# `iv` is the size of the zone for a member.
			# `sz` is the size of the digits slice to take in that zone
			# (max. 8).
			# `of` is the offset in the zone of the slice to take.

			iv = _math.ceil(len(hx) / members)
			of = iv - 8 if iv > 8 else 0
			sz = iv - of

			# Then isolate the slices using the values calculated above.
			# `gr` will be an array of 3 or 4 digit strings (depending on the
			# number of members).

			gr = list(map(lambda i: hx[i * iv + of:i * iv + iv] \
				.ljust(sz, '0'), range(members)))

			# Check how many digits we can skip at the beginning of each slice.

			pre = min(map(lambda x: len(x) - len(x.lstrip('0')), gr))
			pre = min(pre, sz - 2)

			# Then extract the values.

			it = map(lambda x: int('0' + x[pre:pre + 2], 16), gr)
			if members == 3:
				r, g, b = it
			else:
				r, g, b, alpha = it
				alpha /= 255.0

			return Color(Color.Type.RGB, r, g, b, alpha)
		elif any(match[key + '_r'] or match[key + '_r_per'] for key in _rgb):
			# Extract the values.

			for key in _rgb:
				if not match[key + '_r'] and not match[key + '_r_per']:
					continue

				r  = match[f'{key}_r']
				rp = match[f'{key}_r_per']
				g  = match[f'{key}_g']
				gp = match[f'{key}_g_per']
				b  = match[f'{key}_b']
				bp = match[f'{key}_b_per']
				ap = match[f'{key}_a_per']
				af = match[f'{key}_a_flt']
				break

			r = int(r) if r else int(int(rp) * 255 / 100)
			g = int(g) if g else int(int(gp) * 255 / 100) if gp else 0
			b = int(b) if b else int(int(bp) * 255 / 100) if bp else 0

			if   ap:
				alpha = float(ap) / 100.0
			elif af:
				alpha = float(af)

			return Color(Color.Type.RGB, r, g, b, alpha)
		elif match['hsl_hue'] or match['hls_hue']:
			# Extract the values.

			if match['hsl_hue']:
				hue = float(match['hsl_hue'])
				agl = match['hsl_agl']

				# Saturation.
				if match['hsl_sat_per']:
					sat = float(match['hsl_sat_per']) / 100.0
				else:
					sat = float(match['hsl_sat_flt'])
					if sat > 1.0:
						sat /= 100.0

				# Light.
				if match['hsl_lgt_per']:
					lgt = float(match['hsl_lgt_per']) / 100.0
				else:
					lgt = float(match['hsl_lgt_flt'])
					if lgt > 1.0:
						lgt /= 100.0

				# Alpha value.
				if   match['hsl_aph_per']:
					alpha = float(match['hsl_aph_per']) / 100.0
				elif match['hsl_aph_flt']:
					alpha = float(match['hsl_aph_flt'])
			else:
				hue = float(match['hls_hue'])
				agl = match['hls_agl']

				# Saturation.
				if match['hls_sat_per']:
					sat = float(match['hls_sat_per']) / 100.0
				else:
					sat = float(match['hls_sat_flt'])

				# Light.
				if match['hls_lgt_per']:
					lgt = float(match['hls_lgt_per']) / 100.0
				else:
					lgt = float(match['hls_lgt_flt'])

				# Alpha value.
				if   match['hls_aph_per']:
					alpha = float(match['hls_aph_per']) / 100.0
				elif match['hls_aph_flt']:
					alpha = float(match['hls_aph_flt'])

			# Prepare the angle.
			if   agl == 'grad':
				hue = hue * 400.0
			elif agl == 'rad':
				hue = hue / (2 * _math.pi)
			elif not agl or agl == 'deg':
				hue = hue / 360.0
			hue = hue % 1.0

			if sat > 1 or lgt > 1:
				raise Exception

			return Color(Color.Type.HSL, hue = hue,
				saturation = sat, lightness = lgt)
		elif match['hwb_hue']:
			hue = float(match['hwb_hue'])
			agl = match['hwb_agl']

			# Prepare the angle.
			if   agl == 'grad':
				hue = hue * 400.0
			elif agl == 'rad':
				hue = hue / (2 * _math.pi)
			elif not agl or agl == 'deg':
				hue = hue / 360.0
			hue = hue % 1.0

			# Saturation.
			if match['hwb_wht_per']:
				wht = float(match['hwb_wht_per']) / 100.0
			else:
				wht = float(match['hwb_wht_flt'])

			# Light.
			if match['hwb_blk_per']:
				blk = float(match['hwb_blk_per']) / 100.0
			else:
				blk = float(match['hwb_blk_flt'])

			if wht > 1 or blk > 1:
				raise Exception

			return Color(Color.Type.HWB, hue, wht, blk)

		raise ValueError("unsupported format yet")

# End of file.
