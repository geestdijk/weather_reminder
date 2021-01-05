const inMemoryJWTManager = () => {
	let inMemoryJWT = null;

	const getToken = () => inMemoryJWT;

	const setToken = (token) => {
		inMemoryJWT = token;
		return true;
	};

	const eraseToken = () => {
		inMemoryJWT = null;
		return true;
	};

	return {
		eraseToken,
		getToken,
		setToken
	};
};

export default inMemoryJWTManager();
