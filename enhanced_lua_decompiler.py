#!/usr/bin/env python3
"""
增强的Lua字节码反编译器
尝试从Lua字节码中提取更多信息并生成可读的源代码
"""

import struct
import os
import sys
import re
from typing import List, Dict, Any, Tuple

class EnhancedLuaDecompiler:
    def __init__(self):
        self.strings = []
        self.functions = []
        self.constants = []
        self.globals = []
        self.locals = []
        self.debug_info = {}
        
    def read_lua_header(self, data: bytes) -> Dict[str, Any]:
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
    
    def extract_strings_advanced(self, data: bytes) -> List[str]:
        """高级字符串提取"""
        strings = []
        
        # 方法1: 查找以长度开头的字符串
        i = 0
        while i < len(data) - 4:
            try:
                # 尝试读取4字节长度
                length = struct.unpack('<I', data[i:i+4])[0]
                if 1 <= length <= 1000 and i + 4 + length < len(data):
                    string_data = data[i+4:i+4+length]
                    try:
                        # 尝试UTF-8解码
                        string = string_data.decode('utf-8')
                        if self.is_printable_string(string):
                            strings.append(string)
                    except:
                        try:
                            # 尝试GBK解码
                            string = string_data.decode('gbk')
                            if self.is_printable_string(string):
                                strings.append(string)
                        except:
                            pass
            except:
                pass
            i += 1
        
        # 方法2: 查找ASCII字符串
        ascii_strings = self.extract_ascii_strings(data)
        strings.extend(ascii_strings)
        
        # 去重并排序
        return sorted(list(set(strings)))
    
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
    
    def is_printable_string(self, s: str) -> bool:
        """检查字符串是否可打印"""
        if len(s) < 2:
            return False
        return all(ord(c) >= 32 and ord(c) <= 126 for c in s)
    
    def extract_function_patterns(self, data: bytes) -> List[Dict[str, Any]]:
        """提取函数模式"""
        functions = []
        
        # 查找函数相关的字节模式
        function_indicators = [
            b'function',
            b'local function',
            b'end',
            b'return',
            b'if',
            b'else',
            b'for',
            b'while',
            b'do'
        ]
        
        for indicator in function_indicators:
            pos = 0
            while True:
                pos = data.find(indicator, pos)
                if pos == -1:
                    break
                
                # 尝试提取函数上下文
                context_start = max(0, pos - 50)
                context_end = min(len(data), pos + 100)
                context = data[context_start:context_end]
                
                functions.append({
                    'indicator': indicator.decode(),
                    'position': pos,
                    'context': context
                })
                
                pos += len(indicator)
        
        return functions
    
    def generate_pseudo_code(self, strings: List[str], functions: List[Dict[str, Any]]) -> str:
        """生成伪代码"""
        code_lines = []
        
        # 添加文件头注释
        code_lines.append("-- Lua源代码还原 (伪代码)")
        code_lines.append("-- 从字节码中提取的信息")
        code_lines.append("")
        
        # 添加提取的字符串作为注释
        if strings:
            code_lines.append("-- 提取的字符串:")
            for i, string in enumerate(strings[:50]):  # 限制前50个
                code_lines.append(f"-- {i+1}. {string}")
            code_lines.append("")
        
        # 尝试重构函数结构
        code_lines.append("-- 重构的函数结构:")
        code_lines.append("")
        
        # 基于字符串生成伪代码
        for string in strings:
            if any(keyword in string.lower() for keyword in ['function', 'local', 'if', 'for', 'while']):
                code_lines.append(f"-- 可能的函数: {string}")
            elif '=' in string and len(string) < 100:
                code_lines.append(f"-- 可能的赋值: {string}")
            elif string.startswith('print') or string.startswith('log'):
                code_lines.append(f"-- 可能的日志: {string}")
        
        return "\n".join(code_lines)
    
    def analyze_bytecode_structure(self, data: bytes) -> Dict[str, Any]:
        """分析字节码结构"""
        analysis = {
            'file_size': len(data),
            'header': self.read_lua_header(data),
            'strings': [],
            'functions': [],
            'constants': [],
            'debug_info': {}
        }
        
        # 提取字符串
        analysis['strings'] = self.extract_strings_advanced(data)
        
        # 提取函数模式
        analysis['functions'] = self.extract_function_patterns(data)
        
        # 分析常量
        analysis['constants'] = self.extract_constants(data)
        
        return analysis
    
    def extract_constants(self, data: bytes) -> List[Any]:
        """提取常量"""
        constants = []
        
        # 查找数字常量
        i = 0
        while i < len(data) - 8:
            try:
                # 尝试读取double
                number = struct.unpack('<d', data[i:i+8])[0]
                if -1e10 < number < 1e10 and not (number != number):  # 检查NaN
                    constants.append(('number', number))
            except:
                pass
            i += 1
        
        # 查找整数常量
        i = 0
        while i < len(data) - 4:
            try:
                integer = struct.unpack('<i', data[i:i+4])[0]
                if -1000000 < integer < 1000000:
                    constants.append(('integer', integer))
            except:
                pass
            i += 1
        
        return constants
    
    def decompile_file(self, filename: str) -> Dict[str, Any]:
        """反编译单个文件"""
        print(f"\n=== 反编译文件: {filename} ===")
        
        try:
            with open(filename, 'rb') as f:
                data = f.read()
        except Exception as e:
            print(f"读取文件失败: {e}")
            return None
        
        # 分析字节码
        analysis = self.analyze_bytecode_structure(data)
        
        # 生成伪代码
        pseudo_code = self.generate_pseudo_code(analysis['strings'], analysis['functions'])
        
        # 保存结果
        result = {
            'filename': filename,
            'analysis': analysis,
            'pseudo_code': pseudo_code
        }
        
        return result
    
    def save_decompiled_code(self, result: Dict[str, Any], output_dir: str):
        """保存反编译的代码"""
        if not result:
            return
            
        filename = os.path.basename(result['filename'])
        base_name = os.path.splitext(filename)[0]
        
        # 保存伪代码
        pseudo_file = os.path.join(output_dir, f"{base_name}_pseudo.lua")
        with open(pseudo_file, 'w', encoding='utf-8') as f:
            f.write(result['pseudo_code'])
        
        # 保存分析结果
        analysis_file = os.path.join(output_dir, f"{base_name}_analysis.txt")
        with open(analysis_file, 'w', encoding='utf-8') as f:
            f.write(f"文件: {result['filename']}\n")
            f.write(f"大小: {result['analysis']['file_size']} 字节\n")
            f.write(f"字符串数量: {len(result['analysis']['strings'])}\n")
            f.write(f"函数数量: {len(result['analysis']['functions'])}\n")
            f.write(f"常量数量: {len(result['analysis']['constants'])}\n\n")
            
            f.write("提取的字符串:\n")
            for i, string in enumerate(result['analysis']['strings'][:100]):
                f.write(f"{i+1}. {string}\n")
        
        print(f"已保存: {pseudo_file}")
        print(f"已保存: {analysis_file}")

def main():
    decompiler = EnhancedLuaDecompiler()
    
    # 创建输出目录
    output_dir = "decompiled_lua"
    os.makedirs(output_dir, exist_ok=True)
    
    # 反编译所有文件
    input_dir = "extracted_gbk"
    success_count = 0
    
    for i in range(1, 74):  # 1到73
        filename = f"{input_dir}/file_{i}.lua"
        if os.path.exists(filename):
            result = decompiler.decompile_file(filename)
            if result:
                decompiler.save_decompiled_code(result, output_dir)
                success_count += 1
        else:
            print(f"文件不存在: {filename}")
    
    print(f"\n反编译完成! 成功处理 {success_count} 个文件")
    print(f"输出目录: {output_dir}")

if __name__ == "__main__":
    main()