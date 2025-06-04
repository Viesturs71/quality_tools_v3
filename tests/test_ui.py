# tests/test_ui.py

import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class UITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_admin_index_redirects_to_login(self):
        self.driver.get("http://localhost:8000/admin/")
        # without login, index should redirect to the login URL
        self.assertIn("/admin/login/", self.driver.current_url)

    def test_page_title_includes_custom_site_title(self):
        # verify custom site title in both index-redirect and login pages
        for url in ["http://localhost:8000/admin/", "http://localhost:8000/admin/login/"]:
            self.driver.get(url)
            title = self.driver.title
            self.assertIn("Management System Tools Admin", title)

    def test_login_page_shows_branding_h1(self):
        self.driver.get("http://localhost:8000/admin/login/")
        # your login page now shows only the branding <h1>
        h1_texts = [h.text for h in self.driver.find_elements("tag name", "h1")]
        self.assertIn("Management System Tools", h1_texts)

if __name__ == "__main__":
    unittest.main()
