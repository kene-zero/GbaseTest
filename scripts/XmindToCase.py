#!/bin/python3
# -*- coding:utf-8 -*-

import xmind
import os
from xmindparser import xmind_to_dict
from openpyxl import Workbook


class XmindToCase(object):

    def __init__(self):

        self.root_path = os.path.dirname(os.path.dirname(__file__))
        self.files_path = os.path.join(self.root_path, "files")
        self.xmind_path = "D:\\File\\测试文件\\功能测试\\测试设计"
        self.testCase_path = "D:\\File\\测试文件\\功能测试\\测试用例"
        self.xmind_dict_list = []
        self.func_name_list = []

    def xmind_to_dict(self):
        xmind_file_list = os.listdir(self.xmind_path)
        for xmind_file in xmind_file_list:
            xmind_dict = xmind_to_dict(os.path.join(self.xmind_path, xmind_file))
            self.xmind_dict_list.append(xmind_dict)
            self.func_name_list.append(xmind_file[0:-6])

    def dict_to_case(self, xmind_dict):
        case_list = []
        types = xmind_dict[0]['topic']["topics"]
        print(xmind_dict[0]['topic']["title"])
        for t1 in types:
            if t1['title'] == "需求说明":
                func_number = t1['topics'][0]['topics'][0]["title"]
            if t1['title'] == '功能性':
                case_dict = t1['topics']
                for func in case_dict:
                    for test_type in func["topics"]:
                        for test_title in test_type["topics"]:
                            steps = []
                            expect = []
                            for step in test_title["topics"]:
                                steps.append(step["title"])
                                expect.append(step["topics"][0]['title'])
                            case = {"test_func": func['title'],
                                    "test_type": test_type['title'],
                                    "test_title": test_title["title"],
                                    "test_step": steps,
                                    'test_expect': expect}
                            case_list.append(case)
        return case_list

    def generate_excel(self):
        wb = Workbook()
        self.xmind_to_dict()
        index = 0
        for xmind_dict, func_name in zip(self.xmind_dict_list, self.func_name_list):
            case_list = self.dict_to_case(xmind_dict)
            wb.create_sheet(index=index, title=func_name)
            index += 1
            sheet = wb[func_name]
            num = 1
            sheet[f'A{str(num)}'] = "Test linkID"
            sheet[f'B{str(num)}'] = "用例编号"
            sheet[f'C{str(num)}'] = "测试功能"
            sheet[f'D{str(num)}'] = "测试类别"
            sheet[f'E{str(num)}'] = "测试标题"
            sheet[f'F{str(num)}'] = "测试环境"
            sheet[f'G{str(num)}'] = "前置条件"
            sheet[f'H{str(num)}'] = "测试步骤"
            sheet[f'I{str(num)}'] = "检查项"
            sheet[f'J{str(num)}'] = "优先级"
            sheet[f'K{str(num)}'] = "是否自动化"
            sheet[f'L{str(num)}'] = "用例作者"
            for case in case_list:
                num += 1
                sheet[f'A{str(num)}'] = " "
                sheet[f'B{str(num)}'] = "test_demands_"
                sheet[f'C{str(num)}'] = case["test_func"]
                sheet[f'D{str(num)}'] = case["test_type"]
                sheet[f'E{str(num)}'] = case["test_title"]
                sheet[f'F{str(num)}'] = "分布式数据库集群"
                sheet[f'G{str(num)}'] = """1.集群已部署
2.集群状态正常"""
                step = ""
                expect = ''
                n = 1
                for s, e in zip(case["test_step"], case["test_expect"]):
                    s_f = "步骤" + str(n) + ': ' + s + '\r\n'
                    e_f = "步骤" + str(n) + ': ' + e + '\r\n'
                    step += s_f
                    expect += e_f
                    n += 1
                sheet[f'H{str(num)}'] = step
                sheet[f'I{str(num)}'] = expect
                sheet[f'J{str(num)}'] = "★★★"
                sheet[f'K{str(num)}'] = "否"
                sheet[f'L{str(num)}'] = "shishaohua"
            excel_file_path = os.path.join("D:\\File\\测试文件\\功能测试\\测试用例\\迭代一测试用例.xlsx")
            wb.save(excel_file_path)


if __name__ == '__main__':
    tool = XmindToCase()
    tool.xmind_to_dict()
    tool.generate_excel()
