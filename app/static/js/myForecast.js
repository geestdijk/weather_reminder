var forecastDiv;
var cityForecast;

const getUserWeather = (userForecastUrl) => {
	authHttpClient(userForecastUrl, "get")
		.then((response) => {
			createWeatherCards(response.data);
		})
		.catch((error) => {
			console.log(error.response.data);
		});
};

const createWeatherCards = (forecastResponse) => {
	Object.entries(forecastResponse).forEach(([ key, value ]) => {
		const { city } = value;
		forecastDiv = document.querySelector('#cities-forecast');
		forecastDiv.insertAdjacentHTML(
			'beforeend',
			`<div id="${city.name.replace(/\s/g, '')}-div" class="mt-3">
				<h4>${city.name}  <button onclick="removeCityFromUser('${city.name}')" type="button" class="btn btn-outline-danger btn-sm float-end">Remove</button></h4>
				<div class="card-group mt-2" id="forecast-${city.name.replace(/\s/g, '')}">
				</div>
			</div>`
		);
		addFourDaysDailyWeatherCards(city.name, city.forecast.daily);
	});
};

const addFourDaysDailyWeatherCards = (cityName, forecastObject) => {
	Object.entries(
		forecastObject.slice(0, 4)
	).forEach(([ key, dailyForecast ]) => {
		addCard(cityName, dailyForecast);
	});
};

const addCard = (cityName, dailyWeather) => {
	const theDate = new Date(dailyWeather.dt * 1000);
	const day = theDate.toLocaleDateString('en-us', { weekday: 'short' });
	const date = `${theDate.getDate()}/${theDate.getMonth() +
		1}/${theDate.getFullYear()}`;
	cityForecast = document.querySelector(
		`#forecast-${cityName.replace(/\s/g, '')}`
	);
	cityForecast.insertAdjacentHTML(
		'beforeend',
		`<div class="card">
			<h5 class="card-header">${day} ${date}</h5>
			<div class="card-body">
				<img src="http://openweathermap.org/img/wn/${dailyWeather.weather[0]
					.icon}@2x.png">
				<p class="card-text">Day: ${Math.round(dailyWeather.temp.day)} &#8451;</p>
				<p class="card-text">Night: ${Math.round(
					dailyWeather.temp.night
				)} &#8451;</p>
				<p class="card-text">Wind: ${degToCompass(
					dailyWeather.wind_deg
				)} ${Math.round(dailyWeather.wind_speed)} m/s</p>
				<p class="card-text">Weather: ${dailyWeather.weather[0].description}</p>
			</div>
		</div>
    	`
	);
};

const degToCompass = (degrees) => {
	const val = Math.floor(degrees / 22.5 + 0.5);
	const arr = [
		'N',
		'NNE',
		'NE',
		'ENE',
		'E',
		'ESE',
		'SE',
		'SSE',
		'S',
		'SSW',
		'SW',
		'WSW',
		'W',
		'WNW',
		'NW',
		'NNW'
	];
	return arr[val % 16];
};
