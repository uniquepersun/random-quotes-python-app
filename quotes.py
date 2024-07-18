from datetime import date, timedelta
import random
import requests
from bs4 import BeautifulSoup
import re



def get_random_thursday(start_date=date(2019, 9, 12)):
  today = date.today()

  while today.weekday() != 3:
    today -= timedelta(days=1)
  end_date = today

  while True:
    day_delta = random.randint(0, (end_date - start_date).days)
    random_date = start_date + timedelta(days=day_delta)

    if random_date.weekday() == 3:
      return random_date.strftime("%B-%d-%Y")  
    
def get_text():
    base_url = "https://jamesclear.com/3-2-1/"
    rdate = get_random_thursday(start_date=date(2019, 9, 12))
    url = base_url + rdate
    print(url)
    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'html.parser')
    get_div = soup.find("div", class_="page__content page-content-style")
    text = get_div
    print(text)
    return text


def strip_text(text, start_pattern, end_pattern):
  content = text
  pattern = f"{start_pattern}(.*?){end_pattern}"
  match = re.search(pattern, content, flags=re.DOTALL)

  if match:
    return match.group(1).strip()
  else:
    return None


text = get_text()
start_pattern = "I."
end_pattern = "II."

def check_404_error():
  if "Page not found - James Clear" in text:
    get_text()
    check_404_error()
    return text
  else:
    strip_text(text,start_pattern, end_pattern)
    return text


get_text()
text = check_404_error()
print(text)

