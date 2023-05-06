from django.test import LiveServerTestCase
from django.utils import translation
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait


class ProductTest(LiveServerTestCase):

    def setup(self):
        translation.activate("en")
        self.options = Options()
        # self.options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(options=self.options)
        self.browser.maximize_window()
        self.signIntoAccount()
        self.products_end_point = "http://127.0.0.1:8000/en/products/"
        self.create_end_point = "http://127.0.0.1:8000/en/products/create/"
        self.build_expected()

    def build_expected(self):
        self.expected_product_create = {"step1": dict(
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
            invalidName=translation.gettext("message:product_name_length_error"),
            existingName=translation.gettext("message:product_exists_error"),
        ), "step3": dict(
            invalidDesc=translation.gettext("message:product_description_length_error"),
        ), "step4": dict(
            invalidAmount=translation.gettext("message:product_amount_error"),
        ), "step5": dict(
            invalidUnit=translation.gettext("message:product_unit_length_error"),
        ), "step6": dict(
            invalidPrice=translation.gettext("message:product_price_error"),
        ), "step7": dict(
            invalidBrand=translation.gettext("message:product_brand_error"),
        ), "step8": dict(
            success=translation.gettext("message:product_created"),
        ), "step9": dict(
            name="Product Test",
            description="Product Test description",
            amount="1",
            unit="kg",
            price="158.00",
            brand="Samsung",
        )}
        self.expected_product_update = {"step1": dict(
            successUpdate=translation.gettext("message:product_updated")),
            "step2": dict(
                nameUpdated="Product Test Updated",
                descriptionUpdated="Product Test description updated",
                amountUpdated="2",
                unitUpdated="gr",
                priceUpdated="147.00",
                brandUpdated="Samsung",
            )}
        self.expected_product_delete = {"step1": dict(
            isWarningVisible=True,
            isConfirmVisible=True, )}

    def test_Create_Product(self):
        self.setup()
        print("Step 1: Open the product edit page")
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
            self.expected_product_create["step1"],
            self.actualResultCreateStep1,
            f"There should be {len(self.fields_labels)} fields {self.fields_labels}"
        )

        # Step 2 - Create: Fill the name field with incorrect data.(Shorter than 3 or longer than 30)

        print(
            "Step 2: (Create) Fill the name field with incorrect data.(Shorter than 3 or longer than 30)"
        )
        self.fillFieldsAndClickButton("1", "Product1 Description", "1", "kg", "123", 1)

        self.actualResultCreateStep2 = dict(
            invalidName=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )

        self.fillFieldsAndClickButton("Test Product", "Product1 Description", "1", "kg", "123", 1)
        self.actualResultCreateStep2["existingName"] = self.browser.find_element(
            By.XPATH,
            "//span[contains(@class, 'text-danger')]"
        ).text
        self.assertEqual(
            self.expected_product_create["step2"],
            self.actualResultCreateStep2,
            "Name validation errors."
        )

        # Step 3 - Create: Fill the description field with incorrect data.(Shorter than 3 or longer than 100)

        print(
            "Step 3: (Create) Fill the description field with incorrect data.(Shorter than 3 or longer than 100)"
        )
        self.fillFieldsAndClickButton("Product 2", "Pp", "1", "kg", "123", 1)
        self.actualResultCreateStep3 = dict(
            invalidDesc=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )
        self.assertEqual(
            self.expected_product_create["step3"],
            self.actualResultCreateStep3,
            "Description validation errors."
        )

        # Step 4 - Create: Fill the amount field with incorrect data.(Shorter than 0 or longer than 99999999)

        print(
            "Step 4: (Create) Fill the amount field with incorrect data.(Shorter than 0 or longer than 99999999)"
        )
        self.fillFieldsAndClickButton("Product 2", "Product 2 description", "-1", "kg", "123", 1)
        self.actualResultCreateStep4 = dict(
            invalidAmount=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )
        self.assertEqual(
            self.expected_product_create["step4"],
            self.actualResultCreateStep4,
            "Amount validation errors."
        )

        # Step 5 - Create: Fill the unit field with incorrect data.(Shorter than 1 or longer than 10)

        print(
            "Step 5: (Create) Fill the unit field with incorrect data.(Shorter than 1 or longer than 10)"
        )

        self.fillFieldsAndClickButton("Product 2", "Product 2 description", "1", "kgkgkgkgkgkg", "123", 1)
        self.actualResultCreateStep5 = dict(
            invalidUnit=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )
        self.assertEqual(
            self.expected_product_create["step5"],
            self.actualResultCreateStep5,
            "Unit validation errors."
        )

        # Step 6 - Create: Fill the price field with incorrect data.(Shorter than 0 or longer than 99999999)

        print(
            "Step 6: (Create) Fill the price field with incorrect data.(Shorter than 0 or longer than 99999999)"
        )

        self.fillFieldsAndClickButton("Product 2", "Product 2 description", "1", "kg", "-99999", 1)
        self.actualResultCreateStep6 = dict(
            invalidPrice=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )
        self.assertEqual(
            self.expected_product_create["step6"],
            self.actualResultCreateStep6,
            "Price validation errors."
        )

        # Step 7 - Create: Fill the brand field with incorrect data.(When brand is not selected)

        print(
            "Step 7: (Create) Fill the brand field with incorrect data.(When brand is not selected)"
        )

        self.fillFieldsAndClickButton("Product 2", "Product 2 description", "1", "kg", "158", 0)
        self.actualResultCreateStep7 = dict(
            invalidBrand=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )
        self.assertEqual(
            self.expected_product_create["step7"],
            self.actualResultCreateStep7,
            "Brand validation errors."
        )

        # Step 8 - Create: Add a new product with correct data and see success message.

        print(
            "Step 8: (Create) Add a new product with correct data and see success message."
        )

        self.fillFieldsAndClickButton("Product Test", "Product Test description", "1", "kg", "158", 1)
        self.actualResultCreateStep8 = dict(
            success=self.browser.find_element(By.XPATH, "//div[contains(@class, 'alert')]").text,
        )

        self.assertEqual(
            self.expected_product_create["step8"],
            self.actualResultCreateStep8,
            "Product created successfully."
        )

        # Step 9 - Create: Control if the product is added to the list.
        self.actualResultCreateStep9 = dict(
            name=self.browser.find_element(By.XPATH, "//td[contains(text(), 'Product Test')]").text,
            description=self.browser.find_element(By.XPATH, "//td[contains(text(), 'Product Test description')]").text,
            amount=self.browser.find_element(By.XPATH, "//td[contains(text(), '1')]").text,
            unit=self.browser.find_element(By.XPATH, "//td[contains(text(), 'kg')]").text,
            price=self.browser.find_element(By.XPATH, "//td[contains(text(), '158')]").text,
            brand=self.browser.find_element(By.XPATH, "//td[contains(text(), 'Samsung')]").text,
        )

        self.assertEqual(
            self.expected_product_create["step9"],
            self.actualResultCreateStep9,
            "Product added to the list."
        )

    def test_Update_Product(self):
        self.setup()
        # Step 1 - Update: Click the update button of the product and see success message.
        print("# Step 1 - Update: Click the update button of the product and see success message.")
        self.browser.get(self.products_end_point)
        self.browser.find_element(By.XPATH,
                                  '(//table[contains(@class, \'table-striped\')]//tbody//tr//td)[9]//a').click()

        self.fillFieldsAndClickButton("Product Test Updated", "Product Test description updated", "2", "gr", "147", 1)
        self.actualResultUpdateStep1 = dict(
            successUpdate=self.browser.find_element(By.XPATH, "//div[contains(@class, 'alert')]").text
        )

        self.assertEqual(
            self.expected_product_update["step1"],
            self.actualResultUpdateStep1,
            "Product is updated."
        )

        # Step 2 - Update: Control if the product is updated on the list.
        print("# Step 2 - Update: Control if the product is updated.")
        self.actualResultUpdateStep2 = dict(
            nameUpdated=self.browser.find_element(By.XPATH, "//td[contains(text(), 'Product Test Updated')]").text,
            descriptionUpdated=self.browser.find_element(By.XPATH,
                                                         "//td[contains(text(), 'Product Test description updated')]").text,
            amountUpdated=self.browser.find_element(By.XPATH, "//td[contains(text(), '2')]").text,
            unitUpdated=self.browser.find_element(By.XPATH, "//td[contains(text(), 'gr')]").text,
            priceUpdated=self.browser.find_element(By.XPATH, "//td[contains(text(), '147')]").text,
            brandUpdated=self.browser.find_element(By.XPATH, "//td[contains(text(), 'Samsung')]").text,
        )

        self.assertEqual(
            self.expected_product_update["step2"],
            self.actualResultUpdateStep2,
            "Product updated and visible on the list."
        )

    def Test_Delete_Product(self):
        self.setup()
        # Step 1 - Delete: Click the delete button of the product and see alert message.
        print("# Step 1 - Delete: Click the delete button of the product and see success message.")
        self.browser.get(self.products_end_point)
        self.browser.find_element(By.XPATH,
                                  '(//table[contains(@class, \'table-striped\')]//tbody//tr//td)[10]//a').click()

        self.actualResultDeleteStep1 = dict(
            IsWarningVisible=self.browser.find_element(By.XPATH, "//div[contains(@class, 'swal2-modal')]")
        )

        # Step 2 - Delete: Click the delete button on the swal message and see success message.
        print("# Step 2 - Delete: Click the delete button on the alert message and see success message.")
        self.browser.find_element(By.XPATH, "//button[contains(text(), 'Delete')]").click()
        self.actualResultDeleteStep1["isConfirmVisible"] = self.browser.find_element(By.XPATH,
                                                                                     "//div[contains(@class, 'swal2-modal')]")
        self.assertEqual(
            self.expected_product_delete["step1"],
            self.actualResultDeleteStep1,
            "Product is deleted."
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
        self.browser.find_element(By.XPATH, "//input[@automation-id='product-name']").clear()
        self.browser.find_element(By.XPATH, "//textarea[@automation-id='product-description']").clear()
        self.browser.find_element(By.XPATH, "//input[@automation-id='product-amount']").clear()
        self.browser.find_element(By.XPATH, "//input[@automation-id='product-unit']").clear()
        self.browser.find_element(By.XPATH, "//input[@automation-id='product-price']").clear()
        Select(self.browser.find_element(By.XPATH, "//select[@automation-id='product-brand']")).select_by_index(0)

    def fillFieldsAndClickButton(self, productName, productDesc, productAmount, productUnit, productPrice, indexBrand):
        self.clearFields()
        self.browser.find_element(By.XPATH, "//input[@automation-id='product-name']").send_keys(productName)
        self.browser.find_element(By.XPATH, "//textarea[@automation-id='product-description']").send_keys(productDesc)
        self.browser.find_element(By.XPATH, "//input[@automation-id='product-amount']").send_keys(productAmount)
        self.browser.find_element(By.XPATH, "//input[@automation-id='product-unit']").send_keys(productUnit)
        self.browser.find_element(By.XPATH, "//input[@automation-id='product-price']").send_keys(productPrice)
        Select(self.browser.find_element(By.XPATH, "//select[@automation-id='product-brand']")).select_by_index(
            indexBrand)
        self.getAndClickButton()
