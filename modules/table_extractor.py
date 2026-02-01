#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
表名提取模块
从 XML 文件、注解和 Java 文件中提取表名信息
"""

import os
from .extractors.extractor_manager import ExtractorManager


class TableExtractor:
    """表名提取器"""
    
    def __init__(self):
        """初始化表名提取器"""
        # 初始化提取器管理器
        self.extractor_manager = ExtractorManager()
        # 初始化统计计数器
        self.reset_counters()
    
    def reset_counters(self):
        """重置统计计数器"""
        self.total_files = 0
        self.processed_files = 0
        self.failed_files = 0
    
    def extract_from_files(self, files):
        """
        从文件列表中提取表名
        :param files: 文件列表
        :return: 表信息列表
        """
        table_info_list = []
        
        # 重置计数器
        self.reset_counters()
        self.extractor_manager.reset_counters()
        self.total_files = len(files)
        
        print(f"   开始处理 {self.total_files} 个文件...")
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # 使用提取器管理器提取表名
                table_info = self.extractor_manager.extract_from_file(file_path, content)
                table_info_list.extend(table_info)
                self.processed_files += 1
            except Exception as e:
                print(f"处理文件 {file_path} 时出错: {e}")
                self.failed_files += 1
        
        # 打印提取统计信息
        self._print_extraction_stats()
        
        return table_info_list
    
    def _print_extraction_stats(self):
        """
        打印提取统计信息
        """
        print(f"   - 总文件数: {self.total_files}")
        print(f"   - 成功处理: {self.processed_files}")
        print(f"   - 处理失败: {self.failed_files}")
        # 使用提取器管理器打印详细统计
        self.extractor_manager.print_statistics()
