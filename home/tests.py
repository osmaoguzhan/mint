from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from django.utils import translation
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AuthTest(LiveServerTestCase):

    def setup(self):
        translation.activate("en")
        self.options = Options()
        self.options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(options=self.options)
        self.browser.maximize_window()
        self.entry_point_signup = "http://127.0.0.1:8000/en/signup/"
        self.entry_point_login = "http://127.0.0.1:8000/en/login/"
        self.build_expected()

    def build_expected(self):
        self.expected_signup = {
            "step1": dict(
                fields=[
                    translation.gettext('label:email_address'),
                    translation.gettext('label:company_name'),
                    translation.gettext('label:phone_number'),
                    translation.gettext('label:website_optional'),
                    translation.gettext('label:address'),
                    translation.gettext('label:password'),
                    translation.gettext('label:password_confirmation')
                ],
                length=7
            ),
            "step2": dict(
                invalid=translation.gettext("message:email_format"),
                existing=translation.gettext("message:email_already_exists"),
            ),
            "step3": dict(
                invalid=translation.gettext("message:company_name_length_error"),
                existing=translation.gettext("message:company_name_already_exists")
            ),
            "step4": dict(
                invalid=translation.gettext("message:phone_format"),
                existing=translation.gettext("message:phone_number_already_exists")
            ),
            "step5": dict(
                invalid=translation.gettext("message:company_address_length_error"),
                empty=translation.gettext("message:address_is_required")
            ),
            "step6": dict(
                length_error=translation.gettext("message:password_length_error"),
                is_digit=translation.gettext("message:password_at_least_one_letter"),
                is_alpha=translation.gettext("message:password_at_least_one_number"),
                is_upper=translation.gettext("message:password_at_least_one_lowercase"),
                is_lower=translation.gettext("message:password_at_least_one_uppercase"),
                is_special=translation.gettext("message:password_at_least_one_special_character")
            ),
            "step7": dict(
                not_match=translation.gettext("message:passwords_do_not_match")
            ),
            "step8": dict(
                is_visible=True,
                redirected_to="http://127.0.0.1:8000/en/login/"
            )
        }
        self.expected_login = {
            "step1": dict(
                fields=[
                    translation.gettext('label:email_address'),
                    translation.gettext('label:password')
                ],
                length=2
            ),
            "step2": True,
            "step3": "http://127.0.0.1:8000/en/dashboard/"
        }

    def test_2signin(self):
        self.setup()
        print("Entry point: " + self.entry_point_login)
        self.browser.get(self.entry_point_login)
        print("Step 1: Open the signin page")
        self.fields_signin_ui = self.browser.find_elements(
            By.XPATH,
            "//*[@automation-id and not(contains(@type, 'submit'))]"
        )
        self.fields_signin_labels = []
        for field in self.fields_signin_ui:
            self.fields_signin_labels.append(field.get_attribute("placeholder"))
        self.actualResultSigninStep1 = dict(
            fields=self.fields_signin_labels,
            length=len(self.fields_signin_labels)
        )
        self.assertEqual(
            self.expected_login["step1"],
            self.actualResultSigninStep1,
            "There should be 2 fields in the login page."
        )

        print("Step 2: Fill the form with incorrect data")
        self.browser.find_element(By.XPATH, "//input[@automation-id='signin-email']").send_keys(
            "admin@admin.com")
        self.browser.find_element(By.XPATH, "//input[@automation-id='signin-password']").send_keys(
            "aadsdasdas")
        self.getAndClickButton('signin-button')
        self.actualResulSignintStep2 = self.browser.find_element(
            By.XPATH,
            "//div[contains(@class, 'swal2-error')]"
        ).is_displayed(),
        self.assertTrue(self.actualResulSignintStep2, "There should be a popup with error message.")

        print("Step 3: Fill the form with correct data")
        self.browser.find_element(By.XPATH, "//input[@automation-id='signin-email']") \
            .clear()
        self.browser.find_element(By.XPATH, "//input[@automation-id='signin-password']") \
            .clear()
        self.browser.find_element(By.XPATH, "//input[@automation-id='signin-email']") \
            .send_keys("valid@email.com")
        self.browser.find_element(By.XPATH, "//input[@automation-id='signin-password']") \
            .send_keys("Example.1234")
        self.getAndClickButton('signin-button')
        self.actualResultSigninStep3 = self.browser.current_url
        self.assertEqual(
            self.expected_login["step3"],
            self.actualResultSigninStep3,
            "There should be a redirect to the dashboard page."
        )

    def test_1signup(self):
        self.setup()
        print("Entry point: " + self.entry_point_signup)
        self.browser.get(self.entry_point_signup)
        print("Step 1: Open the signup page")
        self.fields_signup_ui = self.browser.find_elements(
            By.XPATH,
            "//*[@automation-id and not(contains(@type, 'submit'))]"
        )
        self.fields_signup_labels = []
        for field in self.fields_signup_ui:
            self.fields_signup_labels.append(field.get_attribute("placeholder"))
        self.actualResultStep1 = dict(
            fields=self.fields_signup_labels,
            length=len(self.fields_signup_labels)
        )
        self.assertEqual(
            self.expected_signup["step1"],
            self.actualResultStep1,
            f"There should be {len(self.fields_signup_labels)} fields {self.fields_signup_labels}"
        )
        print(
            "Step 2: Fill the email field with incorrect data. Fill with the invalid format, later with an "
            "existing one. Fill the others with correct data"
        )
        # Email invalid case
        self.fillFieldsAndClick("Example", "Test Company", "905375016950", "Test address", "Example.123", "Example.123")
        self.actualResultStep2 = dict(
            invalid=self.browser.find_element(
                By.XPATH,
                "//span[contains(@class, 'text-danger')]"
            ).text
        )
        # Email existing case
        self.fillFieldsAndClick("admin@admin.com", "Test Company", "905375016950", "Test address", "Example.123",
                                "Example.123")
        self.actualResultStep2["existing"] = self.browser.find_element(
            By.XPATH,
            "//span[contains(@class, 'text-danger')]"
        ).text
        self.assertEqual(
            self.expected_signup["step2"],
            self.actualResultStep2,
            "There should be validation errors for email address field."
        )

        print("Step 3: Fill the company name field with incorrect data. Fill the others with correct data")
        # Company name existing case
        self.fillFieldsAndClick("valid@email.com", "appservers", "905375016950", "Test address", "Example.123",
                                "Example.123")
        self.actualResultStep3 = dict(
            existing=self.browser.find_element(
                By.XPATH,
                "//span[contains(@class, 'text-danger')]"
            ).text
        )
        # Company name length error case
        self.fillFieldsAndClick("valid@email.com", "a", "905375016950", "Test address", "Example.123", "Example.123")
        self.actualResultStep3["invalid"] = self.browser.find_element(
            By.XPATH,
            "//span[contains(@class, 'text-danger')]"
        ).text
        self.assertEqual(
            self.expected_signup["step3"],
            self.actualResultStep3,
            "There should be validation errors for company name field."
        )

        print("Step 4: Fill the phone number field with incorrect data. Fill the others with correct data")
        # phone number invalid case
        self.fillFieldsAndClick("valid@email.com", "new company", "fsfsf321412", "Test address", "Example.123",
                                "Example.123")
        self.actualResultStep4 = dict(
            invalid=self.browser.find_element(
                By.XPATH,
                "//span[contains(@class, 'text-danger')]"
            ).text
        )
        # phone number length error case
        self.fillFieldsAndClick("valid@email.com", "new company", "+48510373086", "Test address", "Example.123",
                                "Example.123")
        self.actualResultStep4["existing"] = self.browser.find_element(
            By.XPATH,
            "//span[contains(@class, 'text-danger')]"
        ).text
        self.assertEqual(
            self.expected_signup["step4"],
            self.actualResultStep4,
            "There should be validation errors for phone number field."
        )

        print("Step 5: Fill the address field with incorrect data. Fill the others with correct data")
        # address invalid case
        self.fillFieldsAndClick("valid@email.com", "new company", "+48510373085", "ss", "Example.123",
                                "Example.123")
        self.actualResultStep5 = dict(
            invalid=self.browser.find_element(
                By.XPATH,
                "//span[contains(@class, 'text-danger')]"
            ).text
        )
        self.fillFieldsAndClick("valid@email.com", "new company", "+48510373085", "", "Example.123",
                                "Example.123")
        self.actualResultStep5["empty"] = self.browser.find_element(
            By.XPATH,
            "//span[contains(@class, 'text-danger')]"
        ).text
        self.assertEqual(
            self.expected_signup["step5"],
            self.actualResultStep5,
            "There should be validation errors for address field."
        )

        print("Step 6: Fill the password field with incorrect data. Fill the others with correct data")
        # password invalid case
        self.fillFieldsAndClick("valid@email.com", "new company", "+48510373085", "new address", "12",
                                "12")
        self.actualResultStep6 = dict(
            length_error=self.browser.find_element(
                By.XPATH,
                "//span[contains(@class, 'text-danger')]"
            ).text
        )
        self.fillFieldsAndClick("valid@email.com", "new company", "+48510373085", "new address", "123456",
                                "123456")
        self.actualResultStep6["is_digit"] = self.browser.find_element(
            By.XPATH,
            "//span[contains(@class, 'text-danger')]"
        ).text
        self.fillFieldsAndClick("valid@email.com", "new company", "+48510373085", "new address", "asdfgh",
                                "asdfgh")
        self.actualResultStep6["is_alpha"] = self.browser.find_element(
            By.XPATH,
            "//span[contains(@class, 'text-danger')]"
        ).text
        self.fillFieldsAndClick("valid@email.com", "new company", "+48510373085", "new address", "example.123",
                                "example.123")
        self.actualResultStep6["is_lower"] = self.browser.find_element(
            By.XPATH,
            "//span[contains(@class, 'text-danger')]"
        ).text
        self.fillFieldsAndClick("valid@email.com", "new company", "+48510373085", "new address", "EXAMPLE.123",
                                "EXAMPLE.123")
        self.actualResultStep6["is_upper"] = self.browser.find_element(
            By.XPATH,
            "//span[contains(@class, 'text-danger')]"
        ).text
        self.fillFieldsAndClick("valid@email.com", "new company", "+48510373085", "new address", "Example123",
                                "Example123")
        self.actualResultStep6["is_special"] = self.browser.find_element(
            By.XPATH,
            "//span[contains(@class, 'text-danger')]"
        ).text
        self.assertEqual(
            self.expected_signup["step6"],
            self.actualResultStep6,
            "There should be validation errors for password field."
        )

        print("Step 7: Fill the confirm password field with incorrect data. Fill the others with correct data")
        self.fillFieldsAndClick("valid@email.com", "new company", "+48510373085", "new address", "Example.123",
                                "Example1234")
        self.actualResultStep7 = dict(
            not_match=self.browser.find_element(
                By.XPATH,
                "//span[contains(@class, 'text-danger')]"
            ).text
        )
        self.assertEqual(
            self.expected_signup["step7"],
            self.actualResultStep7,
            "There should be validation errors for confirm password field."
        )

        print("Step 8: Enter correct data in all fields and click signup button")
        self.fillFieldsAndClick("valid@email.com", "new company", "+48510373085", "new address", "Example.1234",
                                "Example.1234")
        self.actualResultStep8 = dict(
            is_visible=self.browser.find_element(
                By.XPATH,
                "//div[contains(@class, 'swal2-success')]"
            ).is_displayed(),
            redirected_to=self.browser.current_url
        )
        self.assertEqual(
            self.expected_signup["step8"],
            self.actualResultStep8,
            "There should be a popup with success message and redirect to login page."
        )

    def getAndClickButton(self, id="general-submit-button"):
        try:
            wait = WebDriverWait(self.browser, 10)
            signup_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//button[@automation-id='{id}']")))
        except StaleElementReferenceException:
            signup_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//button[@automation-id='{id}']")))
        self.browser.execute_script("arguments[0].click();", signup_button)

    def clearFields(self):
        self.browser.find_element(By.XPATH, "//input[@automation-id='signup-email']") \
            .clear()
        self.browser.find_element(By.XPATH, "//input[@automation-id='signup-company-name']") \
            .clear()
        self.browser.find_element(By.XPATH, "//input[@automation-id='signup-phone-number']") \
            .clear()
        self.browser.find_element(By.XPATH, "//textarea[@automation-id='signup-address']") \
            .clear()
        self.browser.find_element(By.XPATH, "//input[@automation-id='signup-password1']") \
            .clear()
        self.browser.find_element(By.XPATH, "//input[@automation-id='signup-password2']") \
            .clear()

    def fillFieldsAndClick(self, email, company_name, phone_number, address, password1, password2):
        self.clearFields()
        self.browser.find_element(By.XPATH, "//input[@automation-id='signup-email']") \
            .send_keys(email)
        self.browser.find_element(By.XPATH, "//input[@automation-id='signup-company-name']") \
            .send_keys(company_name)
        self.browser.find_element(By.XPATH, "//input[@automation-id='signup-phone-number']") \
            .send_keys(phone_number)
        self.browser.find_element(By.XPATH, "//textarea[@automation-id='signup-address']") \
            .send_keys(address)
        self.browser.find_element(By.XPATH, "//input[@automation-id='signup-password1']") \
            .send_keys(password1)
        self.browser.find_element(By.XPATH, "//input[@automation-id='signup-password2']") \
            .send_keys(password2)
        self.getAndClickButton('signup-button')
