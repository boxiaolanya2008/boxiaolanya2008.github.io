#!/usr/bin/env python3
"""
高级Lua字节码反编译器
基于现有解码器改进，增加更多功能和更好的源代码重构能力
"""

import struct
import os
import sys
import re
import json
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class LuaString:
    """Lua字符串信息"""
    content: str
    offset: int
    length: int
    is_function_name: bool = False
    is_class_name: bool = False
    is_module_name: bool = False
    is_variable: bool = False

@dataclass
class LuaFunction:
    """Lua函数信息"""
    name: str
    offset: int
    parameters: List[str]
    local_variables: List[str]
    calls: List[str]
    is_main: bool = False

@dataclass
class LuaModule:
    """Lua模块信息"""
    name: str
    functions: List[LuaFunction]
    imports: List[str]
    exports: List[str]
    dependencies: List[str]

class AdvancedLuaDecompiler:
    def __init__(self):
        self.strings: List[LuaString] = []
        self.functions: List[LuaFunction] = []
        self.modules: List[LuaModule] = []
        self.imports: List[str] = []
        self.global_variables: List[str] = []
        self.class_patterns = [
            r'^[A-Z][a-zA-Z0-9_]*$',  # 类名模式
            r'^U[A-Z][a-zA-Z0-9_]*$',  # Unreal类
            r'^A[A-Z][a-zA-Z0-9_]*$',  # Actor类
            r'^F[A-Z][a-zA-Z0-9_]*$',  # 结构体
        ]
        self.function_patterns = [
            r'^[a-zA-Z_][a-zA-Z0-9_]*_[A-Z][a-zA-Z0-9_]*$',  # 函数名模式
            r'^[A-Z][a-zA-Z0-9_]*::[a-zA-Z_][a-zA-Z0-9_]*$',  # C++风格
        ]
        self.module_patterns = [
            r'^[A-Z][a-zA-Z0-9_]*$',  # 模块名
            r'^DFM[A-Z][a-zA-Z0-9_]*$',  # DFM模块
            r'^GP[A-Z][a-zA-Z0-9_]*$',  # GP模块
        ]

    def is_valid_lua_string(self, text: str) -> bool:
        """检查是否为有效的Lua字符串"""
        if not text or len(text) < 2:
            return False
        
        # 检查是否包含可打印字符
        if not all(ord(c) >= 32 and ord(c) <= 126 for c in text):
            return False
        
        # 排除明显的非字符串数据
        if text.isdigit() or text.replace('.', '').isdigit():
            return False
            
        return True

    def classify_string(self, text: str) -> Dict[str, bool]:
        """分类字符串类型"""
        classification = {
            'is_function_name': False,
            'is_class_name': False,
            'is_module_name': False,
            'is_variable': False
        }
        
        # 检查是否为类名
        for pattern in self.class_patterns:
            if re.match(pattern, text):
                classification['is_class_name'] = True
                break
        
        # 检查是否为函数名
        for pattern in self.function_patterns:
            if re.match(pattern, text):
                classification['is_function_name'] = True
                break
        
        # 检查是否为模块名
        for pattern in self.module_patterns:
            if re.match(pattern, text):
                classification['is_module_name'] = True
                break
        
        # 检查是否为变量名
        if re.match(r'^[a-z_][a-zA-Z0-9_]*$', text) and not classification['is_function_name']:
            classification['is_variable'] = True
        
        return classification

    def extract_strings_advanced(self, data: bytes) -> List[LuaString]:
        """高级字符串提取"""
        strings = []
        i = 0
        
        while i < len(data) - 4:
            try:
                # 尝试读取长度（小端序）
                length = struct.unpack('<I', data[i:i+4])[0]
                
                # 检查长度是否合理
                if 2 <= length <= 500 and i + 4 + length < len(data):
                    # 尝试解码为字符串
                    string_data = data[i+4:i+4+length]
                    try:
                        # 尝试UTF-8解码
                        text = string_data.decode('utf-8')
                        if self.is_valid_lua_string(text):
                            classification = self.classify_string(text)
                            lua_string = LuaString(
                                content=text,
                                offset=i,
                                length=length,
                                **classification
                            )
                            strings.append(lua_string)
                    except UnicodeDecodeError:
                        # 尝试GBK解码
                        try:
                            text = string_data.decode('gbk')
                            if self.is_valid_lua_string(text):
                                classification = self.classify_string(text)
                                lua_string = LuaString(
                                    content=text,
                                    offset=i,
                                    length=length,
                                    **classification
                                )
                                strings.append(lua_string)
                        except UnicodeDecodeError:
                            pass
            except struct.error:
                pass
            
            i += 1
        
        return strings

    def extract_functions_from_strings(self, strings: List[LuaString]) -> List[LuaFunction]:
        """从字符串中提取函数信息"""
        functions = []
        function_strings = [s for s in strings if s.is_function_name]
        
        for string in function_strings:
            # 解析函数名
            if '::' in string.content:
                # C++风格函数名
                parts = string.content.split('::')
                if len(parts) == 2:
                    class_name, func_name = parts
                    function = LuaFunction(
                        name=string.content,
                        offset=string.offset,
                        parameters=[],
                        local_variables=[],
                        calls=[]
                    )
                    functions.append(function)
            else:
                # 普通函数名
                function = LuaFunction(
                    name=string.content,
                    offset=string.offset,
                    parameters=[],
                    local_variables=[],
                    calls=[]
                )
                functions.append(function)
        
        return functions

    def extract_modules_from_strings(self, strings: List[LuaString]) -> List[LuaModule]:
        """从字符串中提取模块信息"""
        modules = []
        module_strings = [s for s in strings if s.is_module_name]
        
        for string in module_strings:
            # 查找相关函数
            related_functions = []
            for func in self.functions:
                if string.content in func.name:
                    related_functions.append(func)
            
            module = LuaModule(
                name=string.content,
                functions=related_functions,
                imports=[],
                exports=[],
                dependencies=[]
            )
            modules.append(module)
        
        return modules

    def generate_lua_source(self, strings: List[LuaString], functions: List[LuaFunction], modules: List[LuaModule]) -> str:
        """生成Lua源代码"""
        source_lines = []
        
        # 添加文件头注释
        source_lines.append("-- 自动生成的Lua源代码")
        source_lines.append("-- 从字节码文件反编译生成")
        source_lines.append("-- 生成时间: " + str(os.popen('date').read().strip()))
        source_lines.append("")
        
        # 添加模块声明
        for module in modules:
            source_lines.append(f"-- 模块: {module.name}")
            source_lines.append(f"local {module.name} = {{}}")
            source_lines.append("")
        
        # 添加导入语句
        import_strings = [s for s in strings if 'import' in s.content.lower() or 'require' in s.content.lower()]
        if import_strings:
            source_lines.append("-- 导入模块")
            for imp in import_strings:
                source_lines.append(f"-- {imp.content}")
            source_lines.append("")
        
        # 添加全局变量
        global_vars = [s for s in strings if s.is_variable and len(s.content) > 3]
        if global_vars:
            source_lines.append("-- 全局变量")
            for var in global_vars[:20]:  # 限制数量
                source_lines.append(f"local {var.content} = nil")
            source_lines.append("")
        
        # 添加函数定义
        source_lines.append("-- 函数定义")
        for func in functions:
            source_lines.append(f"-- 函数: {func.name}")
            source_lines.append(f"function {func.name}()")
            source_lines.append("    -- 函数体需要进一步分析")
            source_lines.append("end")
            source_lines.append("")
        
        # 添加主函数
        source_lines.append("-- 主函数")
        source_lines.append("function main()")
        source_lines.append("    -- 主逻辑")
        source_lines.append("end")
        source_lines.append("")
        
        # 添加返回语句
        source_lines.append("return main")
        
        return "\n".join(source_lines)

    def analyze_bytecode_file(self, filepath: str) -> Dict[str, Any]:
        """分析单个字节码文件"""
        print(f"\n=== 分析文件: {filepath} ===")
        
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
        except Exception as e:
            print(f"读取文件失败: {e}")
            return {}
        
        if len(data) < 12:
            print("文件太小，不是有效的Lua字节码")
            return {}
        
        # 检查Lua魔数
        if data[:4] != b'\x1bLua':
            print("不是有效的Lua字节码文件")
            return {}
        
        # 解析头部信息
        version = data[4]
        format_version = data[5]
        endianness = data[6]
        
        print(f"文件大小: {len(data)} 字节")
        print(f"Lua版本: {version}")
        print(f"格式版本: {format_version}")
        print(f"字节序: {'小端' if endianness == 0 else '大端'}")
        
        # 提取字符串
        print("正在提取字符串...")
        strings = self.extract_strings_advanced(data)
        print(f"找到 {len(strings)} 个字符串")
        
        # 分类字符串
        function_strings = [s for s in strings if s.is_function_name]
        class_strings = [s for s in strings if s.is_class_name]
        module_strings = [s for s in strings if s.is_module_name]
        variable_strings = [s for s in strings if s.is_variable]
        
        print(f"函数名: {len(function_strings)} 个")
        print(f"类名: {len(class_strings)} 个")
        print(f"模块名: {len(module_strings)} 个")
        print(f"变量名: {len(variable_strings)} 个")
        
        # 提取函数信息
        functions = self.extract_functions_from_strings(strings)
        
        # 提取模块信息
        modules = self.extract_modules_from_strings(strings)
        
        # 生成源代码
        source_code = self.generate_lua_source(strings, functions, modules)
        
        return {
            'filepath': filepath,
            'file_size': len(data),
            'lua_version': version,
            'format_version': format_version,
            'endianness': endianness,
            'strings': strings,
            'functions': functions,
            'modules': modules,
            'source_code': source_code,
            'statistics': {
                'total_strings': len(strings),
                'function_strings': len(function_strings),
                'class_strings': len(class_strings),
                'module_strings': len(module_strings),
                'variable_strings': len(variable_strings),
                'functions': len(functions),
                'modules': len(modules)
            }
        }

    def process_all_files(self, input_dir: str, output_dir: str) -> Dict[str, Any]:
        """处理所有字节码文件"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        results = {}
        all_strings = []
        all_functions = []
        all_modules = []
        
        # 获取所有字节码文件
        bytecode_files = []
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.endswith('.lua') or not file.endswith('.'):
                    bytecode_files.append(os.path.join(root, file))
        
        print(f"找到 {len(bytecode_files)} 个字节码文件")
        
        # 处理每个文件
        for i, filepath in enumerate(bytecode_files):
            print(f"\n处理文件 {i+1}/{len(bytecode_files)}: {os.path.basename(filepath)}")
            
            result = self.analyze_bytecode_file(filepath)
            if result:
                results[filepath] = result
                all_strings.extend(result['strings'])
                all_functions.extend(result['functions'])
                all_modules.extend(result['modules'])
                
                # 保存单个文件的源代码
                filename = os.path.basename(filepath)
                source_file = os.path.join(output_dir, f"{filename}_source.lua")
                with open(source_file, 'w', encoding='utf-8') as f:
                    f.write(result['source_code'])
        
        # 生成综合报告
        self.generate_comprehensive_report(results, all_strings, all_functions, all_modules, output_dir)
        
        return results

    def generate_comprehensive_report(self, results: Dict[str, Any], all_strings: List[LuaString], 
                                    all_functions: List[LuaFunction], all_modules: List[LuaModule], 
                                    output_dir: str):
        """生成综合报告"""
        
        # 统计信息
        total_files = len(results)
        total_strings = len(all_strings)
        total_functions = len(all_functions)
        total_modules = len(all_modules)
        
        # 生成综合源代码
        comprehensive_source = self.generate_comprehensive_source(all_strings, all_functions, all_modules)
        
        # 保存综合源代码
        with open(os.path.join(output_dir, "comprehensive_source.lua"), 'w', encoding='utf-8') as f:
            f.write(comprehensive_source)
        
        # 生成JSON报告
        report_data = {
            'summary': {
                'total_files': total_files,
                'total_strings': total_strings,
                'total_functions': total_functions,
                'total_modules': total_modules
            },
            'files': results,
            'all_strings': [{'content': s.content, 'offset': s.offset, 'length': s.length, 
                            'is_function_name': s.is_function_name, 'is_class_name': s.is_class_name,
                            'is_module_name': s.is_module_name, 'is_variable': s.is_variable} 
                           for s in all_strings],
            'all_functions': [{'name': f.name, 'offset': f.offset, 'parameters': f.parameters,
                             'local_variables': f.local_variables, 'calls': f.calls, 'is_main': f.is_main}
                            for f in all_functions],
            'all_modules': [{'name': m.name, 'functions': [f.name for f in m.functions],
                           'imports': m.imports, 'exports': m.exports, 'dependencies': m.dependencies}
                          for m in all_modules]
        }
        
        with open(os.path.join(output_dir, "decompilation_report.json"), 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        # 生成Markdown报告
        markdown_report = self.generate_markdown_report(report_data)
        with open(os.path.join(output_dir, "decompilation_report.md"), 'w', encoding='utf-8') as f:
            f.write(markdown_report)
        
        print(f"\n=== 解码完成 ===")
        print(f"处理文件数: {total_files}")
        print(f"提取字符串数: {total_strings}")
        print(f"提取函数数: {total_functions}")
        print(f"提取模块数: {total_modules}")
        print(f"输出目录: {output_dir}")

    def generate_comprehensive_source(self, all_strings: List[LuaString], all_functions: List[LuaFunction], 
                                    all_modules: List[LuaModule]) -> str:
        """生成综合源代码"""
        source_lines = []
        
        # 文件头
        source_lines.append("-- ========================================")
        source_lines.append("-- 综合Lua源代码")
        source_lines.append("-- 从多个字节码文件反编译生成")
        source_lines.append("-- ========================================")
        source_lines.append("")
        
        # 模块声明
        unique_modules = list(set([m.name for m in all_modules]))
        if unique_modules:
            source_lines.append("-- 模块声明")
            for module in sorted(unique_modules):
                source_lines.append(f"local {module} = {{}}")
            source_lines.append("")
        
        # 全局变量
        unique_vars = list(set([s.content for s in all_strings if s.is_variable and len(s.content) > 3]))
        if unique_vars:
            source_lines.append("-- 全局变量")
            for var in sorted(unique_vars)[:50]:  # 限制数量
                source_lines.append(f"local {var} = nil")
            source_lines.append("")
        
        # 函数定义
        unique_functions = list(set([f.name for f in all_functions]))
        if unique_functions:
            source_lines.append("-- 函数定义")
            for func_name in sorted(unique_functions):
                source_lines.append(f"function {func_name}()")
                source_lines.append("    -- 函数体需要进一步分析")
                source_lines.append("end")
                source_lines.append("")
        
        # 主函数
        source_lines.append("-- 主函数")
        source_lines.append("function main()")
        source_lines.append("    -- 主逻辑")
        source_lines.append("end")
        source_lines.append("")
        
        # 返回
        source_lines.append("return main")
        
        return "\n".join(source_lines)

    def generate_markdown_report(self, report_data: Dict[str, Any]) -> str:
        """生成Markdown报告"""
        lines = []
        
        lines.append("# Lua字节码反编译报告")
        lines.append("")
        lines.append("## 总体统计")
        lines.append(f"- 处理文件数: {report_data['summary']['total_files']}")
        lines.append(f"- 提取字符串数: {report_data['summary']['total_strings']}")
        lines.append(f"- 提取函数数: {report_data['summary']['total_functions']}")
        lines.append(f"- 提取模块数: {report_data['summary']['total_modules']}")
        lines.append("")
        
        # 模块统计
        if report_data['all_modules']:
            lines.append("## 模块列表")
            for module in report_data['all_modules']:
                lines.append(f"- {module['name']} ({len(module['functions'])} 个函数)")
            lines.append("")
        
        # 函数统计
        if report_data['all_functions']:
            lines.append("## 函数列表")
            for func in report_data['all_functions'][:20]:  # 限制显示数量
                lines.append(f"- {func['name']}")
            if len(report_data['all_functions']) > 20:
                lines.append(f"- ... 还有 {len(report_data['all_functions']) - 20} 个函数")
            lines.append("")
        
        # 文件详情
        lines.append("## 文件详情")
        for filepath, result in report_data['files'].items():
            lines.append(f"### {os.path.basename(filepath)}")
            lines.append(f"- 文件大小: {result['file_size']} 字节")
            lines.append(f"- Lua版本: {result['lua_version']}")
            lines.append(f"- 字符串数: {result['statistics']['total_strings']}")
            lines.append(f"- 函数数: {result['statistics']['functions']}")
            lines.append(f"- 模块数: {result['statistics']['modules']}")
            lines.append("")
        
        return "\n".join(lines)

def main():
    decompiler = AdvancedLuaDecompiler()
    
    # 设置输入和输出目录
    input_dir = "/workspace/lua_bytecode"
    output_dir = "/workspace/decompiled_source"
    
    print("开始Lua字节码反编译...")
    print(f"输入目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    
    # 处理所有文件
    results = decompiler.process_all_files(input_dir, output_dir)
    
    print("\n反编译完成！")
    print(f"结果保存在: {output_dir}")

if __name__ == "__main__":
    main()