from django.test import LiveServerTestCase
from django.utils import translation
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class CustomerTest(LiveServerTestCase):

    def setup(self):
        translation.activate("en")
        self.options = Options()
        # self.options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(options=self.options)
        self.browser.maximize_window()
        self.signIntoAccount()
        self.entry_point = f"http://127.0.0.1:8000/en/customers/create"
        self.fields = [
            "customer-name",
            "customer-surname",
            "customer-email",
            "customer-phone",
            "customer-address"
        ]
        self.build_expected()

    def build_expected(self):
        self.expected = {"step1": dict(
            fields=[
                translation.gettext('label:firstname'),
                translation.gettext('label:surname'),
                translation.gettext('label:email'),
                translation.gettext('label:phone_number'),
                translation.gettext('label:address'),
            ],
            length=5
        ), "step2": dict(
            firstnamelength=translation.gettext("message:firstname_length"),
            namevalidation=translation.gettext("message:firstname_letters_include"),
        ), "step3": dict(
            surnamelength=translation.gettext("message:surname_length"),
            surnamevalidation=translation.gettext("message:surname_letters_include")
        ), "step4": dict(
            emailformat="Enter a valid email address."
        ), "step5": dict(
            phoneformat=translation.gettext("message:phone_format")
        ), "step6": dict(
            adressformat=translation.gettext("message:address_length")
        ), "step7": dict(
            success_message=translation.gettext("message:customer_created")
        ),
            "step8": dict(
                name="Emre",
                surname="Pelte",
                email="emre@emre.com",
                phone="905375016950",
                address="lkhjslkhsdfsdfsdfsdfsdfsdfsdfsdfsdf lsdgjsgj",
            )
        }
        self.expected_customer_update = {"step1": dict(
            successUpdate=translation.gettext("message:customer_updated")),
            "step2": dict(
                nameUpdated="Mehmet Emre",
                surnameUpdated="Pelte nisatali tatli",
                emailUpdated="emre@pelte.com",
                phoneUpdated="05375016888",
                addressUpdated="bla bla bla bla bla ",
            )}
        self.expected_customer_delete = {"step1": dict(
            isConfirmVisible=True,
            isWarningVisible=True,
        )}

    def test_1create_customer(self):
        self.setup()
        self.browser.get(self.entry_point)
        print("Step 1: Open the customer page")
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
            "Step 2: enter short first name and numbers in name field"
        )
        self.fillFieldsAndClick("AB", "Pelte", "emre@emre.com", "905375016950",
                                "lkhjslkhsdfsdfsdfsdfsdfsdfsdfsdfsdf lsdgjsgj")
        self.actualResultStep2 = dict(
            firstnamelength=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )
        self.fillFieldsAndClick("535fgf", "Pelte", "emre@emre.com", "905375016950",
                                "lkhjslkhsdfsdfsdfsdfsdfsdfsdfsdfsdf lsdgjsgj")
        self.actualResultStep2["namevalidation"] = self.browser.find_element(By.XPATH,
                                                                             "//span[contains(@class, 'text-danger')]").text
        self.assertEqual(
            self.expected["step2"],
            self.actualResultStep2,
            "There should be validation errors."
        )
        print("---------------------------------")

        print(
            "Step 3: enter short surname name and numbers in surname field"
        )
        self.fillFieldsAndClick("Emre", "as", "emre@emre.com", "905375016950",
                                "lkhjslkhsdfsdfsdfsdfsdfsdfsdfsdfsdf lsdgjsgj")
        self.actualResultStep3 = dict(
            surnamelength=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )
        self.fillFieldsAndClick("Emre", "535fgf", "emre@emre.com", "905375016950",
                                "lkhjslkhsdfsdfsdfsdfsdfsdfsdfsdfsdf lsdgjsgj")
        self.actualResultStep3["surnamevalidation"] = self.browser.find_element(By.XPATH,
                                                                                "//span[contains(@class, 'text-danger')]").text
        self.assertEqual(
            self.expected["step3"],
            self.actualResultStep3,
            "There should be validation errors."
        )
        print("---------------------------------")

        print(
            "Step 4: Enter incorrect e-mail format"
        )
        self.fillFieldsAndClick("Emre", "Pelte", "pelteemre", "905375016950",
                                "lkhjslkhsdfsdfsdfsdfsdfsdfsdfsdfsdf lsdgjsgj")
        self.actualResultStep4 = dict(
            emailformat=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text
        )
        self.assertEqual(
            self.expected["step4"],
            self.actualResultStep4,
            "There should be validation errors."
        )
        print("---------------------------------")

        print(
            "Step 5: Enter incorrect Phone format"
        )
        self.fillFieldsAndClick("Emre", "Pelte", "pelte@emre.com", "904375h16950",
                                "lkhjslkhsdfsdfsdfsdfsdfsdfsdfsdfsdf lsdgjsgj")
        self.actualResultStep5 = dict(
            phoneformat=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text
        )
        self.assertEqual(
            self.expected["step5"],
            self.actualResultStep5,
            "There should be validation errors."
        )
        print("---------------------------------")

        print(
            "Step 6: Enter incorrect adress format"
        )
        self.fillFieldsAndClick("Emre", "Pelte", "pelte@emre.com", "904375716950",
                                "lkhjs")
        self.actualResultStep6 = dict(

            adressformat=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text
        )
        self.assertEqual(
            self.expected["step6"],
            self.actualResultStep6,
            "There should be validation errors."
        )
        print("---------------------------------")

        print(
            "Step 7: SAVE VALID DATA"
        )
        self.fillFieldsAndClick("Emre", "Pelte", "emre@emre.com", "905375016950",
                                "lkhjslkhsdfsdfsdfsdfsdfsdfsdfsdfsdf lsdgjsgj")
        self.actualResultStep7 = dict(
            success_message=self.browser.find_element(By.XPATH, "//div[contains(@class, 'alert')]").text,
        )
        self.assertEqual(
            self.expected["step7"],
            self.actualResultStep7,
            "There should be validation errors."
        )
        print("---------------------------------")
        print("Check if data saved")
        self.actualResultStep8 = dict(
            name=self.browser.find_element(By.XPATH, "//td[contains(text(), 'Emre')]").text,
            surname=self.browser.find_element(By.XPATH, "//td[contains(text(), 'Pelte')]").text,
            email=self.browser.find_element(By.XPATH, "//td[contains(text(), 'emre@emre.com')]").text,
            phone=self.browser.find_element(By.XPATH, "//td[contains(text(), '905375016950')]").text,
            address=self.browser.find_element(By.XPATH,
                                              "//td[contains(text(), 'lkhjslkhsdfsdfsdfsdfsdfsdfsdfsdfsdf lsdgjsgj')]").text,
        )

        self.assertEqual(
            self.expected["step8"],
            self.actualResultStep8,
            "Customer added to the list."
        )

    def test_2update_customer(self):
        self.setup()
        # Step 1 - Update: Click the update button, update the customer and see success message.
        print("# Step 1 - Update: Click the update button, update the custoer and see success message.")
        self.browser.get(f"http://127.0.0.1:8000/en/customers")
        self.browser.find_element(By.XPATH,
                                  '(//table[contains(@class, \'table-striped\')]//tbody//tr//td)[8]//a').click()

        self.fillFieldsAndClick("MehmetEmre", "Peltee", "emre@pelte.com", "05375016888"
                                , "bla bla bla bla bla ")
        self.actualResultUpdateStep1 = dict(
            successUpdate=self.browser.find_element(By.XPATH, "//div[contains(@class, 'alert')]").text
        )

        self.assertEqual(
            self.expected_customer_update["step1"],
            self.actualResultUpdateStep1,
            "customer is updated."
        )

        # Step 2 - Update: Control if the customer is updated on the list.
        print("# Step 2 - Update: Control if the customer is updated.")
        self.actualResultUpdateStep2 = dict(
            nameUpdated=self.browser.find_element(By.XPATH, "//td[contains(text(), 'MehmetEmre')]").text,
            surnameUpdated=self.browser.find_element(By.XPATH,
                                                     "//td[contains(text(), 'Peltee')]").text,
            emailUpdated=self.browser.find_element(By.XPATH, "//td[contains(text(), 'emre@pelte.com')]").text,
            phoneUpdated=self.browser.find_element(By.XPATH,
                                                   "//td[contains(text(), '05375016888')]").text,
            addressUpdated=self.browser.find_element(By.XPATH,
                                                     "//td[contains(text(), 'bla bla bla bla bla')]").text
        )

        self.assertEqual(
            self.expected_customer_update["step2"],
            self.actualResultUpdateStep2,
            "customer updated and visible on the list."
        )

    def test_3delete_customer(self):
        self.setup()
        # Step 1 - Delete: Click the delete button of the customer and see alert window is visible.
        print("# Step 1 - Delete: Click the delete button of the customer and see alert window is visible.")
        self.browser.get(f"http://127.0.0.1:8000/en/customers")
        self.browser.find_element(By.XPATH,
                                  '(//table[contains(@class, \'table-striped\')]//tbody//tr//td)[9]//a').click()

        self.actualResultDeleteStep1 = dict(
            IsWarningVisible=self.browser.find_element(By.XPATH,
                                                       "//div[contains(@class, 'swal2-warning')]").is_displayed()
        )

        # Step 2 - Delete: Click the delete button on the swal message and see success message.
        print("# Step 2 - Delete: Click the delete button on the alert message and see success message.")
        self.browser.find_element(By.XPATH, "//button[contains(text(), 'Delete')]").click()
        self.actualResultDeleteStep1["isConfirmVisible"] = self.browser.find_element(By.XPATH,
                                                                                     "//div[contains(@class, 'swal2-modal')]").is_displayed()
        self.assertTrue(
            self.actualResultDeleteStep1,
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

    def signIntoAccount(self):
        self.browser.get("http://127.0.0.1:8000/en/login/")
        self.browser.find_element(By.XPATH, "//input[@automation-id='signin-email']").send_keys(
            "admin@admin.com")
        self.browser.find_element(By.XPATH, "//input[@automation-id='signin-password']").send_keys(
            "Appservers")
        self.getAndClickButton('signin-button')

    def clearFields(self):
        self.browser.find_element(By.XPATH, "//input[@automation-id='customer-name']") \
            .clear()
        self.browser.find_element(By.XPATH, "//input[@automation-id='customer-surname']") \
            .clear()
        self.browser.find_element(By.XPATH, "//input[@automation-id='customer-email']") \
            .clear()
        self.browser.find_element(By.XPATH, "//input[@automation-id='customer-phone']") \
            .clear()
        self.browser.find_element(By.XPATH, "//textarea[@automation-id='customer-address']") \
            .clear()

    def fillFieldsAndClick(self, name, surname, email, phone, address):
        self.clearFields()
        self.browser.find_element(By.XPATH, "//input[@automation-id='customer-name']") \
            .send_keys(name)
        self.browser.find_element(By.XPATH, "//input[@automation-id='customer-surname']") \
            .send_keys(surname)
        self.browser.find_element(By.XPATH, "//input[@automation-id='customer-email']") \
            .send_keys(email)
        self.browser.find_element(By.XPATH, "//input[@automation-id='customer-phone']") \
            .send_keys(phone)
        self.browser.find_element(By.XPATH, "//textarea[@automation-id='customer-address']") \
            .send_keys(address)
        self.getAndClickButton()