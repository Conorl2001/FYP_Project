from bs4 import BeautifulSoup
from duckduckgo_search import ddg
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import whois
import json
import socket
import ssl
import datetime
import nltkScans
import nltk
import requests
import re
import wordninja

#Parses the html information so it can be used by the program
def pullContent(url):
    content = ''
    if not url.startswith("https://"):
        url = "https://" + url
    try:
        req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(req.content, 'html.parser')
        #style and scripts not required for HTML parsing
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        # Removes blank areas from input
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'\s+([^\s\w]|$)', r'\1', text)
        words = []
        for word in nltk.word_tokenize(text):
            words.extend(wordninja.split(word))
        #filter out non alphabet characters
        words = [word for word in words if word.isalpha()]
        content = ' '.join(words)
        return content
    except Exception as e:
        return None

#More simplistic comparison pull for quicker processing
def comparisonPull(url):
    if not url.startswith("https://"):
        url = "https://" + url
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        soup = BeautifulSoup(html, 'lxml')
        return soup.get_text()
    except Exception as e:
        return None
    
#using the whoIs library gathers whoIs information on the website
def whoIsChecks(website):
    try:
        whoIsInfo = whois.whois(website)
        if whoIsInfo is None:
            return 0
        else:
            whoIsStatus = whoIsInfo.status
            statCheck = checkStatus(whoIsStatus)
            domainName = whoIsInfo.domain_name
            domainCheck = checkDomain(domainName, website)
            registrar = whoIsInfo.registrar
            regCheck = checkRegistrar(registrar)
            whoIsFinding = statCheck + domainCheck + regCheck
            return whoIsFinding
    except Exception as e:
        return 0

#checks if the whoIs information is currently valid
def checkStatus(whoIsStatus):
    if whoIsStatus:
        return 10
    else:
        return 0

#ensures that the whoIs information is for the website we are checking
def checkDomain(whois_domain, website):
    domain_check = False
    if whois_domain == website:
        domain_check = True
        return 5
    elif isinstance(whois_domain, str) and whois_domain.lower() == website.lower():
        domain_check = True
        return 5
    else:
        return 0

#checks against of list of accredited registrars to see if the registrar is accredited to provide whoIs information
def checkRegistrar(whoIsRegistrar):
    try:
        with open('accreditedRegistrars.json', 'r') as f:
            data = json.load(f)
        List = data.get("registrars",None)
        found = False
        for entry in List:
            if whoIsRegistrar in entry:
                found = True
        if found:
            return 10
        else:
            return 0
    except:
        return 0

#grabs the webcert for the website to ensure validity
def sslChecks(websiteURL):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((websiteURL, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=websiteURL) as ssock:
                version = ssock.version()
                verCheck = checkVer(version)
                certInfo = ssock.getpeercert()
                timeCheck = checkTime(certInfo)
                hostCheck = checkHost(websiteURL, certInfo)
                SSLScore = verCheck + timeCheck + hostCheck
                return SSLScore
    except Exception as e:
        return 0
    


#Ensures that the SSL is a safe version as other versions are deemed out of date and unsafe for todays standards
def checkVer(version):
    check = False
    if version == "TLSv1.3":
        check = True
    if version == "TLSv1.2":
        check = True
    if check:
        return 10
    else:
        return 0

#ensures that the ssl cert has not fallen out of date
def checkTime(certInfo):
    notBefore = datetime.datetime.strptime(certInfo['notBefore'], '%b %d %H:%M:%S %Y %Z')
    notAfter = datetime.datetime.strptime(certInfo['notAfter'], '%b %d %H:%M:%S %Y %Z')
    time = datetime.datetime.utcnow()
    if notBefore <= time <= notAfter:
        return 10
    else:
        return 0
        

#ensures the website is associated with the web cert
def checkHost(hostname, certInfo):
    check = False
    for entry in certInfo['subject']:
        if entry[0][1].lower() == hostname.lower():
            check = True
    for entry in certInfo['subjectAltName']:
        if entry[1].lower() == hostname.lower():
            check = True
    if check:
        return 5
    else:
        return 0

checkedDomains = set()

def checkNER(url):
    try:
        checkedDomains.clear()
        contentNER = pullContent(url)
        NERs = nltkScans.NER(url, contentNER)
        contentComp = comparisonPull(url)
        found = False
        if NERs:
            for org in NERs:
                results = ddg(org, safesearch="moderate", max_results=3)
                for result in results:
                    if isinstance(result, dict) and 'href' in result:
                        ddgWebsiteLink = result['href']
                        parsedURL = urlparse(ddgWebsiteLink)
                        domain = parsedURL.netloc
                        if domain in checkedDomains:
                            continue
                        checkedDomains.add(domain)
                        ddgWebsiteContent = comparisonPull(domain)
                        if ddgWebsiteContent is not None:
                            similarityPercent = nltkScans.similarityCheck(contentComp, ddgWebsiteContent)
                            if similarityPercent >= 95:
                                found = True
                                return 15
        return 0
    except:
        return 0
    
def imageChecking(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.content, 'html.parser')
        images = soup.find_all('img')
        found = False

        for image in images:
            src = image.get('src')
            try:
                results = ddg(src, safesearch="moderate", max_results=3)
                for result in results:
                    if result['url'] != url:
                        found = True
            except Exception as e:
                continue
        if found:
            return 0
        else:
            return 10
    except Exception as e:
        return 0