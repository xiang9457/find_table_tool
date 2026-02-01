#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础提取器接口
"""

from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    """
    基础提取器接口
    所有具体的提取器都需要实现这个接口
    """
    
    def __init__(self):
        """
        初始化提取器
        """
        self.counter = 0
        # 存储被过滤的表名信息
        self.filtered_tables = []
    
    @abstractmethod
    def extract(self, file_path, content):
        """
        从文件内容中提取表名
        :param file_path: 文件路径
        :param content: 文件内容
        :return: 表信息列表
        """
        pass
    
    def get_counter(self):
        """
        获取提取计数器
        :return: 提取数量
        """
        return self.counter
    
    def reset_counter(self):
        """
        重置提取计数器
        """
        self.counter = 0
    
    def reset_filtered_tables(self):
        """
        重置被过滤的表名信息
        """
        self.filtered_tables = []
    
    def get_filtered_tables(self):
        """
        获取被过滤的表名信息
        :return: 被过滤的表名信息列表
        """
        return self.filtered_tables
