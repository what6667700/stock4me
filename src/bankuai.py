# # '''获取行业板块数据'''
# # -*- coding: utf-8 -*-
#
#
# def getIndustrySection():
#     __logger.debug("开始:收集行业板块数据")
#     try:
#         dbOperator = DBOperator()
#         dbOperator.connDB()
#         table = __stockTables['section']
#         date = getNowdate()
#         for code in range(1, 100):
#             code = '012%03d' % code
#             if isStockSectionExitsInDate(table, code, date, dbOperator):
#                 dataUrl = "http://…………fi_quote_navi_bar&id=bd_ind#mod=list&id=bd%s" % code
#                 getStockSectionDetail(code, dataUrl, dbOperator)
#
#     except Exception as err:
#         __logger.error(">>>>>> Exception: " + str(code) + " " + str(err))
#     finally:
#         dbOperator.closeDB()
#     __logger.debug("结束:收集行业板块数据")
#
#
# def getDataFromUrl(dataUrl):
#     try:
#         browser = webdriver.Firefox()
#         browser.get(dataUrl)
#         time.sleep(2)
#         codes = []
#         pages = [1, ]
#         pageTotalNum = 1
#
#         listFoot = browser.find_element_by_class_name("list-foot")
#         pageTags = listFoot.find_elements_by_tag_name("a")
#         pageTotalNum = len(pageTags) - 2
#
#         for i in range(1, pageTotalNum):
#             element = browser.find_element_by_xpath("//ul[contains(@id,'list-body')]")
#             codeElements = element.find_elements_by_tag_name("li")
#             for codeElement in codeElements:
#                 codes.append(codeElement.get_attribute("id")[-6:])
#
#             listFoot = browser.find_element_by_class_name("list-foot")
#             pageTags = listFoot.find_elements_by_tag_name("a")
#             nextPage = i + 1
#             if i < pageTotalNum and not nextPage in pages:
#                 pageTags[nextPage].click()
#                 pages.append(nextPage)
#                 time.sleep(2)
#         print
#         codes
#     except NoSuchElementException as err:
#         __logger.error(">>>>>> Exception:  " + str(err))
#         return None
#     except TimeoutException as err:
#         __logger.error(">>>>>> Exception:  " + str(err))
#         return None
#     except Exception as err:
#         __logger.error(">>>>>> Exception:  " + str(err))
#         return None
#     finally:
#         browser.close()
#
#     return codes
#
#
# '''获取板块交易信息明细'''
#
#
# def getStockSectionDetail(sectionCode, dataUrl, dbOperator):
#     stockCodes = getDataFromUrl(dataUrl)
#
#     if stockCodes == None and len(stockCodes) == 0:
#         return False
#
#     stockQuotation = {}
#     date = getNowDate()
#     for stockCode in stockCodes:
