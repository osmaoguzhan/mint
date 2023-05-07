from django.test import LiveServerTestCase
from django.utils import translation
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class SupplierTest(LiveServerTestCase):

    def setup(self):
        translation.activate("en")
        self.options = Options()
        # self.options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(options=self.options)
        self.browser.maximize_window()
        self.signIntoAccount()
        self.suppliers_end_point = "http://127.0.0.1:8000/en/suppliers/"
        self.create_end_point = "http://127.0.0.1:8000/en/suppliers/create/"
        self.build_expected()

    def build_expected(self):
        self.expected_supplier_create = {"step1": dict(
            fields=[
                translation.gettext('label:name'),
                translation.gettext('label:email'),
                translation.gettext('label:phone'),
                translation.gettext('label:address'),
            ],
            length=4
        ), "step2": dict(
            invalidName=translation.gettext("message:supplier_name_length")
        ), "step3": dict(
            invalidEmail=translation.gettext("Enter a valid email address."),
        ), "step4": dict(
            invalidPhone=translation.gettext("message:phone_format"),
        ), "step5": dict(
            invalidAddress=translation.gettext("message:address_length"),
        ), "step6": dict(
            success=translation.gettext("message:supplier_created"),
        ), "step7": dict(
            name="Supplier Test",
            email="suppliertest@gmail.com",
            phone="05395516587",
            address="Test street Test city Test country",
        )}
        self.expected_supplier_update = {"step1": dict(
            successUpdate=translation.gettext("message:supplier_updated")),
            "step2": dict(
                nameUpdated="Supplier Test Updated",
                emailUpdated="suppliertestupdated@gmail.com",
                phoneUpdated="05375016888",
                addressUpdated="Test street Test city Test country Updated",
            )}
        self.expected_supplier_delete = {"step1": dict(
            isConfirmVisible=True,
            isWarningVisible=True,
             )}

    def test_1Create_Supplier(self):
        self.setup()
        print("Step 1: Open the supplier create page")
        self.browser.get(self.create_end_point)
        self.fields_ui = self.browser.find_elements(
            By.XPATH,
            "//*[@automation-id and not(contains(@type, 'submit'))]"
        )
        self.fields_labels = []
        for field in self.fields_ui:
            self.fields_labels.append(field.get_attribute("placeholder"))
        self.actualResultCreateStep1 = dict(
            fields=self.fields_labels,
            length=len(self.fields_labels)
        )
        self.assertEqual(
            self.expected_supplier_create["step1"],
            self.actualResultCreateStep1,
            f"There should be {len(self.fields_labels)} fields {self.fields_labels}"
        )

        # Step 2 - Create: Fill the name field with incorrect data.(Shorter than 3 or longer than 30)

        print(
            "Step 2: (Create) Fill the name field with incorrect data.(Shorter than 3 or longer than 30)"
        )
        self.fillFieldsAndClickButton("S", "suppliertest@gmail.com", "05375016952",
                                      "Test street Test city Test country")

        self.actualResultCreateStep2 = dict(
            invalidName=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )

        self.assertEqual(
            self.expected_supplier_create["step2"],
            self.actualResultCreateStep2,
            "Name validation errors."
        )

        # Step 3 - Create: Fill the email field with incorrect data.(It should be invalid format)

        print(
            "Step 3: (Create) Fill the email field with incorrect data.(wrong format)"
        )

        self.fillFieldsAndClickButton("Supplier Test", "suppliertestgmail.com", "05375016952",
                                      "Test street Test city Test country")
        self.actualResultCreateStep3 = dict(
            invalidEmail=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )
        self.assertEqual(
            self.expected_supplier_create["step3"],
            self.actualResultCreateStep3,
            "Email validation errors."
        )

        # Step 4 - Create: Fill the phone field with incorrect data.(It should be in valid format)

        print(
            "Step 4: (Create) Fill the phone field with incorrect data.(It should be invalid format)"
        )

        self.fillFieldsAndClickButton("Supplier Test", "suppliertest@gmail.com", "05",
                                      "Test street Test city Test country")
        self.actualResultCreateStep4 = dict(
            invalidPhone=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )
        self.assertEqual(
            self.expected_supplier_create["step4"],
            self.actualResultCreateStep4,
            "Phone validation errors."
        )

        # Step 5 - Create: Fill the address field with incorrect data.(Shorter than 15 or longer than 100)

        print(
            "Step 5: (Create) Fill the address field with incorrect data.(Shorter than 15 or longer than 100)"
        )

        self.fillFieldsAndClickButton("Supplier Test", "suppliertest@gmail.com", "05375016952", "Test street")
        self.actualResultCreateStep5 = dict(
            invalidAddress=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )
        self.assertEqual(
            self.expected_supplier_create["step5"],
            self.actualResultCreateStep5,
            "Address validation errors."
        )

        # Step 6 - Create: Add a new supplier with correct data and see success message.

        print(
            "Step 6: (Create) Add a new supplier with correct data and see success message."
        )

        self.fillFieldsAndClickButton("Supplier Test", "suppliertest@gmail.com", "05395516587",
                                      "Test street Test city Test country")
        self.actualResultCreateStep6 = dict(
            success=self.browser.find_element(By.XPATH, "//div[contains(@class, 'alert')]").text,
        )

        self.assertEqual(
            self.expected_supplier_create["step6"],
            self.actualResultCreateStep6,
            "Supplier created successfully."
        )

        # Step 7 - Create: Control if the supplier is added to the list.
        self.actualResultCreateStep7 = dict(
            name=self.browser.find_element(By.XPATH, "//td[contains(text(), 'Supplier Test')]").text,
            email=self.browser.find_element(By.XPATH, "//td[contains(text(), 'suppliertest@gmail.com')]").text,
            phone=self.browser.find_element(By.XPATH, "//td[contains(text(), '05395516587')]").text,
            address=self.browser.find_element(By.XPATH,
                                              "//td[contains(text(), 'Test street Test city Test country')]").text,
        )

        self.assertEqual(
            self.expected_supplier_create["step7"],
            self.actualResultCreateStep7,
            "Supplier added to the list and visible."
        )

    def test_2Update_Supplier(self):
        self.setup()
        # Step 1 - Update: Click the update button, update the supplier and see success message.
        print("# Step 1 - Update: Click the update button, update the supplier and see success message.")
        self.browser.get(self.suppliers_end_point)
        self.browser.find_element(By.XPATH,
                                  '(//table[contains(@class, \'table-striped\')]//tbody//tr//td)[7]//a').click()

        self.fillFieldsAndClickButton("Supplier Test Updated", "suppliertestupdated@gmail.com", "05375016888",
                                      "Test street Test city Test country Updated")
        self.actualResultUpdateStep1 = dict(
            successUpdate=self.browser.find_element(By.XPATH, "//div[contains(@class, 'alert')]").text
        )

        self.assertEqual(
            self.expected_supplier_update["step1"],
            self.actualResultUpdateStep1,
            "Supplier is updated."
        )

        # Step 2 - Update: Control if the supplier is updated on the list.
        print("# Step 2 - Update: Control if the supplier is updated.")
        self.actualResultUpdateStep2 = dict(
            nameUpdated=self.browser.find_element(By.XPATH, "//td[contains(text(), 'Supplier Test Updated')]").text,
            emailUpdated=self.browser.find_element(By.XPATH,
                                                   "//td[contains(text(), 'suppliertestupdated@gmail.com')]").text,
            phoneUpdated=self.browser.find_element(By.XPATH, "//td[contains(text(), '05375016888')]").text,
            addressUpdated=self.browser.find_element(By.XPATH,
                                                     "//td[contains(text(), 'Test street Test city Test country Updated')]").text
        )

        self.assertEqual(
            self.expected_supplier_update["step2"],
            self.actualResultUpdateStep2,
            "Supplier updated and visible on the list."
        )

    def test_3Delete_Supplier(self):
        self.setup()
        # Step 1 - Delete: Click the delete button of the supplier and see alert window is visible.
        print("# Step 1 - Delete: Click the delete button of the supplier and see alert window is visible.")
        self.browser.get(self.suppliers_end_point)
        self.browser.find_element(By.XPATH,
                                  '(//table[contains(@class, \'table-striped\')]//tbody//tr//td)[8]//a').click()

        self.actualResultDeleteStep1 = dict(
            IsWarningVisible=self.browser.find_element(By.XPATH, "//div[contains(@class, 'swal2-warning')]").is_displayed()
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
            button = wait.until(
                ec.element_to_be_clickable((By.XPATH, f"//button[@automation-id='{id}']")))
        except StaleElementReferenceException:
            button = wait.until(
                ec.element_to_be_clickable((By.XPATH, f"//button[@automation-id='{id}']")))
        self.browser.execute_script("arguments[0].click();", button)

    def signIntoAccount(self):
        self.browser.get("http://127.0.0.1:8000/en/login/")
        self.browser.find_element(By.XPATH, "//input[@automation-id='signin-email']").send_keys(
            "admin@admin.com")
        self.browser.find_element(By.XPATH, "//input[@automation-id='signin-password']").send_keys(
            "Appservers")
        self.getAndClickButton('signin-button')

    def clearFields(self):
        self.browser.find_element(By.XPATH, "//input[@automation-id='supplier-name']").clear()
        self.browser.find_element(By.XPATH, "//input[@automation-id='supplier-email']").clear()
        self.browser.find_element(By.XPATH, "//input[@automation-id='supplier-phone']").clear()
        self.browser.find_element(By.XPATH, "//textarea[@automation-id='supplier-address']").clear()

    def fillFieldsAndClickButton(self, supplier_name, supplier_email, supplier_phone, supplier_address):
        self.clearFields()
        self.browser.find_element(By.XPATH, "//input[@automation-id='supplier-name']").send_keys(supplier_name)
        self.browser.find_element(By.XPATH, "//input[@automation-id='supplier-email']").send_keys(supplier_email)
        self.browser.find_element(By.XPATH, "//input[@automation-id='supplier-phone']").send_keys(supplier_phone)
        self.browser.find_element(By.XPATH, "//textarea[@automation-id='supplier-address']").send_keys(supplier_address)
        self.getAndClickButton()
