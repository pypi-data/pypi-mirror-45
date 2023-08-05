import pandas
import numpy
import re


def bin_variable(x: pandas.Series, start, end, width, how, default=None, lower=None, upper=None, errors=None):
	x_binned = x.copy()
	nan_values = numpy.array(x_binned.isna()) | numpy.array((x_binned == errors))

	conditions = pandas.Series([True for _ in range(len(x_binned))])

	if lower is not None:
		x_binned.loc[x_binned < start] = lower
		conditions = conditions.values & (x_binned != lower) & (start <= x_binned)

	if upper is not None:
		x_binned.loc[x_binned > end] = upper
		conditions = conditions & (x_binned != upper) & (x_binned <= end)

	x_binned.loc[conditions] = list(numpy.clip(how(x_binned.loc[conditions]/width)*width, start, end))
	x_binned = numpy.round(x_binned, 8)
	if default is not None:
		x_binned.loc[nan_values] = default

	return x_binned


def multiple_replace(series, replacing_dict, default=None):
	for key, value in replacing_dict.items():
		series = series.replace(value, key)
	if default is not None:
		series = series.map(dict(zip(replacing_dict.keys(), replacing_dict.keys()))).fillna(default)
	return series


def find_regex(regex, value):
	if re.search(regex, value) is not None:
		return True
	else:
		return False
