from cryptohash import md5

def get(email, size = 250):
	result = md5(email)
	print('https://secure.gravatar.com/avatar/' + result + '?s=' + str(size))