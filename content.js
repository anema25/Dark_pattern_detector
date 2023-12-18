// content.js
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === 'darkPatternDetection') {
    const elements = scrape();
    const filteredElements = elements.map(element => element.innerText.trim().replace(/\t/g, " "));

    // Post to the Streamlit app
    fetch("http://127.0.0.1:8501/detect_dark_patterns", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tokens: filteredElements }),
    })
      .then((resp) => resp.json())
      .then((data) => {
        data = data.replace(/'/g, '"');
        const json = JSON.parse(data);

        let dpCount = 0;
        let elementIndex = 0;

        for (let i = 0; i < elements.length; i++) {
          const text = elements[i].innerText.trim().replace(/\t/g, " ");
          if (text.length == 0) {
            continue;
          }

          if (json.result[i] !== "Not Dark") {
            highlight(elements[elementIndex], json.result[i]);
            dpCount++;
          }
          elementIndex++;
        }

        // Store the number of dark patterns
        const g = document.createElement("div");
        g.id = "insite_count";
        g.value = dpCount;
        g.style.opacity = 0;
        g.style.position = "fixed";
        document.body.appendChild(g);
        sendDarkPatterns(g.value);
      })
      .catch((error) => {
        console.error(error);
      });
  }
});

function scrape() {
  const elements = Array.from(document.body.getElementsByTagName('*'));
  return elements.filter(element => element.innerText.trim().length > 0);
}

function highlight(element, type) {
  element.classList.add("insite-highlight");

  const body = document.createElement("span");
  body.classList.add("insite-highlight-body");

  // Header
  const header = document.createElement("div");
  header.classList.add("modal-header");
  const headerText = document.createElement("h1");
  headerText.innerHTML = type + " Pattern";
  header.appendChild(headerText);
  body.appendChild(header);

  // Content
  const content = document.createElement("div");
  content.classList.add("modal-content");
  content.innerHTML = descriptions[type];
  body.appendChild(content);

  element.appendChild(body);
}

function sendDarkPatterns(number) {
  chrome.runtime.sendMessage({
    message: "update_current_count",
    count: number,
  });
}

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.message === "analyze_site") {
    scrape();
  } else if (request.message === "popup_open") {
    const element = document.getElementById("insite_count");
    if (element) {
      sendDarkPatterns(element.value);
    }
  }
});
