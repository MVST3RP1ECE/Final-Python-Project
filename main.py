import requests
from bs4 import BeautifulSoup
import fake_useragent
import lxml
import time
import json

def GetLinks(text):
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=f"https://hh.ru/search/vacancy?text={text}&area=1&page=1",
        headers={"user-agent": ua.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, "lxml")
    try:
        PageCount = int(soup.find("div", attrs={"class": "pager"}).find_all("span", recursive=False)[-1]
                        .find("a").find("span").text)
    except:
        return

    for page in range(PageCount):
        try:
            data = requests.get(
                url=f"https://hh.ru/search/vacancy?text={text}&area=1&page={page}",
                headers={"user-agent": ua.random}
            )
            if data.status_code != 200:
                continue
            soup = BeautifulSoup(data.content, "lxml")
            for a in soup.find_all("a", attrs={"class" : "serp-item__title"}):
                yield f"{a.attrs['href'].split('?')[0]}"
        except Exception as e:
            print(f"{e}")
        time.sleep(1)

def GetVacancy(link):
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=link,
        headers={"user-agent": ua.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, "lxml")
    try:
        name = soup.find(attrs={"class": "bloko-header-section-1"}).text
    except:
        name = ""
    try:
        salary = (soup.find(attrs={"class": "bloko-header-section-2"}).text.replace("\xa0", "")
                  )
    except:
        salary = ""
    try:
        skills = [skills.text for skills in soup.find(attrs={"class" : "bloko-tag-list"}).find_all(attrs={"class" : "bloko-tag__section_text"})]
    except:
        skills = []
    Vacancy = {
        "name": name,
        "salary": salary,
        "skills": skills,
    }
    return Vacancy

if __name__ == "__main__":
    data = []
    for a in GetLinks("python"):
        data.append(GetVacancy(a))
        time.sleep(1)
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)