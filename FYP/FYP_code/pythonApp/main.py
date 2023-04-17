from urllib.parse import urlparse
import time
import nltkScans
import webScans

def runCore(urlPassed, progress):
    parsedURL = urlparse(urlPassed)
    domain = parsedURL.netloc
    webContent = webScans.pullContent(domain)

    # Scanning website metadata
    whoIsScan = webScans.whoIsChecks(urlPassed)
    whoIsProgress = 0
    while whoIsProgress <= 25:
        progress.step(1)
        time.sleep(0.01)
        progress.update()
        whoIsProgress += 1

    sslScan = webScans.sslChecks(domain)
    sslProgress = 0
    while sslProgress <= 25:
        progress.step(1)
        time.sleep(0.01)
        progress.update()
        sslProgress += 1

    # NLTK scanning
    grammerChecker = nltkScans.incorrectWordCount(webContent)
    grammerProgress = 0
    while grammerProgress <= 25:
        progress.step(1)
        time.sleep(0.01)
        progress.update()
        grammerProgress += 1

    otherSitesCheck = webScans.checkNER(domain)
    sitesProgress = 0
    while sitesProgress <= 15:
        progress.step(1)
        time.sleep(0.01)
        progress.update()
        sitesProgress += 1

    imageCheck = webScans.imageChecking(domain)
    imageProgress = 0
    while imageProgress <= 10:
        progress.step(1)
        time.sleep(0.01)
        progress.update()
        imageProgress += 1
    legitScore = whoIsScan + sslScan + grammerChecker + otherSitesCheck + imageCheck
    progress['value'] = 100
    progress.update()

    if legitScore > 90:
        return "green"
    elif 75 <= legitScore <= 90:
        return "orange"
    elif 40 <= legitScore <= 75:
        return "blue"
    elif legitScore < 40:
        return "red"
    else:
        return "ERROR"