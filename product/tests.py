from django.test import LiveServerTestCase
from django.utils import translation
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class ProductTest(LiveServerTestCase):

    def setup(self):
        translation.activate("en")
        self.options = Options()
        self.options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(options=self.options)
        self.browser.maximize_window()
        self.signIntoAccount()
        self.entry_point = "http://127.0.0.1:8000/en/products/"
        self.fields = [
            "product-name",
            "product-description",
            "product-amount",
            "product-unit",
            "product-price",
            "product-brand"
        ]
        self.build_expected()

    def build_expected(self):
        self.expected = {"step1": dict(
            fields=[
                translation.gettext('label:name'),
                translation.gettext('label:description'),
                translation.gettext('label:amount'),
                translation.gettext('label:unit'),
                translation.gettext('label:price'),
                translation.gettext('label:brand_name'),
            ],
            length=6
        ), "step2": dict(
            invalid=translation.gettext("message:email_format"),
            existing=translation.gettext("message:email_already_exists"),
        )}

    def test_form(self):
        self.setup()
        self.browser.get(self.entry_point)
        print("Step 1: Open the product page")
        self.fields_ui = self.browser.find_elements(
            By.XPATH,
            "//*[@automation-id and not(contains(@type, 'submit'))]"
        )
        self.fields_labels = []
        for field in self.fields_ui:
            self.fields_labels.append(field.get_attribute("placeholder"))
        self.actualResultStep1 = dict(
            fields=self.fields_labels,
            length=len(self.fields_labels)
        )
        self.assertEqual(
            self.expected["step1"],
            self.actualResultStep1,
            f"There should be {len(self.fields_labels)} fields {self.fields_labels}"
        )

        print(
            "Step 2: Fill the email field with incorrect data. Fill with the invalid format, later with an "
            "existing one. Fill the others with correct data"
        )
        self.browser.find_element(By.XPATH, "//input[@automation-id='product-name']").send_keys("Product1")
        self.browser.find_element(By.XPATH, "//input[@automation-id='product-description']").send_keys("Product1 Description")
        self.browser.find_element(By.XPATH, "//input[@automation-id='product-amount']").send_keys("1")
        self.browser.find_element(By.XPATH, "//textarea[@automation-id='product-unit']").send_keys("Test address")
        self.browser.find_element(By.XPATH, "//input[@automation-id='product-price']").send_keys("Example.123")
        self.browser.find_element(By.XPATH, "//input[@automation-id='product-price']").send_keys("Example.123")
        self.getAndClickButton()
        self.actualResultStep2 = dict(
            invalid=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )
        self.browser.find_element(By.XPATH, "//input[@automation-id='signup-email']").clear()
        self.browser.find_element(By.XPATH, "//input[@automation-id='signup-email']").send_keys("admin@admin.com")
        self.browser.find_element(By.XPATH, "//input[@automation-id='signup-password1']").send_keys("Example.123")
        self.browser.find_element(By.XPATH, "//input[@automation-id='signup-password2']").send_keys("Example.123")
        self.getAndClickButton()
        self.actualResultStep2["existing"] = self.browser.find_element(
            By.XPATH,
            "//span[contains(@class, 'text-danger')]"
        ).text
        self.assertEqual(
            self.expected["step2"],
            self.actualResultStep2,
            "There should be validation errors."
        )
        print("---------------------------------")

    def getAndClickButton(self, id="general-submit-button"):
        try:
            wait = WebDriverWait(self.browser, 10)
            signup_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//button[@automation-id='{id}']")))
        except StaleElementReferenceException:
            signup_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//button[@automation-id='{id}']")))
        self.browser.execute_script("arguments[0].click();", signup_button)

    def signIntoAccount(self):
        self.browser.get("http://127.0.0.1:8000/en/login/")
        self.browser.find_element(By.XPATH, "//input[@automation-id='signin-email']").send_keys(
            "admin@admin.com")
        self.browser.find_element(By.XPATH, "//input[@automation-id='signin-password']").send_keys(
            "Appservers")
        self.getAndClickButton('signin-button')
