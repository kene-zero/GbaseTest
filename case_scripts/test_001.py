import pytest
import allure
from libs import log

log = log.Log().get_logger()


class Test001:
    @allure.story("1111")
    @allure.feature("1111")
    def test01(self):
        log.info("1111")

    @allure.story("1111")
    @allure.feature("1111")
    def test02(self):
        log.info("1111")

    @allure.story("1111")
    @allure.feature("1111")
    def test03(self):
        log.info("1111")


if __name__ == '__main__':
    pytest.main(['--alluredir', 'logs/', 'test_001.py'])
