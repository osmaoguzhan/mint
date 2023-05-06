from django.test import LiveServerTestCase
from django.utils import translation
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select


class ProductTest(LiveServerTestCase):

    def setup(self):
        translation.activate("en")
        self.options = Options()
        #self.options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(options=self.options)
        self.browser.maximize_window()
        self.signIntoAccount()
        self.products_end_point = "http://127.0.0.1:8000/en/products/"
        self.create_end_point = "http://127.0.0.1:8000/en/products/create/"
        self.delete_end_point = "http://127.0.0.1:8000/en/products/delete/"
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
        self.actualResultStep1 = dict(
            fields=self.fields_labels,
            length=len(self.fields_labels)
        )
        self.assertEqual(
            self.expected["step1"],
            self.actualResultStep1,
            f"There should be {len(self.fields_labels)} fields {self.fields_labels}"
        )

        # Step 2 - Create: Fill the name field with incorrect data.(Shorter than 3 or longer than 30)

        print(
            "Step 2: (Create) Fill the name field with incorrect data.(Shorter than 3 or longer than 30)"
        )
        self.fillFieldsAndClickButton("1", "Product1 Description", "1", "kg", "123", 1)

        self.actualResultStep2 = dict(
            invalidName=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )

        self.fillFieldsAndClickButton("Test Product", "Product1 Description", "1", "kg", "123", 1)
        self.actualResultStep2["existingName"] = self.browser.find_element(
            By.XPATH,
            "//span[contains(@class, 'text-danger')]"
        ).text
        self.assertEqual(
            self.expected["step2"],
            self.actualResultStep2,
            "Name validation errors."
        )

        # Step 3 - Create: Fill the description field with incorrect data.(Shorter than 3 or longer than 100)

        print(
            "Step 3: (Create) Fill the description field with incorrect data.(Shorter than 3 or longer than 100)"
        )
        self.fillFieldsAndClickButton("Product 2", "Pp", "1", "kg", "123", 1)
        self.actualResultStep3 = dict(
            invalidDesc=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )
        self.assertEqual(
            self.expected["step3"],
            self.actualResultStep3,
            "Description validation errors."
        )

        # Step 4 - Create: Fill the amount field with incorrect data.(Shorter than 0 or longer than 99999999)

        print(
            "Step 4: (Create) Fill the amount field with incorrect data.(Shorter than 0 or longer than 99999999)"
        )
        self.fillFieldsAndClickButton("Product 2", "Product 2 description", "-1", "kg", "123", 1)
        self.actualResultStep4 = dict(
            invalidAmount=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )
        self.assertEqual(
            self.expected["step4"],
            self.actualResultStep4,
            "Amount validation errors."
        )

        # Step 5 - Create: Fill the unit field with incorrect data.(Shorter than 1 or longer than 10)

        print(
            "Step 5: (Create) Fill the unit field with incorrect data.(Shorter than 1 or longer than 10)"
        )

        self.fillFieldsAndClickButton("Product 2", "Product 2 description", "1", "kgkgkgkgkgkg", "123", 1)
        self.actualResultStep5 = dict(
            invalidUnit=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )
        self.assertEqual(
            self.expected["step5"],
            self.actualResultStep5,
            "Unit validation errors."
        )

        # Step 6 - Create: Fill the price field with incorrect data.(Shorter than 0 or longer than 99999999)

        print(
            "Step 6: (Create) Fill the price field with incorrect data.(Shorter than 0 or longer than 99999999)"
        )

        self.fillFieldsAndClickButton("Product 2", "Product 2 description", "1", "kg", "-99999", 1)
        self.actualResultStep6 = dict(
            invalidPrice=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )
        self.assertEqual(
            self.expected["step6"],
            self.actualResultStep6,
            "Price validation errors."
        )

        # Step 7 - Create: Fill the brand field with incorrect data.(When brand is not selected)

        print(
            "Step 7: (Create) Fill the brand field with incorrect data.(When brand is not selected)"
        )

        self.fillFieldsAndClickButton("Product 2", "Product 2 description", "1", "kg", "158", 0)
        self.actualResultStep7 = dict(
            invalidBrand=self.browser.find_element(By.XPATH, "//span[contains(@class, 'text-danger')]").text,
        )
        self.assertEqual(
            self.expected["step7"],
            self.actualResultStep7,
            "Brand validation errors."
        )

        # Step 8 - Create: Add a new product with correct data and see success message.

        print(
            "Step 8: (Create) Add a new product with correct data and see success message."
        )

        self.fillFieldsAndClickButton("Product Test", "Product Test description", "1", "kg", "158", 1)
        self.actualResultStep8 = dict(
            success=self.browser.find_element(By.XPATH, "//div[contains(@class, 'alert')]").text,
        )

        self.assertEqual(
            self.expected["step8"],
            self.actualResultStep8,
            "Product created successfully."
        )

        # Step 9 - Create: Control if the product is added to the list.
        self.actualResultStep9 = dict(
            name=self.browser.find_element(By.XPATH, "//td[contains(text(), 'Product Test')]").text,
            description=self.browser.find_element(By.XPATH, "//td[contains(text(), 'Product Test description')]").text,
            amount=self.browser.find_element(By.XPATH, "//td[contains(text(), '1')]").text,
            unit=self.browser.find_element(By.XPATH, "//td[contains(text(), 'kg')]").text,
            price=self.browser.find_element(By.XPATH, "//td[contains(text(), '158')]").text,
            brand=self.browser.find_element(By.XPATH, "//td[contains(text(), 'Samsung')]").text,
        )

        self.assertEqual(
            self.expected["step9"],
            self.actualResultStep9,
            "Product added to the list."
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
        Select(self.browser.find_element(By.XPATH, "//select[@automation-id='product-brand']")).select_by_index(indexBrand)
        self.getAndClickButton()