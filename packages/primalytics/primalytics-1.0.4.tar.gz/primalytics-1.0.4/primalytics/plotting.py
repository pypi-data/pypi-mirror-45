import pandas
import seaborn
import pydotplus
import numpy

from sklearn.externals.six import StringIO
from IPython.display import Image
from sklearn.tree import export_graphviz
from matplotlib import pyplot as plt
from matplotlib import gridspec


def univariate_plot(df: pandas.DataFrame, x_list: list, y_list: list, ylim: tuple=(None, None), mean_variables: list=None, order=None, hlines: list=None, grid: bool=False):
	"""
	:param df: pandas dataframe to plot
	:param x_list: x variables to plot
	:param y_list: y variables to plot
	:param ylim: y axis limit
	:param mean_variables: variables of which plot the mean
	:param order: sorting for x values
	:param hlines: list of float. plots horizontal lines
	:param grid: show grid
	:return: None
	"""
	plt.rcParams['figure.figsize'] = (18, 10)

	for x in x_list:
		n_uniques = len(df[x].unique())

		ax1 = plt.axes()
		ax1.tick_params('x', rotation=90)

		if order is None:
			order = df[x].value_counts().sort_values(ascending=False).index
		elif isinstance(order, str):
			if order in df.columns:
				order = list(df.pivot_table(index=x, aggfunc={order: 'mean'}).sort_values(order).index)
			else:
				raise ValueError('{} invalid value for data ordering!'.format(order))

		seaborn.countplot(x=x, data=df, ax=ax1, alpha=0.7, order=order)

		ax2 = ax1.twinx()
		if ylim[0] is not None and ylim[1] is not None:
			ax2.set_ylim(ylim)

		color = seaborn.color_palette("Set1", 8)
		color_index = 0

		for y in y_list:
			seaborn.pointplot(x=x, y=y, data=df, ax=ax2, color=color[color_index], order=order)
			color_index += 1

		ax1.tick_params('x', labelsize=15)
		ax1.tick_params('y', labelsize=15)
		ax2.tick_params('y', labelsize=15)

		if hlines is not []:
			if not isinstance(hlines, list):
				hlines = [hlines]
			for hline in hlines:
				plt.hlines(y=hline, xmin=0, xmax=n_uniques, label=str(hline), colors=color[color_index], linestyles='--')
				color_index += 1

		legend = y_list + list(map(str, hlines))

		if mean_variables is not None:
			for mean_variable in mean_variables:
				y_mean = df[mean_variable].mean()
				ax2.plot([y_mean for _ in range(n_uniques)], c=color[color_index])
				color_index += 1
			legend += [mv + '_mean' for mv in mean_variables]

		ax2.legend(legend)

		leg = ax2.get_legend()
		color_index = 0
		for lgd in leg.legendHandles:
			lgd.set_color(color[color_index])
			color_index += 1

		ax2.grid(grid)
		plt.show()


def tree_plot(tree, class_names, feature_names, weighted_colors=None, palette_name='Accent'):
	palette = seaborn.color_palette(palette_name, n_colors=tree.n_classes_)
	colors = numpy.array(list(map(lambda x: 256*numpy.array(x), palette)))

	dot_data = StringIO()
	export_graphviz(
		tree, out_file=dot_data,
		filled=True, rounded=True,
		special_characters=True,
		feature_names=feature_names,
		class_names=class_names)

	graph_string = dot_data.getvalue()

	for leaf_ID, leaf in enumerate(numpy.where(tree.tree_.children_left == -1)[0]):
		graph_string = graph_string.replace('\n{} [label=<'.format(leaf), '\n{} [label=<----- leaf {} -----<br/>'.format(leaf, leaf_ID))

	graph = pydotplus.graph_from_dot_data(graph_string)

	nodes = graph.get_node_list()

	for node in nodes:
		if node.get_label():
			values = numpy.array([int(ii) for ii in node.get_label().split('value = [')[1].split(']')[0].split(',')])

			if weighted_colors is None:
				color_weights = numpy.zeros(tree.n_classes_)
				color_weights[numpy.where(values == max(values))] = 1
			else:
				color_weights = values/sum(values)
				color_weights = numpy.power(color_weights, weighted_colors)/sum(numpy.power(color_weights, weighted_colors))

			color_rgb = numpy.dot(color_weights, colors)
			color_hex = '#%02x%02x%02x' % tuple(color_rgb.astype(int))
			node.set_fillcolor(color_hex)

	return  Image(graph.create_png())


def scatter_hist_plot(df: pandas.DataFrame, x: str, y: str, fsize=(18, 8), width_ratios=(5, 1), height_ratios=(4, 1), hue=None, s=0.1, bins=100, alpha=0.5):
	plt.rcParams['figure.figsize'] = fsize
	gs = gridspec.GridSpec(2, 2, width_ratios=list(width_ratios), height_ratios=list(height_ratios))

	ax0 = plt.subplot(gs[0])
	ax1 = plt.subplot(gs[1])
	ax2 = plt.subplot(gs[2])

	if hue is not None:
		legend = []
		for value in df[hue].value_counts().index.values:
			legend.append(value)
			ax0.scatter(df.loc[df[hue]==value, x], df.loc[df[hue]==value, y], s=s)
			ax1.hist(df.loc[df[hue]==value, y], orientation='horizontal', bins=bins, alpha=alpha)
			ax2.hist(df.loc[df[hue]==value, x], orientation='vertical', bins=bins, alpha=alpha)

		ax0.set(xlabel=x,       ylabel=y)
		ax1.set(xlabel='count', ylabel=y)
		ax2.set(xlabel=x,       ylabel='count')

		ax0.legend(legend, markerscale=6)

	else:
		ax0.scatter(df.loc[:, x], df.loc[:, y], s=s)
		plt.xlabel(x)
		plt.ylabel(y)
		ax1.hist(df.loc[:, y], orientation='horizontal', bins=bins, alpha=alpha)
		ax2.hist(df.loc[:, x], orientation='vertical', bins=bins, alpha=alpha)

	plt.tight_layout()
	plt.show()
