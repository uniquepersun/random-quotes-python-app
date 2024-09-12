from datetime import date, timedelta
import random
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

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
    
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
)

def get_text(url):
    request = requests.get(url)
    request.raise_for_status()
    soup = BeautifulSoup(request.content, 'html.parser')
    target_div = soup.find('div', class_='page__content page-content-style')
    if target_div:
        return target_div.get_text(strip=True)
    else:
        return None

def extract_with_gemini(content):
    chat_session = model.start_chat()
    prompt = f"""
    Extract the following information from the text provided below. 
    Return each item as a separate variable, NOT as a list or dictionary. And return only the asked information nothing else.
    - Each "IDEA FROM ME" should be in a separate variable (idea1, idea2, idea3). The ideas are given by james clear himself so author name should be in different variable (default_author) and source should be jame's newsletter (idea_source)
    - Each "QUOTE FROM OTHERS" should be in separate variables (quote1, quote2), along with their author (author1, author2) and source (source1, source2).
    - The "1 QUESTION FOR YOU" should be in a variable named 'question'. and for this one, make only source variable (question_source) and source will be jame's newsletter 

    TEXT:
    {content}
    """
    response = chat_session.send_message(prompt)
    gemini_output = response.text
    gemini_output = gemini_output.replace("```python", "").replace("```", "")
    # if not all(line.strip().startswith(valid_start) 
    #            for line in gemini_output.splitlines() 
    #            for valid_start in ["idea", "quote", "author", "source", "question", "default"]):
    #     print("Warning: Gemini output does not look like valid variable assignments.") //TODO: improve it as of now it is causing a lil error :)) TODO
    exec(gemini_output, globals())
    return 

if __name__ == "__main__":
    base_url = "https://jamesclear.com/3-2-1/"
    rdate = get_random_thursday(start_date=date(2019, 9, 12))
    url = base_url + rdate
    print(url)
    url = 'https://jamesclear.com/3-2-1/September-12-2019' 
    content = get_text(url)

    if content:
        extract_with_gemini(content)
        print(f"First idea is: +  {idea1}")
        print(f"second idea is: +  {idea2}")
        print(f"third idea is: +  {idea3}")
        print(f"Here is the first quote: +  {quote1}")
        print(f"The Author: +  {author1}")
        print(f"Here is the second quote: +  {quote2}")
        print(f"The Author: +  {author2}")
        print(f"Here is the question: +  {question}")
    else:
        print("Content not found on the page.")


