def isRedirect(x):

	if str(x).isdigit():
		return x == 300 or x == 301 or x == 302 or x == 303 or x == 305 or x == 307 or x == 308
	else:
		return 'Expected Number'
