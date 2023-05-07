from django.test import LiveServerTestCase
from django.utils import translation
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select


class OrderTest(LiveServerTestCase):

    def setup(self):
        translation.activate("en")
        self.options = Options()
        self.options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(options=self.options)
        self.browser.maximize_window()
        self.signIntoAccount()
        self.entry_point = "http://127.0.0.1:8000/en/orders/create/"
        self.fields = [
            "order-name",
            "order-description",
            "order-amount",
            "order-price",
            "order-product",
            "order-customer"
        ]
        self.build_expected()

    def build_expected(self):
        self.expected = {"step1": dict(
            fields=[
                translation.gettext('label:name'),
                translation.gettext('label:description'),
                translation.gettext('label:amount'),
                translation.gettext('label:price'),
                translation.gettext('label:product_name'),
                translation.gettext('label:customer_name'),
            ],
            length=6
        ), "step2": dict(
            namelength=translation.gettext("message:order_name_error")
        ), "step3": dict(
            descriptionlength=translation.gettext("message:order_description_error"),
        ), "step4": dict(
            amountformat=translation.gettext("message:order_amount_error")
        ), "step5": dict(
            priceformat=translation.gettext("message:order_price_error")
        ), "step6": dict(
            productformat=translation.gettext("message:order_product_error")
        ), "step7": dict(
            customerformat=translation.gettext("message:order_customer_error")
        ),
        "step8": dict(
            success=translation.gettext("message:order_created_successfully"),
        ),
            "step9": dict(
            name="Phone",
            description="Iphone XMax Long",
            amount="1000",
            price="1000",
            product_name= "Smart Phone",
            customer_name= "Oğuzhan Osma",
        )
        }
        self.expected_order_update = {"step1": dict(
            successUpdate=translation.gettext("message:order_updated")),
            "step2": dict(
                nameUpdated="Order Test Updated",
                descriptionUpdated="Iphone 14 xmax",
                amountUpdated="2000",
                priceUpdated="2000",
                productUpdated="Smart Phone",
                customerUpdated="Oğuzhan Osma"
            )}
        self.expected_order_delete = {"step1": dict(
            isConfirmVisible=True,
            isWarningVisible=True,
             )}

    def test_1form(self):
        self.setup()
        self.browser.get(self.entry_point)
        print("Step 1: Open the order page")
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
            "Step 2: Order name and description should be at least 3 characters long"
        )
        self.fillFieldsAndClick("or", "order1 Description", "1", "100", 1, 1)
        self.actualResultStep2 = dict(
            namelength=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )

        self.assertEqual(
            self.expected["step2"],
            self.actualResultStep2,
            "Name length validation errors."
        )

        self.fillFieldsAndClick("order2", "d", "1", "1000", 1, 1)
        self.actualResultStep3 = dict(
            descriptionlength=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )

        self.assertEqual(
            self.expected["step3"],
            self.actualResultStep3,
            "Description validation errors."
        )

        print(
            "Step 3: AMount should be positive numbers"
        )
        self.fillFieldsAndClick("order2", "description", "-1", "1", 1, 1)
        self.actualResultStep4 = dict(
            amountformat=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )

        self.assertEqual(
            self.expected["step4"],
            self.actualResultStep4,
            "Amount format validation errors."
        )

        self.fillFieldsAndClick("order2", "description", "100", "-1", 1, 1)
        self.actualResultStep5 = dict(
            priceformat=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )

        self.assertEqual(
            self.expected["step5"],
            self.actualResultStep5,
            "Price format validation errors."
        )

        print(
            "Step 5: Product"
        )
        self.fillFieldsAndClick("order2", "description", "1000", "1000", 0, 1)
        self.actualResultStep6 = dict(
            productformat=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )

        self.assertEqual(
            self.expected["step6"],
            self.actualResultStep6,
            "Product format validation errors."
        )

        print(
            "Step 7: Customer"
        )
        self.fillFieldsAndClick("order2", "description", "1000", "1000", 1, 0)
        self.actualResultStep7 = dict(
            customerformat=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )

        self.assertEqual(
            self.expected["step7"],
            self.actualResultStep7,
            "Customer format validation errors."
        )

        print(
            "Step 8: Success"
        )
        self.fillFieldsAndClick("Phone", "Iphone XMax Long", "1000", "1000", 1, 1)
        self.actualResultStep8 = dict(
            success=self.browser.find_element(By.XPATH, "//div[contains(@class, 'alert')]").text,
        )

        self.assertEqual(
            self.expected["step8"],
            self.actualResultStep8,
            "Order created succesfully."
        )

        # Step 9 - Create: Control if the product is added to the list.
        self.actualResultCreateStep9 = dict(
            name=self.browser.find_element(By.XPATH, "//td[contains(text(), 'Phone')]").text,
            description=self.browser.find_element(By.XPATH, "//td[contains(text(), 'Iphone XMax Long')]").text,
            amount=self.browser.find_element(By.XPATH, "//td[contains(text(), '1000')]").text,
            price=self.browser.find_element(By.XPATH, "//td[contains(text(), '1000')]").text,
            product_name=self.browser.find_element(By.XPATH, "//td[contains(text(), 'Smart Phone')]").text,
            customer_name=self.browser.find_element(By.XPATH, "//td[contains(text(), 'Oğuzhan Osma')]").text,
        )

        self.assertEqual(
            self.actualResultCreateStep9["step9"],
            self.actualResultCreateStep9,
            "Order added to the list."
        )


    def test_2Update_Order(self):
        self.setup()
        # Step 1 - Update: Click the update button, update the supplier and see success message.
        print("# Step 1 - Update: Click the update button, update the supplier and see success message.")
        self.browser.get("http://127.0.0.1:8000/en/orders")
        self.browser.find_element(By.XPATH,
                                  '(//table[contains(@class, \'table-striped\')]//tbody//tr//td)[9]//a').click()

        self.fillFieldsAndClick("Order Test Updated", "Iphone 14 xmax", "2000",
                                      "2000", 1, 1)
        self.actualResultUpdateStep1 = dict(
            successUpdate=self.browser.find_element(By.XPATH, "//div[contains(@class, 'alert')]").text
        )

        self.assertEqual(
            self.expected_order_update["step1"],
            self.actualResultUpdateStep1,
            "Supplier is updated."
        )

        # Step 2 - Update: Control if the supplier is updated on the list.
        print("# Step 2 - Update: Control if the supplier is updated.")
        self.actualResultUpdateStep2 = dict(
            nameUpdated=self.browser.find_element(By.XPATH, "//td[contains(text(), 'Order Test Updated')]").text,
            descriptionUpdated=self.browser.find_element(By.XPATH,
                                                   "//td[contains(text(), 'Iphone 14 xmax')]").text,
            amountUpdated=self.browser.find_element(By.XPATH, "//td[contains(text(), '2000')]").text,
            priceUpdated=self.browser.find_element(By.XPATH,
                                                     "//td[contains(text(), '2000')]").text,
            productUpdated=self.browser.find_element(By.XPATH, "//td[contains(text(), 'Smart Phone')]").text,
            customerUpdated=self.browser.find_element(By.XPATH,
                                                     "//td[contains(text(), 'Oğuzhan Osma')]").text
        )

        self.assertEqual(
            self.expected_order_update["step2"],
            self.actualResultUpdateStep2,
            "Order updated and visible on the list."
        )

    def test_3Delete_Order(self):
        self.setup()
        # Step 1 - Delete: Click the delete button of the supplier and see alert window is visible.
        print("# Step 1 - Delete: Click the delete button of the supplier and see alert window is visible.")
        self.browser.get("http://127.0.0.1:8000/en/orders")
        self.browser.find_element(By.XPATH,
                                  '(//table[contains(@class, \'table-striped\')]//tbody//tr//td)[10]//a').click()

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
                EC.element_to_be_clickable((By.XPATH, f"//button[@automation-id='{id}']")))
        except StaleElementReferenceException:
            button = wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//button[@automation-id='{id}']")))
        self.browser.execute_script("arguments[0].click();", button)

    def signIntoAccount(self):
        self.browser.get("http://127.0.0.1:8000/en/login/")
        self.browser.find_element(By.XPATH, "//input[@automation-id='signin-email']").send_keys(
            "admin@admin.com")
        self.browser.find_element(By.XPATH, "//input[@automation-id='signin-password']").send_keys(
            "Appservers")
        self.getAndClickButton('signin-button')

    def clearFields(self):
        self.browser.find_element(By.XPATH, "//input[@automation-id='order-name']") \
            .clear()
        self.browser.find_element(By.XPATH, "//textarea[@automation-id='order-description']") \
            .clear()
        self.browser.find_element(By.XPATH, "//input[@automation-id='order-amount']") \
            .clear()
        self.browser.find_element(By.XPATH, "//input[@automation-id='order-price']") \
            .clear()
        Select(self.browser.find_element(By.XPATH, "//select[@automation-id='order-product']")).select_by_index(0)
        Select(self.browser.find_element(By.XPATH, "//select[@automation-id='order-customer']")).select_by_index(0)

    def fillFieldsAndClick(self, name, description, amount, price, productIndex, customerIndex):
        self.clearFields()
        self.browser.find_element(By.XPATH, "//input[@automation-id='order-name']") \
            .send_keys(name)
        self.browser.find_element(By.XPATH, "//textarea[@automation-id='order-description']") \
            .send_keys(description)
        self.browser.find_element(By.XPATH, "//input[@automation-id='order-amount']") \
            .send_keys(amount)
        self.browser.find_element(By.XPATH, "//input[@automation-id='order-price']") \
            .send_keys(price)
        Select(self.browser.find_element(By.XPATH, "//select[@automation-id='order-product']")).select_by_index(
            productIndex)
        Select(self.browser.find_element(By.XPATH, "//select[@automation-id='order-customer']")).select_by_index(
            customerIndex)
        self.getAndClickButton()