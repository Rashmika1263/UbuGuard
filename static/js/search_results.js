// search_script.js
document.addEventListener('DOMContentLoaded', function () {
    const searchBox = document.getElementById('search-box');
    const searchPopup = document.getElementById('search-popup');
    const overlay = document.querySelector('.overlay');

    searchBox.addEventListener('focus', function () {
        // Display "Start typing" message when the search input is focused
        searchPopup.innerHTML = `<p class="search">Start typing...</p>`
    });

    searchBox.addEventListener('input', function () {
        const query = searchBox.value.trim();

        // Make a request to the search view
        fetch(`/ubugaurd_app/search/?query=${query}`)
            .then(response => response.json())
            .then(data => {
                // Handle the response data
                displayResults(data);
            })
            .catch(error => console.error('Error:', error));
    });

    function displayResults(results) {
        // Clear previous results
        searchPopup.innerHTML = '';

        // Check if there are any results
        if (results.length === 0) {
            searchPopup.innerHTML = `<p class="search">No results found.</p>`;
            return;
        }

        // Create a list to display results
        const resultList = document.createElement('ul');

        // Limit the results to a maximum of 5
        const limitedResults = results.slice(0, 5);

        // Iterate over results and create list items
        limitedResults.forEach(result => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<a href="${result.url}">${result.name}</a>`;
            resultList.appendChild(listItem);
        });

        // Append the list to the search popup
        searchPopup.appendChild(resultList);

        // Show the overlay and search popup
        overlay.style.display = 'block';
        searchPopup.style.display = 'block';
    }

    // Close the search popup when the overlay is clicked
    overlay.addEventListener('click', function () {
        overlay.style.display = 'none';
        searchPopup.style.display = 'none';
    });

    // Make the entire area clickable
    searchPopup.addEventListener('click', function (event) {
        if (event.target.tagName === 'A') {
            window.location.href = event.target.href;
        }
    });
});
