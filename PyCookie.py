import http.cookiejar
import urllib.request, urllib.parse

ID_USERNAME = 'id_username'
ID_PASSWORD = 'id_password'
USERNAME = 'you@email.com'
PASSWORD = 'mypassword'
LOGIN_URL = 'https://bitbucket.org/account/signin/?next=/'
NORMAL_URL = 'https://bitbucket.org/'

def extract_cookie_info():
    cj = http.cookiejar.CookieJar()
    login_data = urllib.parse.urlencode({ID_USERNAME: USERNAME,
                                         ID_PASSWORD: PASSWORD}).encode("utf-8")
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    resp = opener.open(LOGIN_URL, login_data)
    for cookie in cj:
        print("----First time cookie: %s --> %s" % (cookie.name, cookie.value))
    print("Headers: %s" % resp.headers)

    resp = opener.open(NORMAL_URL)
    for cookie in cj:
        print("++++Second time cookie: %s --> %s" % (cookie.name, cookie.value))
    print("Headers: %s" % resp.headers)


if __name__ == '__main__':
    extract_cookie_info()