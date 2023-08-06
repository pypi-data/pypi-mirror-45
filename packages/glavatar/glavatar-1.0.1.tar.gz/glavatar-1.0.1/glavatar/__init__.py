import gitlab as user

def get(username):
	res = user.get(username)

	result = {}
	result['avatar_url'] = res['avatar_url']

	return (result['avatar_url'])
