#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Java SQL提取器
从Java文件中提取SQL语句中的表名，类似于XML文件的处理方式
"""

import re
import os
from .base_extractor import BaseExtractor


class JavaSQLExtractor(BaseExtractor):
    """
    Java SQL提取器
    从Java文件中提取SQL语句中的表名
    """
    
    def __init__(self):
        """
        初始化Java SQL提取器
        """
        super().__init__()
        self.table_keywords = ['FROM', 'JOIN', 'INTO', 'UPDATE', 'TABLE']
    
    def extract(self, file_path, content):
        """
        从Java文件中提取SQL语句中的表名
        :param file_path: 文件路径
        :param content: 文件内容
        :return: 表信息列表
        """
        table_info = []
        
        try:
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                try:
                    # 检查是否包含SQL关键字
                    has_sql_keyword = any(keyword in line.upper() for keyword in self.table_keywords)
                    # 检查是否可能是SQL语句（包含引号或SQL关键字）
                    is_sql_line = has_sql_keyword or ('"' in line and 'SELECT' in line.upper()) or ('"' in line and 'INSERT' in line.upper()) or ('"' in line and 'UPDATE' in line.upper()) or ('"' in line and 'DELETE' in line.upper())
                    
                    if is_sql_line:
                        # 提取关键字后的表名
                        for keyword in self.table_keywords:
                            # 使用正则表达式匹配关键字后的表名，支持更复杂的情况
                            pattern = r'\b' + keyword + r'\b\s+([\w\.]+(?:\s*\.[\w]+)*)'
                            matches = re.finditer(pattern, line, re.IGNORECASE)
                            
                            for match in matches:
                                table_name = match.group(1).strip()
                                # 过滤掉空表名和无效表名
                                if table_name and not table_name.startswith('${') and not table_name.startswith('#{'):
                                    table_info.append({
                                        'source': 'Java SQL',
                                        'table_name': table_name,
                                        'file_name': os.path.basename(file_path),
                                        'line_num': line_num
                                    })
                                    self.counter += 1
                                else:
                                    # 记录被过滤的表名信息
                                    filter_reasons = []
                                    if not table_name:
                                        filter_reasons.append('空表名')
                                    if table_name.startswith('${') or table_name.startswith('#{'):
                                        filter_reasons.append('包含变量形式')
                                    if filter_reasons:
                                        self.filtered_tables.append({
                                            'table_name': table_name,
                                            'file_name': os.path.basename(file_path),
                                            'line_num': line_num,
                                            'filter_reasons': filter_reasons
                                        })
                except Exception as e:
                    # 忽略错误，继续处理下一行
                    pass
        except Exception as e:
            # 忽略错误，返回已提取的表信息
            pass
        
        return table_info
