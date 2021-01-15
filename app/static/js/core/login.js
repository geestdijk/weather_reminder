axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
axios.defaults.xsrfCookieName = 'csrftoken';

getError = (errors, prop) => {
	try {
		return errors[prop];
	} catch (err) {
		return '';
	}
};

authUser = function() {
	const email = document.querySelector('#id_email').value;
	const password = document.querySelector('#id_password').value;

	const data = {
		email,
		password
	};
	axios.post('/api/token/', data).then(
		(response) => {
			inMemoryJWT.setToken(response.data);
			const homeUrl = document
				.querySelector('#homeUrl')
				.getAttribute('home-url');
			document.location.href = homeUrl;
		},
		(error) => {
			const errors = error.response.data;
			document.querySelector('#err').innerHTML = getError(
				errors,
				'detail'
			);
		}
	);
};
