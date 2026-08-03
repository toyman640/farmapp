from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class EventFormSeleniumTests(StaticLiveServerTestCase):
    tests_run = 0
    tests_passed = 0

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Automatically downloads the correct matching driver version when online
        cls.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        cls.browser.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()
        print("\n" + "="*40)
        print(f" TESTS COMPLETED SUMMARY ")
        print(f" Total Tests Run:    {cls.tests_run}")
        print(f" Total Tests Passed: {cls.tests_passed}")
        print("="*40 + "\n")

    def setUp(self):
        EventFormSeleniumTests.tests_run += 1

    def tearDown(self):
        if hasattr(self, '_outcome') and self._outcome.success:
            EventFormSeleniumTests.tests_passed += 1
        elif not hasattr(self, '_outcome'):
            EventFormSeleniumTests.tests_passed += 1

    def test_login_fields_and_event_page(self):
        self.browser.get(f"{self.live_server_url}/skaal-vet-hub/event/create/")
        
        username_field = self.browser.find_element(By.NAME, "username")
        password_field = self.browser.find_element(By.NAME, "password")
        
        self.assertIsNotNone(username_field, "Username field is missing from the login page")
        self.assertIsNotNone(password_field, "Password field is missing from the login page")