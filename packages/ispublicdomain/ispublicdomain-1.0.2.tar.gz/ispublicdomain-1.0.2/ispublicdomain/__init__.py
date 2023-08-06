import tld
from normalizeurl import normalize

def check(domain):

	domain = normalize(domain)
	res = domain.split('.')
	res = res[-1].split('/')
	dom = tld.get_tld(domain, as_object = True)

	if res[0] == dom.tld:
		return True
	else:
		return False
