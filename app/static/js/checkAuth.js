const authHttpClient = (url) => {
    const options = {
        headers: {"Accept": 'application/json'},
    };
    const token = inMemoryJWT.getToken();

    if (token) {
        options.headers['Authorization'] = `Bearer ${token}`;
        return axios.get(url, options);
    } else {
        inMemoryJWT.setRefreshTokenEndpoint('http://localhost:8000/api/token/refresh/');
        return inMemoryJWT.getRefreshedToken().then((gotFreshToken) => {
            if (gotFreshToken) {
                options.headers['Authorization'] = `Bearer ${inMemoryJWT.getToken()}`;
            };
            return axios.get(url, options);
        });
    }
};
