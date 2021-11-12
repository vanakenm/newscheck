from bs4 import BeautifulSoup
import requests
import spacy
import gender_guesser.detector as gender

nlp = spacy.load("fr_core_news_sm")
d = gender.Detector()

sources = [{
  "name": "rtbf", 
  "url": "https://www.rtbf.be/info/",
  "finder": "h3"
},
{
  "name": "lesoir",
  "url": "https://www.lesoir.be",
  "finder": "h3"
}, {
  "name": "nouvelobs",
  "url": "https://www.nouvelobs.com/",
  "finder": "h2"
}]

results = []

for(source) in sources:
  url = source["url"]
  name = source["name"]

  r = requests.get(url)
  html = r.text

  soup = BeautifulSoup(html, 'html.parser')
  article_titles = [x.text.strip() for x in soup.find_all(source["finder"])]
  
  for(title) in article_titles:
    doc = nlp(title)
    for word in doc.ents:
      if(word.label_ == "PER"):
        gender = d.get_gender(word.text.split(" ")[0])
        if(gender != "unknown"):
          print(name + ":" + word.text + " - " + gender)
          results.append({"name": word.text, "gender": gender, "source": name})
