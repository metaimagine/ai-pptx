# -*- coding: utf-8 -*-
"""
@Time    : 2024/3/28 16:24
@Author  : minglang.wu
@Email   : minglang.wu@tenclass.com
@File    : ppt_tools.py
@Desc    :
"""
import os
import time

import pythoncom
import win32com.client


def recreate_slide_by_win32(ppt_path: str, save_path: str, indexs: list):
    ppt_instance, prs = None, None
    try:
        # Avoid the error of "CoInitialize has not been called"
        pythoncom.CoInitialize()
        ppt_instance = win32com.client.Dispatch('PowerPoint.Application')
        # open the powerpoint presentation headless in background
        read_only = True
        has_title = False
        window = False
        try:
            prs = ppt_instance.Presentations.open(os.path.join(os.getcwd(), ppt_path),
                                                  read_only, has_title, window)
            # Record the count of template slides
            count = prs.Slides.Count
            print("当前页面数量：", prs.Slides.Count, count)
            # Copy and paste the target slides
            for index in indexs:
                prs.Slides(index + 1).Copy()
                prs.Slides.Paste()  # Index=insert_index, 不填则默认在最后插入
                print("当前页面数量：", prs.Slides.Count, count)
                time.sleep(0.3)  # 防止复制过快导致丢失

            # Delete template slides
            for _ in range(count):
                prs.Slides(1).Delete()
            prs.SaveAs(os.path.join(os.getcwd(), save_path))
        finally:
            if prs:
                prs.Close()
    finally:
        if ppt_instance:
            ppt_instance.Quit()
            del ppt_instance
        pythoncom.CoUninitialize()