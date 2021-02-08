const authHttpClient = (url, method) => {
	const options = {
		headers: { Accept: 'application/json' }
	};
	const token = inMemoryJWT.getToken();

	if (token) {
		options.headers['Authorization'] = `Bearer ${token}`;
		if (method === 'get') {
			return axios.get(url, options);
		} else if (method === 'post') {
			return axios.post(url, {}, options);
		} else if (method === 'delete') {
			return axios.delete(url, options);
		}
	} else {
		inMemoryJWT.setRefreshTokenEndpoint(
			'http://localhost:8000/api/token/refresh/'
		);
		return inMemoryJWT.getRefreshedToken().then((gotFreshToken) => {
			if (gotFreshToken) {
				options.headers[
					'Authorization'
				] = `Bearer ${inMemoryJWT.getToken()}`;
			}
			if (method === 'get') {
				return axios.get(url, options);
			} else if (method === 'post') {
				return axios.post(url, {}, options);
			} else if (method === 'delete') {
				return axios.delete(url, options);
			}
		});
	}
};
