import json
from typing import Literal
from seleniumwire import webdriver
import seleniumwire.undetected_chromedriver as uc
from seleniumwire.utils import decode
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)


def login(email: str, password: str) -> dict[Literal["sign_in_response", "cookies"], dict]:
    driver.get("https://higgsfield.ai/auth/login")

    print("Get login page")

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="submit"]'))
    )

    email_input = driver.find_element(By.CSS_SELECTOR, 'input[type="email"]')
    email_input.clear()
    email_input.send_keys(email)

    print("Email entered")

    password_input = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
    password_input.send_keys(password)

    print("Password entered")

    login_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
    login_button.click()

    print("Login button clicked")

    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_to_be("https://higgsfield.ai/"))

    print("Redirected to home")

    cookies = {}
    sign_in_response = "{}"

    for request in driver.requests:
        if request.response:
            if "https://clerk.higgsfield.ai/v1/client/sign_ins" in request.url:
                sign_in_response = decode(
                    request.response.body, request.response.headers.get("Content-Encoding", "identity")
                )
                print(sign_in_response)
            if "set-cookie" in request.response.headers:
                header = request.response.headers["set-cookie"]
                cookie = header.split(";", 1)
                key, value = cookie[0].split("=")
                cookies[key] = value

    return {"sign_in_response": json.loads(sign_in_response), "cookies": cookies}
