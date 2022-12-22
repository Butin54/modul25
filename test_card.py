import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

#python -m pytest -v -s --driver Chrome --driver-path D:/chromedriver.exe tests/test_card.py
PATH = "D:/chromedriver.exe"

@pytest.fixture(autouse=True)
def testing():
  chrome_options = Options()
  chrome_options.binary_location = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
  #chrome_options.add_argument('--headless')
  #chrome_options.add_argument('--no-sandbox')
  #chrome_options.add_argument('--disable-dev-shm-usage')

  pytest.driver = webdriver.Chrome(executable_path=PATH, chrome_options=chrome_options)
  pytest.driver.implicitly_wait(10)
  # Переходим на страницу авторизации
  pytest.driver.get('http://petfriends.skillfactory.ru/login')

  yield pytest.driver

  pytest.driver.quit()


def test_pets(testing):
  # Вводим email
  pytest.driver.find_element(By.ID, 'email').send_keys('butin54@yandex.ru')
  # Вводим пароль
  pytest.driver.find_element(By.ID, 'pass').send_keys('12345678')
  # Нажимаем на кнопку входа в аккаунт
  pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
  # Проверяем, что мы оказались на главной странице пользователя
  assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

  images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
  names = pytest.driver.find_elements(By.CSS_SELECTOR, ".card-deck .card-title")
  descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, ".card-deck .card-text")

  for i in range(len(names)):
    print(i, images[i].get_attribute("src")[:5], names[i].text, descriptions[i].text)
    assert images[i].get_attribute("src") != ''
    assert names[i].text != ''
    assert descriptions[i].text != ''
    assert ', ' in descriptions[i].text
    parts = descriptions[i].text.split(", ")
    assert len(parts[0]) > 0
    assert len(parts[1]) > 0


