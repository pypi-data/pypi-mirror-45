import numpy
import pandas
from sklearn.feature_extraction import FeatureHasher


class Hasher:
	def __init__(self, categoricals: list, n_min_features: int=2, n_attempt_max: int=3, n_attempt_tot_max: int=30, verbose: bool=False):
		self.categoricals = categoricals
		self.hashing_dict = {}
		self.n_min_features = n_min_features
		self.n_attempt_max = n_attempt_max
		self.n_attempt_tot_max = n_attempt_tot_max
		self.fitted = False
		self.verbose = verbose

	def fit(self, df: pandas.DataFrame):
		self.fitted = False

		for variable in self.categoricals:
			if self.verbose:
				print('Fitting', variable)
			self.get_hashing(df, variable)

		self.fitted = True

	def transform(self, data, array_indices=None):
		if not self.fitted:
			raise FitError('Hasher class not fitted')

		is_df = type(data) == pandas.DataFrame
		is_series = type(data) == pandas.Series
		is_dict = type(data) == dict
		is_array = type(data) == numpy.ndarray

		if is_df:
			transformed = data[data.columns.difference(self.categoricals)]
		elif is_series:
			transformed = data[data.index.difference(self.categoricals)]
		elif is_dict:
			transformed = data.copy()
		elif is_array:
			if array_indices is None:
				raise MissingIndicesError('Missing indices for array transformation')
			transformed = numpy.array([])
		else:
			raise TypeError('Type not valid for transformation')

		if is_df or is_series:
			for variable in self.categoricals:
				if self.verbose:
					print('Transforming', variable)
				n_new_columns = len(list(self.hashing_dict[variable].values())[0])
				columns = [variable + '_H' + str(i) for i in range(n_new_columns)]

				if is_series:
					try:
						transformed = transformed.append(pandas.Series(self.hashing_dict[variable][data[variable]], index=columns))
					except KeyError:
						raise HashingError('Value \'{}\' not found in hashing dict for variable \'{}\'.'.format(data[variable], variable))

				else:
					transformed = transformed.join(pandas.DataFrame(list(data[variable].apply(lambda x: self.hashing_dict[variable][x])), index=data.index, columns=columns))

		elif is_dict:
			for variable in self.categoricals:
				if self.verbose:
					print('Transforming', variable)

				n_new_columns = len(list(self.hashing_dict[variable].values())[0])
				columns = [variable + '_H' + str(i) for i in range(n_new_columns)]
				value = transformed.pop(variable)
				try:
					hashing_values = self.hashing_dict[variable][value]
				except KeyError:
					raise HashingError('Value \'{}\' not found in hashing dict for variable \'{}\'.'.format(value, variable))

				transformed.update({columns[i]: float(v) for i, v in enumerate(hashing_values)})

		elif is_array:
			for index in range(len(data)):
				if index in array_indices.keys():
					variable = array_indices[index]
					try:
						transformed = numpy.append(transformed, numpy.array(self.hashing_dict[variable][data[index]]))
					except KeyError:
						raise HashingError('Value \'{}\' not found in hashing dict for variable \'{}\'.'.format(data[index], variable))
				else:
					numpy.append(transformed, data[index])
		else:
			raise TypeError('Type not valid for transformation')

		return transformed

	def fit_transform(self, df: pandas.DataFrame):
		self.fit(df)
		return self.transform(df)

	def get_hashing(self, df: pandas.DataFrame, variable: str):

		n_features = self.n_min_features
		n_attempt = 0
		n_attempt_tot = 0
		lost = -1
		non_trivial = False
		uniques = df.loc[:, variable].unique()
		hashed_matrix = [[]]

		while (lost != 0 or not non_trivial) and n_attempt_tot < self.n_attempt_tot_max:
			non_trivial = False
			feature_hasher = FeatureHasher(input_type='string', n_features=n_features)
			keys_list = list(map(lambda x: str(x) + str(numpy.random.rand())[2:8], uniques))

			hashed_matrix = feature_hasher.fit_transform(keys_list).toarray().astype(int)
			hashed_code = set(map(lambda x: ''.join(x.astype(str)), hashed_matrix))

			lost = len(hashed_code) - len(uniques)

			n_attempt += 1
			n_attempt_tot += 1

			if n_attempt == self.n_attempt_max:
				n_attempt = 0
				n_features += 1

			if min(numpy.var(hashed_matrix, axis=0)) > 0:
				non_trivial = True

		if lost != 0 or not non_trivial:
			raise HashingError('Hashing failed on variable: {}. Lost: {}. Trivial: {}.'.format(variable, lost, not non_trivial))

		else:
			tmp_hashing_dict = dict(zip(uniques, map(list, hashed_matrix)))
			self.hashing_dict.update({variable: tmp_hashing_dict})


class HashingError(Exception):
	""":raises Error when hashing is invalid"""


class FitError(Exception):
	""":raises Error when class Hasher is not fitted"""


class MissingIndicesError(Exception):
	""":raises Error when indices are missing"""
