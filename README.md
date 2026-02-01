# 项目表结构分析工具说明文档

## 一、使用说明

### 1.1 环境要求

- Python 3.6 或更高版本
- 需要安装的依赖包：
  - `openpyxl`：用于生成 Excel 文件
  - `glob`：用于文件扫描（Python 标准库）

安装依赖：
```bash
pip install openpyxl
```

### 1.2 运行步骤

1. **启动工具**
   - 在命令行中进入工具目录
   - 运行主程序：
     ```bash
     python main.py
     ```

2. **输入项目路径**
   - 程序会提示输入项目地址
   - 输入要分析的项目根目录的绝对路径或相对路径
   - 例如：`D:\data\workspace\my-project`

3. **等待处理完成**
   - 工具会自动执行以下步骤：
     - 扫描项目文件
     - 提取表名信息
     - 分析 Schema 归属
     - 生成 Excel 报告
   - 处理过程中会显示实时进度和统计信息

4. **查看结果**
   - 生成的 Excel 文件位于 `output/项目汇总.xlsx`
   - 包含多个工作表，展示不同维度的表信息

### 1.3 输出说明

工具会在 `output` 目录下生成 `项目汇总.xlsx` 文件，包含以下工作表：

- **Sheet1**：原始表信息（未清洗）
- **Sheet2**：清洗后的表信息（去重、排序、过滤）
- **Sheet3**：去重后表信息（只保留schema和表名）
- **Sheet4**：文件统计信息
- **Sheet5**：处理总结

**日志信息：**
- 工具会在执行过程中打印详细的处理日志
- 生成 Excel 文件完成后，会在日志中打印生成文件的完整路径
- 日志包含各阶段的统计信息和处理结果

### 1.4 注意事项

- 确保项目路径正确且可访问
- 项目中应包含 Java 文件（.java）和 XML 文件（.xml）
- 工具会优先扫描名为 `main` 的目录
- 如果找不到 `main` 目录，会在项目根目录直接扫描

## 二、功能说明

### 2.1 核心功能

#### 2.1.1 文件扫描
- 自动扫描项目中的 Java 文件和 XML 文件
- 支持递归扫描子目录
- 优先扫描 `main` 目录（符合 Maven/Gradle 项目结构）
- 提供详细的扫描统计信息

#### 2.1.2 表名提取
从多种来源提取表名：

1. **XML 文件**
   - 解析 MyBatis XML 映射文件
   - 提取 SQL 语句中的表名
   - 支持复杂的 SQL 语句结构

2. **Java 注解**
   - `@TableName`：实体类注解
   - `@Select`：查询注解
   - `@Insert`：插入注解
   - `@Update`：更新注解
   - `@Delete`：删除注解

3. **Java SQL 语句**
   - 提取 Java 代码中的 SQL 字符串
   - 支持多行 SQL 语句
   - 识别常见的 SQL 关键字

#### 2.1.3 Schema 归属分析
- 通过 `@DS` 注解确定表的 Schema 归属
- 支持类级别和方法级别的注解
- 智能匹配文件名和类名
- 提供默认 Schema（master）

#### 2.1.4 数据清洗
对提取的表信息进行清洗：

1. **过滤规则**
   - 过滤包含中文字符的表名
   - 过滤 SQL 关键字（SELECT、FROM、WHERE 等）
   - 过滤 Java 关键字（class、interface、public 等）
   - 过滤 Oracle 特殊关键字（DUAL、TO）
   - 过滤变量形式的表名（${tableName}）

2. **数据规范化**
   - 仅保留英文字母、数字、下划线和点
   - 统一表名格式

3. **排序规则**
   - 按所有列升序排列
   - 排序优先级：来源 > Schema > 表名 > 文件名 > 行号

#### 2.1.5 统计报告
- 提取统计：按提取规则分类统计
- 过滤统计：记录被过滤的表名及原因
- Schema 统计：按 Schema 分组统计表数量
- 文件统计：记录处理的文件数量和失败情况

### 2.2 技术特性

