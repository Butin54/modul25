import numpy as np
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


#python -m pytest -v -s --driver Chrome --driver-path D:/chromedriver.exe tests/test_table.py
PATH = "D:/chromedriver.exe"

@pytest.fixture(autouse=True)
def testing():
  chrome_options = Options()
  chrome_options.binary_location = 'C:\Program Files\Google\Chrome\Application\chrome.exe'


  pytest.driver = webdriver.Chrome(executable_path=PATH, chrome_options=chrome_options)
  # Переходим на страницу авторизации
  pytest.driver.get('http://petfriends.skillfactory.ru/login')

  yield

  pytest.driver.quit()


def test_show_my_pets(testing):
  # Вводим email
  pytest.driver.find_element(By.ID, 'email').send_keys('butin54@yandex.ru')
  # Вводим пароль
  pytest.driver.find_element(By.ID, 'pass').send_keys('12345678')
  # Нажимаем на кнопку входа в аккаунт
  pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
  # Переходим на страницу мои питомцы
  pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы").click()
  # Проверяем, что мы оказались на странице мои питомцы
  assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'

  pets = WebDriverWait(pytest.driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#all_my_pets table tbody tr')))
  lines_in_table = len(pets)
  quantity_pets  = pytest.driver.find_element(
    By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(":")[1]
  #print(lines_in_table, quantity_pets) для отладки
  assert lines_in_table == int(quantity_pets)

  images = WebDriverWait(pytest.driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#all_my_pets table tbody tr th img')))
  n = 0
  for i in range(len(images)):
    if images[i].get_attribute("src") != '':
      n += 1
  #print(n, len(images)/2) #для отладки
  assert n >= len(images)/2

  list_param = WebDriverWait(pytest.driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#all_my_pets table tbody tr td')))
  pets_param = list()
  for i in range(len(list_param)):
    pets_param.append(list_param[i].text)
  #print(pets_param) #для отладки
  #разбиваем список на части, количество частей соответствует количеству питомцев в таблице, записываем в массив
  pets = np.array_split(pets_param, len(images))
  for i in range(len(images)):
    #print(pets[i][0]) #для отладки
    #проверка что у всех питомцев есть имя
    assert pets[i][0] != ''
    #print(pets[i][1]) #для отладки
    #проверка что у всех питомцев есть порода
    assert pets[i][1] != ''
    #print(pets[i][2]) #для отладки
    #проверка что у всех питомцев есть возраст
    assert pets[i][2] != ''

  #создаем список имен питомцев
  names = list()
  for i in range(len(images)):
    names.append(pets[i][0])
  #print(names) #для отладки
  for i in range(len(names)):
    #проверяем что в списке имен каждое встречается только один раз
    assert names.count(names[i]) == 1

  #проверяем что списки в массиве петс уникальны
  m = 0
  for i in range(len(images)):
    for j in range(1, len(images)-i):
      #print(pets[i][0], pets[-j][0], pets[i][1], pets[-j][1], pets[i][2], pets[-j][2])
      if pets[i][0] == pets[-j][0] and pets[i][1] == pets[-j][1] and pets[i][2] == pets[-j][2]:
        m += 1
  #print(m)
  assert m == 0
  # python -m pytest -v -s --driver Chrome --driver-path D:/chromedriver.exe tests/test_table.py










