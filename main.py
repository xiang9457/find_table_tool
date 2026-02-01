#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目表结构分析工具
根据用户提供的项目地址，自动检索并提取项目中的数据库表信息，最终生成"项目汇总.xlsx"文件
"""

import os
import sys
import time
from modules.file_scanner import FileScanner
from modules.table_extractor import TableExtractor
from modules.schema_analyzer import SchemaAnalyzer
from modules.excel_generator import ExcelGenerator

def main():
    """主程序入口"""
    print("=== 项目表结构分析工具 ===")
    print()
    
    try:
        # 获取用户输入的项目地址
        project_path = input("请输入项目地址: ").strip()
        
        # 验证项目路径是否存在
        if not project_path:
            print("错误: 项目路径不能为空")
            return
        
        if not os.path.exists(project_path):
            print(f"错误: 项目路径 '{project_path}' 不存在")
            return
        
        # 创建输出目录
        output_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\n开始分析项目: {project_path}")
        print(f"输出目录: {output_dir}")
        print("=" * 60)
        
        # 1. 文件扫描
        print("\n1. 正在扫描项目文件...")
        scanner = FileScanner(project_path)
        files = scanner.scan()
        print(f"   扫描完成，找到 {len(files)} 个文件")
        
        if not files:
            print("   警告: 未找到任何文件，请检查项目路径是否正确")
            return
        
        # 2. 表名提取
        print("\n2. 正在提取表名...")
        extractor = TableExtractor()
        table_info_list = extractor.extract_from_files(files)
        print(f"   提取完成，找到 {len(table_info_list)} 条表信息")
        
        if not table_info_list:
            print("   警告: 未提取到任何表信息，请检查项目中是否存在数据库操作相关文件")
            return
        
        # 3. Schema 归属分析
        print("\n3. 正在分析 Schema 归属...")
        analyzer = SchemaAnalyzer()
        table_info_list = analyzer.analyze_schema(table_info_list, files)
        print("   Schema 分析完成")
        
        # 4. 生成 Excel 文件
        print("\n4. 正在生成 Excel 文件...")
        excel_path = os.path.join(output_dir, "项目汇总.xlsx")
        generator = ExcelGenerator(excel_path)
        generator.generate(table_info_list)
        
        # 5. 后续处理
        print("\n5. 后续处理...")
        print("Excel 文件生成完成，无需清理中间数据")
        
        print("\n=== 任务完成 ===")
    except KeyboardInterrupt:
        print("\n用户中断操作，程序退出")
        return
    except Exception as e:
        print(f"\n程序运行出错: {e}")
        import traceback
        traceback.print_exc()
        return

if __name__ == "__main__":
    main()
