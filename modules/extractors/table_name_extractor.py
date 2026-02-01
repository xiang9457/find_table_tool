#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TableName注解提取器
从Java文件中提取@TableName注解中的表名
"""

import re
import os
from .base_extractor import BaseExtractor


class TableNameExtractor(BaseExtractor):
    """
    TableName注解提取器
    从Java文件中提取@TableName注解中的表名
    """
    
    def __init__(self):
        """
        初始化TableName提取器
        """
        super().__init__()
    
    def extract(self, file_path, content):
        """
        从Java文件中提取@TableName注解中的表名
        :param file_path: 文件路径
        :param content: 文件内容
        :return: 表信息列表
        """
        table_info = []
        
        try:
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                try:
                    # 处理 @TableName 注解
                    if '@TableName' in line:
                        try:
                            pattern = r'@TableName\s*\(\s*value\s*=\s*["\']([^"\']+)["\']'
                            match = re.search(pattern, line)
                            if match:
                                table_name = match.group(1)
                                table_info.append({
                                    'source': '@TableName',
                                    'table_name': table_name,
                                    'file_name': os.path.basename(file_path),
                                    'line_num': line_num
                                })
                                self.counter += 1
                            else:
                                # 尝试匹配不带 value 的形式
                                pattern = r'@TableName\s*\(\s*["\']([^"\']+)["\']'
                                match = re.search(pattern, line)
                                if match:
                                    table_name = match.group(1)
                                    table_info.append({
                                        'source': '@TableName',
                                        'table_name': table_name,
                                        'file_name': os.path.basename(file_path),
                                        'line_num': line_num
                                    })
                                    self.counter += 1
                        except Exception as e:
                            # 忽略错误，继续处理其他注解
                            pass
                except Exception as e:
                    # 忽略错误，继续处理下一行
                    pass
        except Exception as e:
            # 忽略错误，返回已提取的表信息
            pass
        
        return table_info
