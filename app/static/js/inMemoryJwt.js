const inMemoryJWTManager = () => {
	let inMemoryJWT = null;
	let refreshEndpoint = '/api/token/refresh/';
	let refreshTimeoutId;

	const setRefreshTokenEndpoint = (endpoint) => (refreshEndpoint = endpoint);

	const refreshToken = (delay) => {
		refreshTimeoutId = window.setTimeout(
			getRefreshedToken,
			delay * 1000 - 5000
		);
	};

	const abortRefreshToken = () => {
		if (refreshTimeoutId) {
			window.clearTimeout(refreshTimeoutId);
		}
	};

	const getRefreshedToken = () => {
		return axios
			.post(refreshEndpoint, {}, { withCredentials: true })
			.then((response) => {
				if (response.status != 200) {
					eraseToken();
					global.console.log(
						'Failed to renew jwt from the refresh token'
					);
					return { accessToken: null };
				}
				return response.data;
			})
			.then(({ accessToken, tokenExpire }) => {
				if (accessToken) {
					setToken(accessToken, tokenExpire);
					return true;
				}
				return false;
			});
	};

	const getToken = () => inMemoryJWT;

	const setToken = (token, delay) => {
		inMemoryJWT = token;
		refreshToken(delay);
		return true;
	};

	const eraseToken = () => {
		inMemoryJWT = null;
		abortRefreshToken();
		return true;
	};

	return {
		eraseToken,
		getToken,
		setToken,
		getRefreshedToken,
		setRefreshTokenEndpoint
	};
};

inMemoryJWT = inMemoryJWTManager();