- **模块化设计**：各功能模块独立，易于维护和扩展
- **错误处理**：完善的异常捕获和错误报告
- **日志记录**：详细的处理过程日志
- **性能优化**：高效的文件扫描和正则匹配

## 三、项目结构说明

### 3.1 目录结构

```
find_table_tool/
├── main.py                          # 主程序入口
├── modules/                         # 核心模块目录
│   ├── __init__.py
│   ├── file_scanner.py              # 文件扫描模块
│   ├── table_extractor.py           # 表名提取模块
│   ├── schema_analyzer.py           # Schema 分析模块
│   ├── excel_generator.py           # Excel 生成模块
│   └── extractors/                  # 提取器目录
│       ├── __init__.py
│       ├── base_extractor.py        # 基础提取器接口
│       ├── extractor_manager.py     # 提取器管理器
│       ├── xml_extractor.py         # XML 文件提取器
│       ├── table_name_extractor.py  # @TableName 注解提取器
│       ├── sql_annotation_extractor.py  # SQL 注解提取器
│       └── java_sql_extractor.py    # Java SQL 提取器
└── output/                          # 输出目录
    └── 项目汇总.xlsx                 # 生成的 Excel 文件
```

### 3.2 模块说明

#### 3.2.1 main.py
- **功能**：主程序入口，协调整个处理流程
- **主要方法**：
  - `main()`：主函数，控制程序执行流程
- **处理流程**：
  1. 获取用户输入的项目路径
  2. 创建输出目录
  3. 扫描项目文件
  4. 提取表名信息
  5. 分析 Schema 归属
  6. 生成 Excel 文件

#### 3.2.2 modules/file_scanner.py
- **功能**：扫描项目中的目标文件
- **主要类**：`FileScanner`
- **主要方法**：
  - `scan()`：扫描项目文件，返回文件列表
- **扫描策略**：
  1. 优先扫描所有 `main` 目录
  2. 在 `main` 目录中查找 `.java` 和 `.xml` 文件
  3. 如果未找到，在项目根目录直接扫描

#### 3.2.3 modules/table_extractor.py
- **功能**：从文件中提取表名信息
- **主要类**：`TableExtractor`
- **主要方法**：
  - `extract_from_files(files)`：从文件列表中提取表名
  - `_print_extraction_stats()`：打印提取统计信息
- **统计信息**：
  - 总文件数
  - 成功处理数
  - 处理失败数
  - 各提取规则的提取数量

#### 3.2.4 modules/schema_analyzer.py
- **功能**：分析表的 Schema 归属关系
- **主要类**：`SchemaAnalyzer`
- **主要方法**：
  - `analyze_schema(table_info_list, files)`：分析 Schema 归属
  - `_extract_ds_annotations(files)`：提取 @DS 注解
  - `_find_schema_for_table(table_info, ds_annotations)`：查找表对应的 Schema
- **分析策略**：
  1. 通过文件名匹配 @DS 注解
  2. 通过类名匹配 @DS 注解
  3. 通过文件路径匹配
  4. 基于表名哈希值分配 Schema
  5. 默认使用 master Schema

#### 3.2.5 modules/excel_generator.py
- **功能**：生成 Excel 报告
- **主要类**：`ExcelGenerator`
- **主要方法**：
  - `generate(table_info_list)`：生成 Excel 文件
  - `_clean_table_info(table_info_list)`：清洗表信息
  - `_create_sheet1()`：创建原始数据表
  - `_create_sheet2()`：创建清洗后数据表
  - `_create_sheet3()`：创建 Schema 统计表
  - `_create_sheet4()`：创建文件统计表
  - `_create_sheet5()`：创建处理总结表
- **清洗规则**：
  - 过滤中文字符
  - 过滤关键字
  - 过滤变量形式
  - 数据规范化
  - 多列排序

#### 3.2.6 modules/extractors/base_extractor.py
- **功能**：定义提取器基础接口
- **主要类**：`BaseExtractor`（抽象类）
- **主要方法**：
  - `extract(file_path, content)`：抽象方法，提取表名
  - `get_counter()`：获取提取计数
  - `reset_counter()`：重置计数器
  - `get_filtered_tables()`：获取被过滤的表名
  - `reset_filtered_tables()`：重置过滤记录

