from selenium import webdriver
from selenium.webdriver.common.by import By
import time

work = True
i = 0

def configure_url():
    """"Proxy configuration"""
    # main url
    main_url = 'https://hidemy.name/ua/proxy-list/'
    # proxy speed
    proxy_speed = f'?maxtime={input("Enter proxy speed: ")}'
    if proxy_speed == '0':
        proxy_speed = int('')
    elif proxy_speed == '\n':
        proxy_speed = int('')
    # proxy anonimity
    proxy_anon_input = input('Anonimity lvl (0-3) or (all) :')
    if proxy_anon_input == '0':
        proxy_anon = '&anon=1'
    elif proxy_anon_input == '1':
        proxy_anon = '&anon=2'
    elif proxy_anon_input == '2':
        proxy_anon = '&anon=3'
    elif proxy_anon_input == '3':
        proxy_anon = '&anon=4'
    elif proxy_anon_input == 'all':
        proxy_anon = ''
    else:
        print('Invalid input')
        quit()
        return
    # proxy type
    proxy_type_input = input('Type (h) for http, (hs) for https, (4) for socks4, (5) for socks5 or (all):')
    if proxy_type_input == 'h':
        proxy_type = '&type=h'
    elif proxy_type_input == 'hs':
        proxy_type = '&type=s'
    elif proxy_type_input == '4':
        proxy_type = '&type=4'
    elif proxy_type_input == '5':
        proxy_type = '&type=5'
    elif proxy_anon_input == 'all':
        proxy_type = ''
    else:
        print('Invalid input')
        return
    all_url = main_url + proxy_speed + proxy_type + proxy_anon + '#list'
    print("-" * 100)
    print(all_url)
    return all_url


def next_page(driver, work):
    """Next page"""
    try:
        if driver.find_element(By.CLASS_NAME, value="next_array").click():
            work = True
    except Exception as ex:
        print(ex)
        print('No more pages')
        work = False
    finally:
        return work


def driver():
    """Setup driver"""
    driver = webdriver.Firefox(executable_path='./geco/geckodriver')
    driver.maximize_window()
    return driver


def parse_page(driver, work, proxy_num):
    ''''Parse data'''
    driver.get(configure_url())
    time.sleep(1)

    # get all proxies
    while work == True:
        try:
            get_proxy = driver.find_elements(By.TAG_NAME, value="tbody")[0].find_elements(By.TAG_NAME, value="tr")[
                proxy_num].find_elements(By.TAG_NAME, value="td")[0].text
            get_port = driver.find_elements(By.TAG_NAME, value="tbody")[0].find_elements(By.TAG_NAME, value="tr")[
                proxy_num].find_elements(By.TAG_NAME, value="td")[1].text

            with open('./proxy/proxies.txt', 'a') as f:
                f.write(get_proxy + ':' + get_port + '\n')
                f.close()

            proxy_num += 1

            if proxy_num == len(driver.find_elements(By.TAG_NAME, value="tbody")[0].find_elements(By.TAG_NAME, value="tr")):
                next_page(driver, work)
                proxy_num = 0
        except Exception as ex:
            print(ex)
            work = False

def main():
    """Main function"""
    parse_page(driver(), work, i)


if __name__ == '__main__':
    main()
