#!/usr/bin/env python3
"""
高级Lua字节码解码器
深入分析Lua字节码结构并生成更准确的源代码还原
"""

import struct
import os
import sys
import re
from typing import List, Dict, Any, Tuple, Optional

class AdvancedLuaDecoder:
    def __init__(self):
        self.strings = []
        self.functions = []
        self.constants = []
        self.locals = []
        self.upvalues = []
        self.debug_info = {}
        self.source_lines = []
        
    def read_lua_header(self, data: bytes) -> Optional[Dict[str, Any]]:
        """读取Lua字节码头部信息"""
        if len(data) < 12:
            return None
            
        # 检查Lua魔数
        if data[:4] != b'\x1bLua':
            return None
            
        header = {
            'version': data[4],
            'format_version': data[5],
            'endianness': data[6],
            'int_size': data[7],
            'size_t_size': data[8],
            'instruction_size': data[9],
            'number_size': data[10],
            'integral_flag': data[11]
        }
        
        return header
    
    def extract_strings_comprehensive(self, data: bytes) -> List[str]:
        """全面提取字符串"""
        strings = []
        
        # 方法1: 查找长度前缀的字符串
        strings.extend(self.extract_length_prefixed_strings(data))
        
        # 方法2: 查找ASCII字符串
        strings.extend(self.extract_ascii_strings(data))
        
        # 方法3: 查找UTF-8字符串
        strings.extend(self.extract_utf8_strings(data))
        
        # 方法4: 查找GBK字符串
        strings.extend(self.extract_gbk_strings(data))
        
        # 去重并过滤
        unique_strings = []
        seen = set()
        for s in strings:
            if s not in seen and len(s) >= 2 and self.is_meaningful_string(s):
                unique_strings.append(s)
                seen.add(s)
        
        return sorted(unique_strings)
    
    def extract_length_prefixed_strings(self, data: bytes) -> List[str]:
        """提取长度前缀的字符串"""
        strings = []
        i = 0
        while i < len(data) - 4:
            try:
                # 尝试读取4字节长度
                length = struct.unpack('<I', data[i:i+4])[0]
                if 1 <= length <= 2000 and i + 4 + length < len(data):
                    string_data = data[i+4:i+4+length]
                    try:
                        string = string_data.decode('utf-8')
                        if self.is_printable_string(string):
                            strings.append(string)
                    except:
                        try:
                            string = string_data.decode('gbk')
                            if self.is_printable_string(string):
                                strings.append(string)
                        except:
                            pass
            except:
                pass
            i += 1
        return strings
    
    def extract_ascii_strings(self, data: bytes) -> List[str]:
        """提取ASCII字符串"""
        strings = []
        current_string = ""
        
        for byte in data:
            if 32 <= byte <= 126:  # 可打印ASCII字符
                current_string += chr(byte)
            else:
                if len(current_string) >= 3:
                    strings.append(current_string)
                current_string = ""
        
        if len(current_string) >= 3:
            strings.append(current_string)
            
        return strings
    
    def extract_utf8_strings(self, data: bytes) -> List[str]:
        """提取UTF-8字符串"""
        strings = []
        i = 0
        while i < len(data) - 1:
            if data[i] >= 0x80:  # UTF-8多字节字符开始
                try:
                    # 尝试解码UTF-8
                    end = i
                    while end < len(data) and data[end] != 0:
                        end += 1
                    if end > i:
                        string = data[i:end].decode('utf-8')
                        if self.is_printable_string(string):
                            strings.append(string)
                        i = end
                    else:
                        i += 1
                except:
                    i += 1
            else:
                i += 1
        return strings
    
    def extract_gbk_strings(self, data: bytes) -> List[str]:
        """提取GBK字符串"""
        strings = []
        i = 0
        while i < len(data) - 1:
            if 0x81 <= data[i] <= 0xFE:  # GBK多字节字符开始
                try:
                    end = i
                    while end < len(data) and data[end] != 0:
                        end += 1
                    if end > i:
                        string = data[i:end].decode('gbk')
                        if self.is_printable_string(string):
                            strings.append(string)
                        i = end
                    else:
                        i += 1
                except:
                    i += 1
            else:
                i += 1
        return strings
    
    def is_printable_string(self, s: str) -> bool:
        """检查字符串是否可打印"""
        if len(s) < 2:
            return False
        printable_count = sum(1 for c in s if ord(c) >= 32 and ord(c) <= 126)
        return printable_count >= len(s) * 0.8  # 80%以上可打印字符
    
    def is_meaningful_string(self, s: str) -> bool:
        """检查字符串是否有意义"""
        if len(s) < 2:
            return False
        
        # 过滤掉纯数字和特殊字符
        if s.isdigit() or s.isalpha() == False and len(s) < 4:
            return False
        
        # 过滤掉明显的垃圾数据
        garbage_patterns = [
            r'^[0-9]+$',
            r'^[A-Z]{1,2}$',
            r'^[a-z]{1,2}$',
            r'^[^a-zA-Z0-9]{1,3}$'
        ]
        
        for pattern in garbage_patterns:
            if re.match(pattern, s):
                return False
        
        return True
    
    def analyze_function_structure(self, strings: List[str]) -> List[Dict[str, Any]]:
        """分析函数结构"""
        functions = []
        
        for string in strings:
            if self.is_function_name(string):
                func_info = {
                    'name': string,
                    'type': self.classify_function_type(string),
                    'module': self.extract_module_name(string),
                    'parameters': self.extract_parameters(string),
                    'return_type': self.extract_return_type(string)
                }
                functions.append(func_info)
        
        return functions
    
    def is_function_name(self, string: str) -> bool:
        """判断是否为函数名"""
        patterns = [
            r'^[A-Z][A-Za-z0-9_]*::[A-Za-z0-9_]+$',  # C++风格
            r'^[A-Z][A-Za-z0-9_]*_[A-Za-z0-9_]+_BS$',  # 蓝图函数
            r'^[A-Z][A-Za-z0-9_]*_[A-Za-z0-9_]+_ES$',  # 事件函数
            r'^[A-Z][A-Za-z0-9_]*_[A-Za-z0-9_]+_Implementation$',  # 实现函数
            r'^[A-Z][A-Za-z0-9_]*_[A-Za-z0-9_]+_BS$',  # 蓝图系统
        ]
        return any(re.match(pattern, string) for pattern in patterns)
    
    def classify_function_type(self, func_name: str) -> str:
        """分类函数类型"""
        if '::' in func_name:
            return 'C++方法'
        elif '_BS' in func_name:
            return '蓝图系统函数'
        elif '_ES' in func_name:
            return '事件系统函数'
        elif '_Implementation' in func_name:
            return '实现函数'
        else:
            return '普通函数'
    
    def extract_module_name(self, func_name: str) -> str:
        """提取模块名"""
        if '::' in func_name:
            return func_name.split('::')[0]
        elif '_' in func_name:
            parts = func_name.split('_')
            if len(parts) >= 2:
                return parts[0]
        return 'Unknown'
    
    def extract_parameters(self, func_name: str) -> List[str]:
        """提取参数信息（基于命名模式）"""
        # 这是一个简化的实现，实际需要更复杂的分析
        return []
    
    def extract_return_type(self, func_name: str) -> str:
        """提取返回类型（基于命名模式）"""
        if 'Get' in func_name:
            return 'Object'
        elif 'Is' in func_name or 'Has' in func_name:
            return 'Boolean'
        elif 'Set' in func_name or 'Update' in func_name:
            return 'Void'
        else:
            return 'Unknown'
    
    def generate_lua_source(self, strings: List[str], functions: List[Dict[str, Any]]) -> str:
        """生成Lua源代码"""
        lines = []
        
        # 文件头
        lines.append("-- Lua源代码解码结果")
        lines.append("-- 基于字节码深度分析生成")
        lines.append("-- 生成时间: " + str(__import__('datetime').datetime.now()))
        lines.append("")
        
        # 模块导入
        imports = [s for s in strings if 'import' in s or 'require' in s or 'DFM.' in s]
        if imports:
            lines.append("-- 模块导入")
            for imp in imports[:20]:  # 限制前20个
                lines.append(f"-- {imp}")
            lines.append("")
        
        # 常量定义
        constants = [s for s in strings if self.is_constant(s)]
        if constants:
            lines.append("-- 常量定义")
            for const in constants[:30]:  # 限制前30个
                lines.append(f"-- local {const}")
            lines.append("")
        
        # 函数定义
        if functions:
            lines.append("-- 函数定义")
            for func in functions[:50]:  # 限制前50个
                lines.append(f"-- {func['type']}: {func['name']}")
                lines.append(f"-- 模块: {func['module']}")
                lines.append(f"-- 返回类型: {func['return_type']}")
                lines.append("")
        
        # 生成实际函数代码
        lines.append("-- 函数实现")
        lines.append("")
        
        for func in functions[:20]:  # 限制前20个主要函数
            lines.append(self.generate_function_code(func, strings))
            lines.append("")
        
        return "\n".join(lines)
    
    def is_constant(self, string: str) -> bool:
        """判断是否为常量"""
        patterns = [
            r'^[A-Z_]+$',  # 全大写常量
            r'^[A-Z][A-Za-z0-9_]*$',  # 大写开头的常量
        ]
        return any(re.match(pattern, string) for pattern in patterns)
    
    def generate_function_code(self, func: Dict[str, Any], strings: List[str]) -> str:
        """生成函数代码"""
        lines = []
        
        # 函数签名
        if '::' in func['name']:
            class_name, method_name = func['name'].split('::', 1)
            lines.append(f"function {class_name}:{method_name}()")
        else:
            lines.append(f"function {func['name']}()")
        
        # 函数体
        lines.append("    -- 基于字节码分析重构的函数实现")
        lines.append("    ")
        
        # 添加相关的字符串作为注释
        related_strings = [s for s in strings if any(part in s for part in func['name'].split('_'))]
        for s in related_strings[:5]:
            lines.append(f"    -- {s}")
        
        lines.append("    ")
        lines.append("    -- TODO: 需要根据实际业务逻辑完善实现")
        lines.append("    ")
        lines.append("    return nil")
        lines.append("end")
        
        return "\n".join(lines)
    
    def decode_file(self, file_path: str) -> Dict[str, Any]:
        """解码单个文件"""
        print(f"正在解码文件: {file_path}")
        
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
        except Exception as e:
            print(f"读取文件失败: {e}")
            return None
        
        # 分析头部
        header = self.read_lua_header(data)
        if not header:
            print("不是有效的Lua字节码文件")
            return None
        
        # 提取字符串
        strings = self.extract_strings_comprehensive(data)
        
        # 分析函数结构
        functions = self.analyze_function_structure(strings)
        
        # 生成源代码
        source_code = self.generate_lua_source(strings, functions)
        
        return {
            'file_path': file_path,
            'header': header,
            'strings': strings,
            'functions': functions,
            'source_code': source_code
        }
    
    def decode_all_files(self, input_dir: str, output_dir: str):
        """解码所有文件"""
        os.makedirs(output_dir, exist_ok=True)
        
        success_count = 0
        all_results = []
        
        # 处理extracted_gbk目录
        for i in range(1, 74):
            file_path = f"{input_dir}/file_{i}.lua"
            if os.path.exists(file_path):
                result = self.decode_file(file_path)
                if result:
                    all_results.append(result)
                    
                    # 保存解码结果
                    base_name = f"file_{i}"
                    source_file = f"{output_dir}/{base_name}_decoded.lua"
                    with open(source_file, 'w', encoding='utf-8') as f:
                        f.write(result['source_code'])
                    
                    # 保存分析报告
                    report_file = f"{output_dir}/{base_name}_analysis.txt"
                    with open(report_file, 'w', encoding='utf-8') as f:
                        f.write(f"文件: {result['file_path']}\n")
                        f.write(f"Lua版本: {result['header']['version']}\n")
                        f.write(f"字符串数量: {len(result['strings'])}\n")
                        f.write(f"函数数量: {len(result['functions'])}\n\n")
                        f.write("提取的字符串:\n")
                        for i, s in enumerate(result['strings'][:100]):
                            f.write(f"{i+1}. {s}\n")
                    
                    print(f"已保存: {source_file}")
                    success_count += 1
        
        # 生成总体报告
        self.generate_summary_report(all_results, output_dir)
        
        print(f"\n解码完成! 成功处理 {success_count} 个文件")
        print(f"输出目录: {output_dir}")
    
    def generate_summary_report(self, results: List[Dict[str, Any]], output_dir: str):
        """生成总结报告"""
        report_lines = []
        report_lines.append("# Lua字节码解码总结报告")
        report_lines.append("")
        report_lines.append(f"## 总体统计")
        report_lines.append(f"- 总文件数: {len(results)}")
        report_lines.append(f"- 总字符串数: {sum(len(r['strings']) for r in results)}")
        report_lines.append(f"- 总函数数: {sum(len(r['functions']) for r in results)}")
        report_lines.append("")
        
        # 按模块统计
        module_stats = {}
        for result in results:
            for func in result['functions']:
                module = func['module']
                if module not in module_stats:
                    module_stats[module] = {'functions': 0, 'files': set()}
                module_stats[module]['functions'] += 1
                module_stats[module]['files'].add(result['file_path'])
        
        report_lines.append("## 模块统计")
        for module, stats in sorted(module_stats.items()):
            report_lines.append(f"- {module}: {stats['functions']} 个函数, {len(stats['files'])} 个文件")
        
        # 保存报告
        report_file = f"{output_dir}/DECODE_SUMMARY.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))

def main():
    decoder = AdvancedLuaDecoder()
    
    # 解码所有文件
    input_dir = "extracted_gbk"
    output_dir = "decoded_lua_source"
    
    decoder.decode_all_files(input_dir, output_dir)

if __name__ == "__main__":
    main()