#### 3.2.7 modules/extractors/extractor_manager.py
- **功能**：管理所有提取器
- **主要类**：`ExtractorManager`
- **主要方法**：
  - `extract_from_file(file_path, content)`：从文件中提取表名
  - `get_statistics()`：获取统计信息
  - `print_statistics()`：打印统计信息
  - `reset_counters()`：重置所有计数器
- **管理的提取器**：
  - XML 提取器
  - @TableName 提取器
  - SQL 注解提取器
  - Java SQL 提取器

#### 3.2.8 modules/extractors/xml_extractor.py
- **功能**：从 XML 文件中提取表名
- **主要类**：`XMLExtractor`
- **提取规则**：
  - 匹配 SQL 语句中的表名
  - 支持 FROM、JOIN、INSERT INTO、UPDATE、DELETE FROM 等语句

#### 3.2.9 modules/extractors/table_name_extractor.py
- **功能**：提取 @TableName 注解中的表名
- **主要类**：`TableNameExtractor`
- **提取规则**：
  - 匹配 `@TableName("table_name")` 格式
  - 支持单引号和双引号

#### 3.2.10 modules/extractors/sql_annotation_extractor.py
- **功能**：提取 SQL 注解中的表名
- **主要类**：`SQLAnnotationExtractor`
- **提取规则**：
  - `@Select`：提取 SELECT 语句中的表名
  - `@Insert`：提取 INSERT 语句中的表名
  - `@Update`：提取 UPDATE 语句中的表名
  - `@Delete`：提取 DELETE 语句中的表名

#### 3.2.11 modules/extractors/java_sql_extractor.py
- **功能**：从 Java 代码中提取 SQL 语句中的表名
- **主要类**：`JavaSQLExtractor`
- **提取规则**：
  - 匹配字符串中的 SQL 语句
  - 识别常见的 SQL 关键字

## 四、规则说明

### 4.1 表名提取规则

#### 4.1.1 XML 文件提取规则

**支持的 SQL 语句类型：**

1. **SELECT 语句**
   - 模式：`FROM\s+([a-zA-Z_][a-zA-Z0-9_]*)`
   - 示例：`SELECT * FROM user_table`
   - 提取：`user_table`

2. **JOIN 语句**
   - 模式：`JOIN\s+([a-zA-Z_][a-zA-Z0-9_]*)`
   - 示例：`JOIN order_table ON ...`
   - 提取：`order_table`

3. **INSERT 语句**
   - 模式：`INSERT\s+INTO\s+([a-zA-Z_][a-zA-Z0-9_]*)`
   - 示例：`INSERT INTO user_table (id, name) VALUES (...)`
   - 提取：`user_table`

4. **UPDATE 语句**
   - 模式：`UPDATE\s+([a-zA-Z_][a-zA-Z0-9_]*)`
   - 示例：`UPDATE user_table SET name = '...'`
   - 提取：`user_table`

5. **DELETE 语句**
   - 模式：`DELETE\s+FROM\s+([a-zA-Z_][a-zA-Z0-9_]*)`
   - 示例：`DELETE FROM user_table WHERE id = 1`
   - 提取：`user_table`

**特殊处理：**
- 支持多行 SQL 语句
- 忽略注释中的表名
- 支持表别名（提取实际表名）

#### 4.1.2 Java 注解提取规则

**@TableName 注解：**
- 模式：`@TableName\s*\(\s*["']([^"']+)["']\s*\)`
- 示例：
  ```java
  @TableName("user_table")
  public class User { }
  ```
- 提取：`user_table`

**@Select 注解：**
- 模式：`@Select\s*\(\s*["']([^"']+)["']\s*\)`
- 提取 SQL 语句中的表名（同 XML 规则）
- 示例：
  ```java
  @Select("SELECT * FROM user_table WHERE id = #{id}")
  List<User> findById(Long id);
  ```
- 提取：`user_table`

