const addSelectHours = () => {
	let result = '';
	let i;
	for (i = 4; i < 23; i++) {
		result += `<option id="hour-${i}" value="${i}">${i}:00</option>`;
	}
	return result;
};

const renderSubscriptionData = (subscriptionData) => {
	const subscriptionDiv = document.querySelector('#subscription-div');
	if (subscriptionData['exists']) {
		const time = subscriptionData['time'];
		subscriptionDiv.innerHTML = `
            <span>
                You're subscribed for the daily weather updates at ${time}:00 (Ukrainian time)
                <button type="button" 
                    onclick="removeSubscription(${time})" 
                    class="btn btn-outline-danger btn-sm ms-2">Delete
                </button>
            </span>
        `;
	} else {
		subscriptionDiv.innerHTML = `
            <span>
                Subscribe for daily weather updates:
                <div class="input-group">
                    <select class="form-select" id="select-hour">
                        ${addSelectHours()}
                    </select>

                    <button type="button" 
                        onclick="subscribeForWeatherUpdates()" 
                        class="btn btn-outline-primary btn-sm ms-2">Subscribe
                    </button>
                </div>
            </span>
        `;
	}
};


