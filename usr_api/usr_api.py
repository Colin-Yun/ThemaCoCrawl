from selenium import webdriver

'''************************************************
* @Function Name : set_chrome_opt
************************************************'''
def set_chrome_opt(opt1):
    opt = webdriver.ChromeOptions()

    # OPT1 : VISIBLE or INVISBLE
    if opt1 == 1:           #INVISIBLE
        opt.add_argument('headless')
        opt.add_argument('disable-gpu')
    else:
        pass

    return opt