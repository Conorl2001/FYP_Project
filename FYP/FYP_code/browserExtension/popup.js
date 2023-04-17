async function getCurrentTab() {
  let [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
  return tab;
}

function runScan() {
  var flask = "http://localhost:5000";
  //send current website to the underlying program
  getCurrentTab().then(tab => {
    var currentTab = tab.url;
    var currentWebsite = {
      url: currentTab
    }
    var currentWebsiteJson = JSON.stringify(currentWebsite);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", flask, true);
    xhr.setRequestHeader("Content-type", "application/json");
    //reply with underlying applications response
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) 
      {
        var verdict = JSON.parse(xhr.responseText);
        if (verdict.result === "green")
        {
          var resultWindow = window.open("safeResult.html", "_blank", "width=200,height=400");
        }
        else if(verdict.result === "orange")
        {
          var resultWindow = window.open("caution.html", "_blank", "width=200,height=400");
        }
        else if(verdict.result === "blue")
        {
          var resultWindow = window.open("yield.html", "_blank", "width=200,height=400");
        }
        else if(verdict.result === "red") {
          var resultWindow = window.open("warning.html", "_blank", "width=200,height=400");
        } 
        else 
        {
          console.log(xhr.responseText);
        }
      }
    };
    console.log("Sending request to Flask server:", currentWebsiteJson);
    xhr.send(currentWebsiteJson);
  });
}

var runButton = document.getElementById("runScan");
runButton.addEventListener("click", runScan);