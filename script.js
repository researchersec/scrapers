document.addEventListener('DOMContentLoaded', function () {
    fetchNewsData();
    fetchJobsData();
    fetchWeatherData();
    fetchOffersData();
});

function fetchNewsData() {
    axios.get('news.json')
        .then(response => {
            displayNewsItems(response.data);
        })
        .catch(error => {
            console.error('Error fetching news data:', error);
        });
}

function fetchJobsData() {
    axios.get('jobs.json')
        .then(response => {
            displayJobItems(response.data);
        })
        .catch(error => {
            console.error('Error fetching jobs data:', error);
        });
}

function fetchWeatherData() {
    axios.get('weather.json')
        .then(response => {
            displayWeatherItems(response.data);
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
        });
}

function fetchOffersData() {
    axios.get('tilbud.json')
        .then(response => {
            displayOfferItems(response.data);
        })
        .catch(error => {
            console.error('Error fetching offers data:', error);
        });
}

function displayNewsItems(newsItems) {
    const newsContainer = document.getElementById('news-container');
    // Sort news by date, newest first
    newsItems.sort((a, b) => new Date(b.published) - new Date(a.published));
    newsItems.forEach(item => {
        const newsCard = createNewsCard(item);
        newsContainer.appendChild(newsCard);
    });
}

function displayJobItems(jobItems) {
    const jobsContainer = document.getElementById('jobs-container');
    // Sort jobs by date, newest first
    jobItems.sort((a, b) => new Date(b.pub_date) - new Date(a.pub_date));
    jobItems.forEach(item => {
        const jobCard = createJobCard(item);
        jobsContainer.appendChild(jobCard);
    });
}

function displayWeatherItems(weatherItems) {
    const weatherContainer = document.getElementById('weather-container');
    weatherItems.forEach(item => {
        const weatherCard = createWeatherCard(item);
        weatherContainer.appendChild(weatherCard);
    });
}

function displayOfferItems(offerItems) {
    const offersContainer = document.getElementById('offers-container');
    offerItems.forEach(item => {
        const offerCard = createOfferCard(item);
        offersContainer.appendChild(offerCard);
    });
}

function createNewsCard(item) {
    const col = document.createElement('div');
    col.className = 'col-12 col-md-6 col-lg-4 mb-4';

    const card = document.createElement('div');
    card.className = 'card text-white bg-dark h-100';

    const cardBody = document.createElement('div');
    cardBody.className = 'card-body';

    const cardTitle = document.createElement('h5');
    cardTitle.className = 'card-title';
    cardTitle.textContent = item.title;

    const cardText = document.createElement('p');
    cardText.className = 'card-text';
    cardText.textContent = item.description;

    const cardLink = document.createElement('a');
    cardLink.className = 'btn btn-primary';
    cardLink.href = item.link;
    cardLink.textContent = 'Read more';

    const cardFooter = document.createElement('div');
    cardFooter.className = 'card-footer';
    cardFooter.innerHTML = `<small class="text-muted">Published: ${item.published}</small><br><small class="text-muted">Category: ${item.category}</small>`;

    cardBody.appendChild(cardTitle);
    cardBody.appendChild(cardText);
    cardBody.appendChild(cardLink);

    card.appendChild(cardBody);
    card.appendChild(cardFooter);

    col.appendChild(card);

    return col;
}

function createJobCard(item) {
    const col = document.createElement('div');
    col.className = 'col-12 col-md-6 col-lg-4 mb-4';

    const card = document.createElement('div');
    card.className = 'card text-white bg-dark h-100';

    const cardBody = document.createElement('div');
    cardBody.className = 'card-body';

    const cardTitle = document.createElement('h5');
    cardTitle.className = 'card-title';
    cardTitle.textContent = item.title;

    const cardText = document.createElement('p');
    cardText.className = 'card-text';
    cardText.innerHTML = `Company: ${item.company}<br>Location: ${item.location}`;

    const cardLink = document.createElement('a');
    cardLink.className = 'btn btn-primary';
    cardLink.href = item.job_URL;
    cardLink.textContent = 'View job';

    const cardFooter = document.createElement('div');
    cardFooter.className = 'card-footer';
    cardFooter.innerHTML = `<small class="text-muted">Posted: ${item.pub_date}</small><br><small class="text-muted">Category: ${item.category}</small>`;

    cardBody.appendChild(cardTitle);
    cardBody.appendChild(cardText);
    cardBody.appendChild(cardLink);

    card.appendChild(cardBody);
    card.appendChild(cardFooter);

    col.appendChild(card);

    return col;
}

function createWeatherCard(item) {
    const col = document.createElement('div');
    col.className = 'col-12 col-md-6 col-lg-4 mb-4';

    const card = document.createElement('div');
    card.className = 'card text-white bg-dark h-100';

    const cardBody = document.createElement('div');
    cardBody.className = 'card-body';

    const cardTitle = document.createElement('h5');
    cardTitle.className = 'card-title';
    cardTitle.textContent = item.location;

    const cardText = document.createElement('p');
    cardText.className = 'card-text';
    cardText.innerHTML = `Temperature: ${item.temperature}°C<br>Condition: ${item.condition}`;

    cardBody.appendChild(cardTitle);
    cardBody.appendChild(cardText);

    card.appendChild(cardBody);

    col.appendChild(card);

    return col;
}

function createOfferCard(item) {
    const col = document.createElement('div');
    col.className = 'col-12 col-md-6 col-lg-4 mb-4';

    const card = document.createElement('div');
    card.className = 'card text-white bg-dark h-100';

    const cardBody = document.createElement('div');
    cardBody.className = 'card-body';

    const cardTitle = document.createElement('h5');
    cardTitle.className = 'card-title';
    cardTitle.textContent = item.title;

    const cardText = document.createElement('p');
    cardText.className = 'card-text';
    cardText.innerHTML = `Price: ${item.price} ${item.currency}<br>Valid from: ${item.valid_from}<br>Valid until: ${item.valid_until}`;

    const cardLink = document.createElement('a');
    cardLink.className = 'btn btn-primary';
    cardLink.href = item.link;
    cardLink.textContent = 'See offer';

    cardBody.appendChild(cardTitle);
    cardBody.appendChild(cardText);
    cardBody.appendChild(cardLink);

    card.appendChild(cardBody);

    col.appendChild(card);

    return col;
}
