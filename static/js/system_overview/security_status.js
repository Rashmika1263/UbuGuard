// Function to fetch JSON data from a given URL
async function fetchData(url) {
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching data:", error);
        return null;
    }
}

// Function to create a div with class name "box" and display key-value pairs
function createBox(data) {
    const boxDiv = document.createElement("div");
    boxDiv.className = "box";

    for (const [key, value] of Object.entries(data)) {
        const heading = document.createElement("h5");
        heading.textContent = key;

        const subBox = document.createElement("div");
        subBox.className = "sub-box";

        if (typeof value === "object") {
            // If the value is an object, recursively create sub-boxes
            const subBoxContent = createBox(value);
            subBox.appendChild(subBoxContent);
        } else {
            // If the value is not an object, create a pre element
            const preElement = document.createElement("pre");
            preElement.textContent = value;
            subBox.appendChild(preElement);
        }

        boxDiv.appendChild(heading);
        boxDiv.appendChild(subBox);
    }

    return boxDiv;
}

async function fetchAndCreate(url) {
    fetchData(url)
        .then((data) => {
            if (data) {
                const resultBox = createBox(data);
                const display = document.getElementById("display")
                display.appendChild(resultBox); // Append the result box to the body or any other container
            } else {
                console.error("Failed to fetch data.");
            }
        })
        .catch((error) => console.error("Error:", error));
}

fetchAndCreate("/system_overview/security_status/?display=network_security");
fetchAndCreate("/system_overview/security_status/?display=application_security_status"); 
fetchAndCreate("/system_overview/security_status/?display=user_access_status"); 
fetchAndCreate("/system_overview/security_status/?display=installed_security_modules"); 