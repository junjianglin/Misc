def fit(X, Y):
    """ Fitting the line according the data X and Y
    Args:
	    X: predictor variable
	    Y: reponse variable
    Returns:
	    line(x): A closure to predict reponse given new data x
    """
    import math
    def mean(Xs):
	""" Calculate the mean of Xs """
	return sum(Xs) / len(Xs)

    m_X = mean(X)
    m_Y = mean(Y)

    def std(Xs, m):
	""" Calculate the std of Xs given the mean of Xs, which is m
	Args:
	    Xs: the given vector of data
	    m: mean of Xs
	Returns:
	    std of Xs
	"""
	normalizer = len(Xs) - 1
	return math.sqrt(sum((pow(x - m, 2) for x in Xs)) / normalizer)
	# assert np.round(Series(X).std(), 6) == np.round(std(X, m_X), 6)

    def pearson_r(Xs, Ys):
	""" Calculate the pearson R value given Xs and Ys
	Args:
	    Xs: predictor
	    Ys: reponse variable
	Returns:
	    pearson R value for Xs and Ys
	"""
	sum_xy = 0
	sum_sq_v_x = 0
	sum_sq_v_y = 0

	for (x, y) in zip(Xs, Ys):
		var_x = x - m_X
		var_y = y - m_Y
		sum_xy += var_x * var_y
		sum_sq_v_x += pow(var_x, 2)
		sum_sq_v_y += pow(var_y, 2)
	return sum_xy / math.sqrt(sum_sq_v_x * sum_sq_v_y)
	# assert np.round(Series(X).corr(Series(Y)), 6) == np.round(pearson_r(X, Y), 6)

    r = pearson_r(X, Y)

    b = r * (std(Y, m_Y) / std(X, m_X))
    A = m_Y - b * m_X

    def line(x):
	""" The line to be returned
	"""
	return b * x + A
    return line
