#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQL注解提取器
从Java文件中提取@Select、@Insert、@Update、@Delete注解中的表名
"""

import re
import os
from .base_extractor import BaseExtractor


class SQLAnnotationExtractor(BaseExtractor):
    """
    SQL注解提取器
    从Java文件中提取@Select、@Insert、@Update、@Delete注解中的表名
    """
    
    def __init__(self):
        """
        初始化SQL注解提取器
        """
        super().__init__()
        self.table_keywords = ['FROM', 'JOIN', 'INTO', 'UPDATE', 'TABLE']
        self.annotation_keywords = ['@Select', '@Insert', '@Update', '@Delete']
        # 分别统计不同注解的数量
        self.annotation_counters = {
            'Select': 0,
            'Insert': 0,
            'Update': 0,
            'Delete': 0
        }
    
    def extract(self, file_path, content):
        """
        从Java文件中提取SQL注解中的表名
        :param file_path: 文件路径
        :param content: 文件内容
        :return: 表信息列表
        """
        table_info = []
        
        try:
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                try:
                    # 处理SQL注解
                    for keyword in self.annotation_keywords:
                        if keyword in line:
                            try:
                                sql = None
                                
                                # 1. 尝试匹配直接的SQL字符串
                                direct_patterns = [
                                    keyword + r'\s*\(\s*["\']([^"\']*)["\']',  # @Select("SQL")
                                    keyword + r'\s*\(\s*value\s*=\s*["\']([^"\']*)["\']',  # @Select(value="SQL")
                                    keyword + r'\s*\(\s*"([^"]*)"',  # @Select("SQL") 不带 value
                                    keyword + r"\s*\(\s*'([^']*)'"  # @Select('SQL') 单引号
                                ]
                                
                                for pattern in direct_patterns:
                                    match = re.search(pattern, line, re.DOTALL)
                                    if match:
                                        sql = match.group(1)
                                        break
                                
                                # 2. 尝试匹配变量引用
                                if not sql:
                                    var_pattern = keyword + r'\s*\(\s*([^)]+)\)'
                                    match = re.search(var_pattern, line)
                                    if match:
                                        var_name = match.group(1).strip()
                                        # 尝试从当前文件中查找变量定义
                                        sql_var = self._extract_table_name_from_variable(content, var_name)
                                        if sql_var:
                                            sql = sql_var
                                
                                if sql:
                                    # 从 SQL 中提取表名
                                    annotation_table_count = 0
                                    
                                    # 1. 匹配直接表名
                                    for table_keyword in self.table_keywords:
                                        # 匹配直接表名
                                        direct_pattern = r'\b' + table_keyword + r'\b\s+([\w\.]+)'
                                        try:
                                            table_matches = re.finditer(direct_pattern, sql, re.IGNORECASE)
                                            if table_matches:
                                                for table_match in table_matches:
                                                    table_name = table_match.group(1)
                                                    # 过滤掉变量形式的表名
                                                    if not table_name.startswith('${') and not table_name.startswith('#{'):
                                                        table_info.append({
                                                            'source': keyword,
                                                            'table_name': table_name,
                                                            'file_name': os.path.basename(file_path),
                                                            'line_num': line_num
                                                        })
                                                        annotation_table_count += 1
                                                        self.counter += 1
                                                    else:
                                                        # 记录被过滤的表名信息
                                                        filter_reasons = []
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
                                            # 忽略错误，继续处理其他关键字
                                            pass
                                    
                                    # 2. 解析变量获取表名
                                    try:
                                        variable_pattern = r'\$\{([^}]+)\}'
                                        variable_matches = re.finditer(variable_pattern, sql)
                                        if variable_matches:
                                            for var_match in variable_matches:
                                                var_name = var_match.group(1)
                                                # 尝试从当前文件中查找变量定义
                                                table_name = self._extract_table_name_from_variable(content, var_name)
                                                if table_name:
                                                    table_info.append({
                                                        'source': keyword,
                                                        'table_name': table_name,
                                                        'file_name': os.path.basename(file_path),
                                                        'line_num': line_num
                                                    })
                                                    annotation_table_count += 1
                                                    self.counter += 1
                                    except Exception as e:
                                        # 忽略错误，继续处理其他部分
                                        pass
                                    
                                    # 3. 对于 @Insert 注解，尝试从 INTO 关键字提取表名
                                    if keyword == '@Insert' and 'INTO' in sql:
                                        try:
                                            insert_pattern = r'INTO\s+([\w\.]+)'
                                            insert_matches = re.finditer(insert_pattern, sql, re.IGNORECASE)
                                            if insert_matches:
                                                for insert_match in insert_matches:
                                                    table_name = insert_match.group(1)
                                                    if not table_name.startswith('${') and not table_name.startswith('#{'):
                                                        table_info.append({
                                                            'source': keyword,
                                                            'table_name': table_name,
                                                            'file_name': os.path.basename(file_path),
                                                            'line_num': line_num
                                                        })
                                                        annotation_table_count += 1
                                                        self.counter += 1
                                        except Exception as e:
                                            # 忽略错误，继续处理其他部分
                                            pass
                                    
                                    # 更新注解计数器
                                    if annotation_table_count > 0:
                                        annotation_type = keyword[1:]  # 去掉 @ 符号
                                        if annotation_type in self.annotation_counters:
                                            self.annotation_counters[annotation_type] += annotation_table_count
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
    
    def _extract_table_name_from_variable(self, content, var_name):
        """
        从变量定义中提取表名
        :param content: 文件内容
        :param var_name: 变量名
        :return: 表名或 None
        """
        try:
            # 尝试匹配变量定义
            var_pattern = r'\b' + re.escape(var_name) + r'\s*=\s*["\']([^"\']+)["\']'
            match = re.search(var_pattern, content)
            if match:
                table_name = match.group(1)
                return table_name
        except Exception as e:
            # 忽略错误，返回 None
            pass
        return None
    
    def get_annotation_counters(self):
        """
        获取不同注解的计数器
        :return: 注解计数器字典
        """
        return self.annotation_counters
