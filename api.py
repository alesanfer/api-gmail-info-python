# Api para verificacao espaco utilizado Gmail @alessandroferreira

import json
import time
import os
import datetime
import bottle
from bottle import Bottle, route, request, run, response, HTTPResponse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# decorator cors


def allow_cors(func):
    def wrapper(*args, **kwargs):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
        return func(*args, **kwargs)
    return wrapper


app = Bottle()


@app.route('/api/info', method=['OPTIONS', 'POST'])
@allow_cors
def buscaInfo():

    email = request.POST.email
    print('requisitando informacoes para o email: ' + email)
    if email == os.environ['ID_EMAIL1']:
        senha = os.environ['EMAIL1']
    elif email == os.environ['ID_EMAIL2']:
        senha = os.environ['EMAIL2']
    elif email == os.environ['ID_EMAIL3']:
        senha = os.environ['EMAIL3']
    elif email == os.environ['ID_EMAIL4']:
        senha = os.environ['EMAIL4']
    else:
        response.body = json.dumps({"error": True, "msg": "e-mail nao cadastrado"}, sort_keys=True)
        return response

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
            info_utilizado = driver.find_element_by_css_selector(
                '.H01aEe').get_attribute('innerHTML')
            info_total = driver.find_element_by_css_selector(
                '.xl7bTb').get_attribute('innerHTML')
            now = datetime.datetime.now()
            ret = {
                "email": email,
                "utilizado": info_utilizado.replace("GB", "").strip(),
                "total": info_total.replace("GB", "").strip(),
                "data": now.strftime('%Y-%m-%d %H:%M:%S.%f'),
            }
            driver.quit()
            response.content_type = 'application/json'
            response._set_status = 200
            response.body = json.dumps(ret, sort_keys=True)
            return response

        except Exception as inst:
            print(inst)
            response.content_type = 'application/json'
            response._set_status = 500
            response.body = json.dumps(
                {"error": True, "msg": "erro ao buscar informacoes do e-mail: " + email}, sort_keys=True)
            return response

    else:
        response.content_type = 'application/json'
        response._set_status = 400
        response.body = json.dumps(
            {"error": True, "msg": "e-mail nao informado"}, sort_keys=True)
        return response


app.run(host='localhost', port=8090, debug=True)
