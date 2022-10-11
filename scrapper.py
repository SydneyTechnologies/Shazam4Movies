from bs4 import BeautifulSoup
import requests


CELEBRITY_URL = "https://starbyface.com/Home/LooksLikeByPhoto"
files = {'imageUploadForm': open("test.JPG",'rb')}
response= requests.post(CELEBRITY_URL, files=files)
soup = BeautifulSoup(response.content, 'html.parser')


if response.status_code == 200:
    male = soup.find(id="male-celebs-result")
    female = soup.find(id="female-celebs-result")
    mCandidate = male.find("div", attrs={"class":"progress-bar"})
    fCandidate = female.find("div", attrs={"class":"progress-bar"})
    mPercentage = mCandidate.text.replace("\r", "").replace("\n", "").replace("%", "")
    fPercentage = fCandidate.text.replace("\r", "").replace("\n", "").replace("%", "")
    print(f"{male.div['name']}:{int(mPercentage)}")
    print(f"{female.div['name']}:{int(fPercentage)}")