**@Insert 注解：**
- 模式：`@Insert\s*\(\s*["']([^"']+)["']\s*\)`
- 提取 INSERT 语句中的表名
- 示例：
  ```java
  @Insert("INSERT INTO user_table (name, age) VALUES (#{name}, #{age})")
  void insert(User user);
  ```
- 提取：`user_table`

**@Update 注解：**
- 模式：`@Update\s*\(\s*["']([^"']+)["']\s*\)`
- 提取 UPDATE 语句中的表名
- 示例：
  ```java
  @Update("UPDATE user_table SET name = #{name} WHERE id = #{id}")
  void update(User user);
  ```
- 提取：`user_table`

**@Delete 注解：**
- 模式：`@Delete\s*\(\s*["']([^"']+)["']\s*\)`
- 提取 DELETE 语句中的表名
- 示例：
  ```java
  @Delete("DELETE FROM user_table WHERE id = #{id}")
  void deleteById(Long id);
  ```
- 提取：`user_table`

#### 4.1.3 Java SQL 提取规则

**字符串中的 SQL 语句：**
- 模式：识别包含 SQL 关键字的字符串
- 支持的关键字：SELECT、INSERT、UPDATE、DELETE、FROM、JOIN 等
- 示例：
  ```java
  String sql = "SELECT * FROM user_table WHERE status = 1";
  ```
- 提取：`user_table`

**特殊处理：**
- 支持多行字符串
- 支持字符串拼接
- 忽略注释中的 SQL

### 4.2 Schema 归属规则

#### 4.2.1 @DS 注解识别

**类级别注解：**
```java
@DS("slave")
public class UserMapper {
    // 所有方法使用 slave 数据源
}
```

**方法级别注解：**
```java
public class UserMapper {
    @DS("master")
    public User findById(Long id) {
        // 使用 master 数据源
    }
    
    @DS("slave")
    public List<User> findAll() {
        // 使用 slave 数据源
    }
}
```

#### 4.2.2 Schema 匹配策略

**匹配优先级：**

1. **文件名匹配**
   - 提取文件名（不含扩展名）
   - 在 @DS 注解中查找匹配的类名
   - 示例：`UserMapper.java` → 匹配 `UserMapper` 类

2. **类名匹配**
   - 从文件内容中提取类名
   - 在 @DS 注解中查找匹配
   - 示例：`public class UserMapper` → 匹配 `UserMapper` 类

3. **文件路径匹配**
   - 检查文件路径是否包含 Schema 关键字
   - 示例：包含 `slave` 的路径 → slave Schema

4. **哈希分配**
   - 对表名进行 MD5 哈希
   - 根据哈希值分配 Schema
   - master: 50%, slave: 25%, mdb: 25%

5. **默认 Schema**
   - 如果以上都不匹配，使用默认 Schema：`master`

### 4.3 数据清洗规则

#### 4.3.1 过滤规则

**1. 中文字符过滤**
- 规则：检查表名是否包含中文字符
- 范围：`\u4e00` 到 `\u9fff`
- 示例：
  - `user_table` → 保留
  - `用户表` → 过滤
  - `user_表` → 过滤

**2. SQL 关键字过滤**
- 规则：检查表名是否为 SQL 关键字
- 关键字列表：
  - DDL：CREATE、DROP、ALTER、TABLE、VIEW、INDEX、TRIGGER、PROCEDURE、FUNCTION
  - DML：SELECT、INSERT、UPDATE、DELETE
  - DQL：FROM、WHERE、JOIN、LEFT、RIGHT、INNER、OUTER、ON
  - DCL：GRANT、REVOKE
  - 其他：AND、OR、NOT、IN、LIKE、BETWEEN、IS、NULL、TRUE、FALSE、DISTINCT、UNION、ALL、CASE、WHEN、THEN、ELSE、END、GROUP、BY、HAVING、ORDER、LIMIT、OFFSET、AS

**3. Oracle 关键字过滤**
- 规则：检查表名是否为 Oracle 特殊关键字
- 关键字列表：DUAL、TO
- 示例：
  - `DUAL` → 过滤
  - `dual` → 过滤
  - `dual_table` → 保留

