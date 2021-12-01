import time
import xlsxwriter
from selenium import webdriver

def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    return driver

def get_list(driver):
    driver.get("https://www.google.com/")
    driver.find_element_by_class_name("gLFyf.gsfi").send_keys("top youtube clips")
    driver.find_element_by_class_name("gNO89b").click()
    ml = driver.find_element_by_xpath("//*[@id='rso']/div[1]/div/div[1]/div/div[1]/div/div/div/div/div[1]/div/div[2]/table")

    sl = ml.find_elements_by_tag_name("td")
    sl = sl[:-3]
    return sl

def get_content(driver, sl):
    tl = []
    vl = []
    hl = []
    dl = []

    for i in range(len(sl)):
        if i % 3 == 1:
            tl.append(sl[i].text)
            vl.append(sl[i+1].text+" bills views")

    driver.get("https://www.youtube.com/")
    for el in tl:
        driver.find_element_by_name("search_query").send_keys(el)
        time.sleep(2)
        driver.find_element_by_id("search-icon-legacy").click()
        time.sleep(4)
        v = driver.find_element_by_class_name('yt-simple-endpoint.style-scope.ytd-video-renderer').get_attribute('href')
        hl.append(v)
        d = driver.find_element_by_class_name("yt-simple-endpoint.style-scope.ytd-video-renderer").get_attribute("aria-label")
        el = str(d).split()
        for i in range(len(el)):
            if el[i] in ["лет", "года"]:
                dl.append(el[i-1] + " years ago")
        driver.find_element_by_name("search_query").clear()
    driver.close()
    return tl, vl, hl, dl

def xls(tl, vl, hl, dl):
    workbook = xlsxwriter.Workbook("data.xls")
    worksheet = workbook.add_worksheet()

    for i in range(len(tl)):
        worksheet.write("A" + str(i + 1), tl[i])
        worksheet.write("B" + str(i + 1), vl[i])
        worksheet.write("C" + str(i + 1), dl[i])
        worksheet.write("D" + str(i + 1), hl[i])
    worksheet.set_column(0, 1, 20)
    worksheet.set_column(2, 2, 15)
    worksheet.set_column(3, 3, 50) 
    workbook.close()

def main():
    dr = driver()
    ml = get_list(dr)
    tl, vl, hl, dl = get_content(dr, ml)
    xls(tl, vl, hl, dl)

if __name__ == '__main__':
    main()