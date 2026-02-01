#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件扫描模块
扫描项目中的目标文件，包括包含注解的文件和 XML 文件
"""

import os
import glob

class FileScanner:
    """文件扫描器"""
    
    def __init__(self, project_path):
        """
        初始化文件扫描器
        :param project_path: 项目路径
        """
        self.project_path = project_path
    
    def scan(self):
        """
        扫描项目文件
        :return: 扫描到的文件列表
        """
        files = []
        
        print(f"   正在扫描项目: {self.project_path}")
        
        # 扫描所有名为 main 的文件夹，无论层级
        main_dirs = glob.glob(os.path.join(self.project_path, "**", "main"), recursive=True)
        print(f"   找到 {len(main_dirs)} 个 main 文件夹")
        
        # 对每个 main 目录进行扫描
        for main_dir in main_dirs:
            if os.path.exists(main_dir) and os.path.isdir(main_dir):
                print(f"   正在扫描目录: {main_dir}")
                # 扫描 Java 文件
                java_files = glob.glob(os.path.join(main_dir, "**", "*.java"), recursive=True)
                print(f"      找到 {len(java_files)} 个 Java 文件")
                files.extend(java_files)
                
                # 扫描 XML 文件
                xml_files = glob.glob(os.path.join(main_dir, "**", "*.xml"), recursive=True)
                print(f"      找到 {len(xml_files)} 个 XML 文件")
                files.extend(xml_files)
        
        # 如果仍然没有找到文件，尝试在项目根目录直接查找
        if not files:
            print("   尝试在项目根目录直接查找文件...")
            # 直接在项目根目录扫描 Java 文件
            java_files = glob.glob(os.path.join(self.project_path, "**", "*.java"), recursive=True)
            print(f"      找到 {len(java_files)} 个 Java 文件")
            files.extend(java_files)
            
            # 直接在项目根目录扫描 XML 文件
            xml_files = glob.glob(os.path.join(self.project_path, "**", "*.xml"), recursive=True)
            print(f"      找到 {len(xml_files)} 个 XML 文件")
            files.extend(xml_files)
        
        # 去重并返回
        unique_files = list(set(files))
        print(f"   扫描完成，共找到 {len(unique_files)} 个文件")
        return unique_files