**4. Java 关键字过滤**
- 规则：检查表名是否为 Java 关键字
- 关键字列表：
  - 访问修饰符：public、private、protected
  - 类声明：class、interface、extends、implements
  - 修饰符：static、final、abstract、synchronized、volatile、transient、native
  - 包和导入：package、import
  - 控制流：if、else、for、while、do、switch、case、default、break、continue、return
  - 异常处理：try、catch、finally、throw、throws
  - 其他：new、this、super、instanceof、typeof、void
  - 类型：int、long、float、double、char、boolean、byte、short、String、Object、List、Map、Set、Array、ArrayList、HashMap、HashSet

**5. 变量形式过滤**
- 规则：检查表名是否包含变量占位符
- 模式：`${...}`
- 示例：
  - `user_table` → 保留
  - `${tableName}` → 过滤
  - `user_${suffix}` → 过滤

**6. 空表名过滤**
- 规则：过滤空字符串或仅包含特殊字符的表名
- 示例：
  - `` → 过滤
  - `   ` → 过滤
  - `user_table` → 保留

#### 4.3.2 数据规范化

**字符过滤：**
- 规则：仅保留英文字母、数字、下划线和点
- 示例：
  - `user-table` → `usertable`
  - `user table` → `usertable`
  - `user@table` → `usertable`
  - `user.table` → `user.table`
  - `user_table` → `user_table`

#### 4.3.3 排序规则

**多列排序：**
- 排序方向：所有列升序（ASC）
- 排序优先级（从高到低）：
  1. 来源（source）
  2. Schema（schema）
  3. 表名（table_name）
  4. 文件名（file_name）
  5. 行号（line_num）

**示例：**
```
来源    | Schema | 表名        | 文件名           | 行号
--------|--------|-------------|------------------|------
XML     | master | order_item  | OrderMapper.xml  | 10
XML     | master | order_item  | OrderMapper.xml  | 25
XML     | master | order_table | OrderMapper.xml  | 5
XML     | slave  | user_table  | UserMapper.xml   | 15
注解    | master | user_table  | UserMapper.java  | 20
```

### 4.4 统计规则

#### 4.4.1 提取统计

**统计维度：**
1. **总提取条数**：所有提取器提取的表名总数
2. **XML 文件**：从 XML 文件提取的数量
3. **注解提取**：从 Java 注解提取的总数
   - @TableName：数量
   - @Select：数量
   - @Insert：数量
   - @Update：数量
   - @Delete：数量
4. **Java SQL**：从 Java SQL 语句提取的数量

#### 4.4.2 过滤统计

**统计维度：**
1. **总过滤数**：被过滤的表名总数
2. **按原因分组**：
   - 包含中文字符：数量
   - 是 SQL 关键字：数量
   - 是 Java 关键字：数量
   - 是 Oracle 关键字：数量
   - 包含变量形式：数量
   - 其他原因：数量

#### 4.4.3 Schema 统计

**统计维度：**
1. **按 Schema 分组**：
   - master：表数量
   - slave：表数量
   - mdb：表数量
   - 其他：表数量
2. **总表数**：所有表的总数

#### 4.4.4 文件统计

**统计维度：**
1. **总文件数**：扫描到的文件总数
2. **成功处理**：成功提取表名的文件数
3. **处理失败**：处理时出错的文件数
4. **文件类型分布**：
   - Java 文件：数量
   - XML 文件：数量

### 4.5 Excel 生成规则

#### 4.5.1 Sheet1：原始数据

**列结构：**
1. 来源（source）：表名来源（XML、注解、Java SQL）
2. Schema（schema）：Schema 归属
3. 表名（table_name）：提取的表名
4. 文件名（file_name）：所在文件名
5. 行号（line_num）：所在行号

**特点：**
- 包含所有提取的原始数据
- 未经过滤和排序
- 用于数据溯源
- 表头采用蓝色背景、白色加粗文字、居中对齐的格式
- 列宽自适应内容长度

#### 4.5.2 Sheet2：清洗后数据

