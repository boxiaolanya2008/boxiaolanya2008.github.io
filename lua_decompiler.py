#!/usr/bin/env python3
"""
Lua字节码反编译器
尝试解码Lua字节码文件并提取可读信息
"""

import struct
import os
import sys

class LuaDecompiler:
    def __init__(self):
        self.strings = []
        self.functions = []
        
    def read_string(self, data, offset):
        """读取字符串"""
        if offset >= len(data):
            return "", offset
            
        # 尝试读取长度
        try:
            length = struct.unpack('<I', data[offset:offset+4])[0]
            offset += 4
            if length == 0:
                return "", offset
            if offset + length > len(data):
                return "", offset
            string = data[offset:offset+length].decode('utf-8', errors='ignore')
            offset += length
            return string, offset
        except:
            return "", offset
    
    def read_number(self, data, offset):
        """读取数字"""
        try:
            number = struct.unpack('<d', data[offset:offset+8])[0]
            return number, offset + 8
        except:
            return 0, offset
    
    def read_integer(self, data, offset):
        """读取整数"""
        try:
            integer = struct.unpack('<i', data[offset:offset+4])[0]
            return integer, offset + 4
        except:
            return 0, offset
    
    def analyze_bytecode(self, filename):
        """分析字节码文件"""
        print(f"\n=== 分析文件: {filename} ===")
        
        with open(filename, 'rb') as f:
            data = f.read()
        
        if len(data) < 12:
            print("文件太小，不是有效的Lua字节码")
            return
        
        # 检查Lua魔数
        if data[:4] != b'\x1bLua':
            print("不是有效的Lua字节码文件")
            return
        
        print(f"文件大小: {len(data)} 字节")
        
        # 解析头部
        version = data[4]
        format_version = data[5]
        endianness = data[6]
        
        print(f"Lua版本: {version}")
        print(f"格式版本: {format_version}")
        print(f"字节序: {'小端' if endianness == 0 else '大端'}")
        
        # 尝试提取字符串
        self.extract_strings(data)
        
        # 尝试提取函数信息
        self.extract_functions(data)
    
    def extract_strings(self, data):
        """提取字符串"""
        print("\n--- 提取的字符串 ---")
        strings = []
        
        # 搜索可能的字符串模式
        i = 0
        while i < len(data) - 4:
            # 查找可能的字符串长度（小整数）
            try:
                length = struct.unpack('<I', data[i:i+4])[0]
                if 4 <= length <= 200 and i + 4 + length < len(data):
                    # 尝试解码为字符串
                    string_data = data[i+4:i+4+length]
                    try:
                        string = string_data.decode('utf-8')
                        if string.isprintable() and len(string) > 2:
                            strings.append(string)
                            print(f"  {string}")
                    except:
                        pass
            except:
                pass
            i += 1
        
        print(f"找到 {len(strings)} 个可能的字符串")
    
    def extract_functions(self, data):
        """提取函数信息"""
        print("\n--- 函数信息 ---")
        
        # 搜索函数相关的模式
        function_patterns = [
            b'function',
            b'local',
            b'return',
            b'if',
            b'else',
            b'end',
            b'for',
            b'while',
            b'do'
        ]
        
        for pattern in function_patterns:
            count = data.count(pattern)
            if count > 0:
                print(f"  找到 {count} 个 '{pattern.decode()}' 模式")
    
    def decompile_file(self, filename):
        """反编译单个文件"""
        try:
            self.analyze_bytecode(filename)
        except Exception as e:
            print(f"反编译 {filename} 时出错: {e}")

def main():
    decompiler = LuaDecompiler()
    
    # 反编译前几个文件
    for i in range(1, 6):
        filename = f'extracted_gbk/file_{i}.lua'
        if os.path.exists(filename):
            decompiler.decompile_file(filename)
        else:
            print(f"文件不存在: {filename}")

if __name__ == "__main__":
    main()