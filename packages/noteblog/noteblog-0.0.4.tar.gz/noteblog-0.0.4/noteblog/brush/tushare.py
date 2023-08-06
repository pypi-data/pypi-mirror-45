import random
import re
from time import sleep

from noteblog.brush.TempEmail import TempEmail
from splinter.browser import Browser


def local_debug(msg):
    print(str(msg))


def get_random_str():
    random_str = str(random.randint(1000000, 9999999))
    return random_str


class ProcessOn:
    def __init__(self, url):
        try:
            self.email = TempEmail()
            self.driver_name = 'chrome'
            self.executable_path = '/usr/local/bin/chromedriver'

            self.driver = Browser(driver_name=self.driver_name, executable_path=self.executable_path)
            self.driver.driver.set_window_size(800, 800)
            self.driver.visit(url)
            self.driver.cookies.delete("processon_userKey")
            self.driver.find_by_text(u"注 册").first.click()
            sleep(1)
            if self.driver.url == 'https://tushare.pro/register':
                return

        except Exception as e:
            print(e)
            self.driver.quit()

    def signup(self):
        try:
            self.driver.fill("account", self.email.get_email_address())
            self.driver.fill("password", get_random_str())

            while True:
                if self.driver.is_text_not_present(u'秒', 1):
                    local_debug("还没发送验证码，等待...")
                    sleep(1)
                else:
                    local_debug("已发送验证码")
                    break

        except Exception as e:
            print(e)
            self.driver.quit()

    def getSecurityCode(self):
        try:
            self.email.check_received_email()

            info = self.email.get_email_content()
            local_debug(info)

            pat = "验证码([0-9]{6})"
            m = re.search(pat, info)

            return m.group(1)
        except Exception as e:
            print(e)
            return "000000"

    def input_code(self):
        try:
            code = self.getSecurityCode()

            self.driver.fill("verify_code", code)
            sleep(1)
            self.driver.find_by_id("register-btn").first.click()

        except Exception as e:
            print(e)

    def check_success(self):
        while self.driver.is_text_not_present(u"没有账号？"):
            local_debug("等待注册完成")
            sleep(2)

    def clear(self):
        self.driver.cookies.delete()
        self.driver.quit()


def runlop(url):
    processOn = ProcessOn(url)

    processOn.signup()

    processOn.input_code()

    processOn.check_success()

    processOn.clear()
    sleep(1)
    print("\r【OK】")


if __name__ == '__main__':
    pass

    url = "https://tushare.pro/register?reg=233807"
    try:
        runlop(url)
    except Exception as e:
        print(e)
        print("================end================")
