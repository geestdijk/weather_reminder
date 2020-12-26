axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
axios.defaults.xsrfCookieName = 'csrftoken';

createUser = function() {
	const email = document.querySelector('#id_email').value;
	const name = document.querySelector('#id_name').value;
	const password = document.querySelector('#id_password1').value;
	const password2 = document.querySelector('#id_password2').value;
	if (password !== password2) {
		document.querySelector('#password_error').innerHTML =
			'Passwords are not the same';
		return false;
	}
	const params = {
		email,
		name,
		password
	};

	console.log(document.cookie);
	axios
		.post('/api/user/create/', params)
		.then(function(response) {
			console.log(response);
		})
		.catch(function(error) {
			console.log(error);
		});
};
