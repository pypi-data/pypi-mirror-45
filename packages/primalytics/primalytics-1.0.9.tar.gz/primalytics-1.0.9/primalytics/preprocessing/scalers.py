import numpy
import pandas


class Scaler:
	def __init__(self, scaler):
		self.__scaler = scaler
		self.__fitted = False
		self.__variables = None

	def fit(self, df: pandas.DataFrame, variables):
		self.__variables = variables
		self.__scaler.fit(df[self.__variables])
		self.__fitted = True

	def transform(self, df):
		if self.__fitted:
			original_variables = list(df.columns)
			other_variables = list(df.columns.difference(self.__variables))
			transformed = self.__scaler.transform(df[self.__variables])

			transformed = df[other_variables].join(transformed)
		else:
			raise Exception('Scaler not fitted')

		return transformed[original_variables]

	def fit_transform(self, df, variables):
		self.fit(df, variables)
		return self.transform(df)


class MultiDimStandardScaler:
	def __init__(self):
		self._mean = None
		self._var = None
		self._std = None
		self.__fitted = None

	def fit(self, df):
		if isinstance(df, pandas.DataFrame):
			data = df.values
		else:
			data = df.copy()

		self._mean = numpy.mean(data, axis=0)
		self._var = numpy.var(data, axis=0)
		self._std = numpy.sqrt(self._var)
		self.__fitted = True

	def transform(self, df):
		if self.__fitted:
			sample_len = len(df)
			scaled = df - numpy.array([self._mean for _ in range(sample_len)])
			scaled = scaled / numpy.array([self._std for _ in range(sample_len)])
		else:
			raise Exception('Scaler not fitted.')

		return scaled

	def fit_transform(self, df):
		self.fit(df)
		return self.transform(df)
