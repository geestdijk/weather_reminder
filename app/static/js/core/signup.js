axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
axios.defaults.xsrfCookieName = 'csrftoken';

getError = (errors, prop) => {
	try {
		return errors[prop][0];
	} catch (err) {
		return '';
	}
};

createUser = function() {
	const email = document.querySelector('#id_email').value;
	const name = document.querySelector('#id_name').value;
	const password = document.querySelector('#id_password1').value;
	const password2 = document.querySelector('#id_password2').value;
	if (password !== password2) {
		document.querySelector('#password_err').innerHTML =
			'Passwords are not the same';
		return false;
	}
	const data = {
		email,
		name,
		password
	};
	axios.post('/api/user/create/', data).then(
		(response) => {
			const loginUrl = document
				.querySelector('#loginUrl')
				.getAttribute('login-url');
			document.location.href = loginUrl;
		},
		(error) => {
			const errors = error.response.data;
			document.querySelector('#email_err').innerHTML = getError(
				errors,
				'email'
			);
			document.querySelector('#name_err').innerHTML = getError(
				errors,
				'name'
			);
			document.querySelector('#password_err').innerHTML = getError(
				errors,
				'password'
			);
		}
	);
};