**列结构：**
1. 来源（source）：表名来源
2. Schema（schema）：Schema 归属
3. 表名（table_name）：清洗后的表名
4. 文件名（file_name）：所在文件名
5. 行号（line_num）：所在行号

**特点：**
- 经过过滤规则清洗
- 经过数据规范化
- 按多列升序排序
- 用于最终分析
- 表头采用蓝色背景、白色加粗文字、居中对齐的格式
- 列宽自适应内容长度

#### 4.5.3 Sheet3：Schema 统计

**列结构：**
1. Schema：Schema 名称
2. 表数量：该 Schema 下的表数量
3. 占比：占总表数的百分比

**特点：**
- 按表数量降序排列
- 提供可视化统计
- 表头采用蓝色背景、白色加粗文字、居中对齐的格式
- 列宽自适应内容长度

#### 4.5.4 Sheet4：文件统计

**列结构：**
1. 文件类型：Java 或 XML
2. 文件数量：该类型的文件数量
3. 提取表数：从该类型提取的表数量
4. 平均每文件：平均每个文件提取的表数量

**特点：**
- 按文件类型分组统计
- 提供处理效率分析
- 表头采用蓝色背景、白色加粗文字、居中对齐的格式
- 列宽自适应内容长度

#### 4.5.5 Sheet5：处理总结

**内容结构：**
1. 项目信息
   - 项目路径
   - 扫描时间
   - 总文件数

2. 提取统计
   - 总提取条数
   - 各提取规则的数量

3. 过滤统计
   - 总过滤数
   - 各过滤原因的数量

4. Schema 统计
   - 各 Schema 的表数量

5. 处理结果
   - 成功处理文件数
   - 处理失败文件数
   - 最终表数量

**特点：**
- 提供整体处理概况
- 便于快速了解处理结果
- 表头采用蓝色背景、白色加粗文字、居中对齐的格式
- 列宽自适应内容长度

## 五、常见问题

### 5.1 扫描不到文件

**可能原因：**
- 项目路径不正确
- 项目中没有 `main` 目录
- 文件编码不是 UTF-8

**解决方法：**
- 检查项目路径是否正确
- 确认项目中存在 `.java` 或 `.xml` 文件
- 检查文件编码是否为 UTF-8

### 5.2 提取的表名不准确

**可能原因：**
- SQL 语句格式不规范
- 注解格式不正确
- 表名使用了变量

**解决方法：**
- 检查 SQL 语句格式
- 确认注解格式正确
- 避免在表名中使用变量

### 5.3 Schema 归属不正确

**可能原因：**
- @DS 注解格式不正确
- 类名和文件名不匹配
- 方法级别注解未识别

**解决方法：**
- 检查 @DS 注解格式
- 确保类名和文件名一致
- 使用类级别注解替代方法级别注解

### 5.4 过滤掉有效的表名

**可能原因：**
- 表名包含中文字符
- 表名是关键字
- 表名包含特殊字符

**解决方法：**
- 避免在表名中使用中文字符
- 避免使用关键字作为表名
- 仅使用字母、数字、下划线和点

## 六、扩展开发

### 6.1 添加新的提取规则

1. 在 `modules/extractors/` 目录下创建新的提取器类
2. 继承 `BaseExtractor` 基类
3. 实现 `extract()` 方法
4. 在 `ExtractorManager` 中注册新的提取器

### 6.2 修改清洗规则

在 `ExcelGenerator._clean_table_info()` 方法中修改清洗逻辑：

```python
def _clean_table_info(self, table_info_list):
    # 添加新的过滤规则
    # 修改现有的过滤规则
    # 调整排序规则
    pass
```

### 6.3 添加新的统计维度

在相应的模块中添加统计逻辑：

1. 在提取器中添加计数器
2. 在 `ExtractorManager` 中添加统计方法
3. 在 `ExcelGenerator` 中添加统计表

## 七、版本历史

### v1.0.0
- 初始版本
- 支持从 XML 和 Java 文件提取表名
- 支持 Schema 归属分析
- 支持 Excel 报告生成
- 支持数据清洗和排序
- 支持详细的统计报告

## 八、联系方式

如有问题或建议，请联系开发团队。
