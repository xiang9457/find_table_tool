#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取器管理器
管理所有的表名提取器并提供统一的接口
"""

from .xml_extractor import XMLExtractor
from .table_name_extractor import TableNameExtractor
from .sql_annotation_extractor import SQLAnnotationExtractor
from .java_sql_extractor import JavaSQLExtractor


class ExtractorManager:
    """
    提取器管理器
    管理所有的表名提取器并提供统一的接口
    """
    
    def __init__(self):
        """
        初始化提取器管理器
        """
        # 初始化所有提取器
        self.extractors = {
            'xml': XMLExtractor(),
            'table_name': TableNameExtractor(),
            'sql_annotation': SQLAnnotationExtractor(),
            'java_sql': JavaSQLExtractor()
        }
        # 初始化统计信息
        self.reset_counters()
    
    def reset_counters(self):
        """
        重置所有计数器
        """
        for extractor in self.extractors.values():
            extractor.reset_counter()
            extractor.reset_filtered_tables()
        # 重置SQL注解提取器的计数器
        if hasattr(self.extractors['sql_annotation'], 'annotation_counters'):
            self.extractors['sql_annotation'].annotation_counters = {
                'Select': 0,
                'Insert': 0,
                'Update': 0,
                'Delete': 0
            }
    
    def extract_from_file(self, file_path, content):
        """
        从文件中提取表名
        :param file_path: 文件路径
        :param content: 文件内容
        :return: 表信息列表
        """
        table_info = []
        
        # 根据文件类型选择提取器
        if file_path.endswith('.xml'):
            # 使用XML提取器
            table_info.extend(self.extractors['xml'].extract(file_path, content))
        elif file_path.endswith('.java'):
            # 使用Java相关提取器
            table_info.extend(self.extractors['table_name'].extract(file_path, content))
            table_info.extend(self.extractors['sql_annotation'].extract(file_path, content))
            table_info.extend(self.extractors['java_sql'].extract(file_path, content))
        
        return table_info
    
    def get_statistics(self):
        """
        获取提取统计信息
        :return: 统计信息字典
        """
        stats = {
            'XML': self.extractors['xml'].get_counter(),
            'Annotation': 0,
            'TableName': self.extractors['table_name'].get_counter(),
            'Select': 0,
            'Insert': 0,
            'Update': 0,
            'Delete': 0,
            'Java SQL': self.extractors['java_sql'].get_counter()
        }
        
        # 计算注解总数量
        stats['Annotation'] = stats['TableName'] + self.extractors['sql_annotation'].get_counter()
        
        # 获取SQL注解的详细统计
        if hasattr(self.extractors['sql_annotation'], 'get_annotation_counters'):
            sql_stats = self.extractors['sql_annotation'].get_annotation_counters()
            stats['Select'] = sql_stats['Select']
            stats['Insert'] = sql_stats['Insert']
            stats['Update'] = sql_stats['Update']
            stats['Delete'] = sql_stats['Delete']
        
        return stats
    
    def print_statistics(self):
        """
        打印提取统计信息
        """
        stats = self.get_statistics()
        
        print("   提取统计信息:")
        print(f"   - 总提取条数: {sum(stats.values())} 条")
        print(f"   - 提取规则统计:")
        print(f"     * XML 文件: {stats['XML']} 条")
        print(f"     * 注解提取: {stats['Annotation']} 条")
        print(f"       - @TableName: {stats['TableName']} 条")
        print(f"       - @Select: {stats['Select']} 条")
        print(f"       - @Insert: {stats['Insert']} 条")
        print(f"       - @Update: {stats['Update']} 条")
        print(f"       - @Delete: {stats['Delete']} 条")
        print(f"     * Java SQL: {stats['Java SQL']} 条")
        
        # 打印被过滤的表名信息
        total_filtered = 0
        all_filtered_tables = []
        for extractor_name, extractor in self.extractors.items():
            filtered_tables = extractor.get_filtered_tables()
            total_filtered += len(filtered_tables)
            all_filtered_tables.extend(filtered_tables)
        
        if total_filtered > 0:
            print("\n   被过滤的表名信息:")
            print(f"   共过滤掉 {total_filtered} 条表名记录:")
            # 按过滤原因分组统计
            reason_counts = {}
            for filtered in all_filtered_tables:
                for reason in filtered['filter_reasons']:
                    reason_counts[reason] = reason_counts.get(reason, 0) + 1
            # 打印过滤原因统计
            for reason, count in reason_counts.items():
                print(f"     * {reason}: {count} 条")
