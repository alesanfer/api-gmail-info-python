# Api para verificacao espaco utilizado Gmail @alessandroferreira

import json
import time
from bottle import route, request,run, response
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

@route('/info', method='POST')
def buscaInfo():
    email = request.json['email']
    senha = request.json['senha']
    if "" != email and "" != senha:
        try:
            options = Options()
            options.headless = True
            driver = webdriver.Firefox(options=options)
            driver.get("http://mail.google.com")
            driver.find_element_by_id("identifierId").send_keys(email)
            time.sleep(5)
            driver.find_element_by_id("identifierNext").click()
            time.sleep(5)
            driver.find_element_by_name("password").send_keys(senha)
            time.sleep(5)
            driver.find_element_by_id("passwordNext").click()
            time.sleep(5)
            driver.get("https://drive.google.com/u/0/settings/storage?hl=pt-BR")
            info_utilizado = driver.find_element_by_css_selector('.H01aEe').get_attribute('innerHTML')
            info_total = driver.find_element_by_css_selector('.xl7bTb').get_attribute('innerHTML')
            ret = {"email": email,"utilizado": info_utilizado,"total": info_total}
            response.content_type = 'application/json'
            return json.dumps(ret, sort_keys=True)

        except Exception as inst:
            print(inst)
            return {"error": "erro ao buscar informacoes do e-mail: " + email}
    else:
        return {"error": "e-mail nao informado"}
run(host='localhost', port=8090, debug=True)
