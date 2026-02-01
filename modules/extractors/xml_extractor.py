#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XML文件提取器
从XML文件中提取表名
"""

import re
import os
from .base_extractor import BaseExtractor


class XMLExtractor(BaseExtractor):
    """
    XML文件提取器
    从XML文件中提取表名
    """
    
    def __init__(self):
        """
        初始化XML提取器
        """
        super().__init__()
        self.table_keywords = ['FROM', 'JOIN', 'INTO', 'UPDATE', 'TABLE']
    
    def extract(self, file_path, content):
        """
        从XML文件中提取表名
        :param file_path: 文件路径
        :param content: 文件内容
        :return: 表信息列表
        """
        table_info = []
        
        try:
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                try:
                    # 提取关键字后的表名
                    for keyword in self.table_keywords:
                        # 使用正则表达式匹配关键字后的表名，支持更复杂的情况
                        pattern = r'\b' + keyword + r'\b\s+([\w\.]+(?:\s*\.[\w]+)*)'
                        matches = re.finditer(pattern, line, re.IGNORECASE)
                        
                        for match in matches:
                            table_name = match.group(1).strip()
                            # 过滤掉空表名和无效表名
                            if table_name and not table_name.startswith('${'):
                                table_info.append({
                                    'source': 'XML',
                                    'table_name': table_name,
                                    'file_name': os.path.basename(file_path),
                                    'line_num': line_num
                                })
                                self.counter += 1
                except Exception as e:
                    # 忽略错误，继续处理下一行
                    pass
        except Exception as e:
            # 忽略错误，返回已提取的表信息
            pass
        
        return table_info
