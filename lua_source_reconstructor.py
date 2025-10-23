#!/usr/bin/env python3
"""
Lua源代码重构器
基于提取的字符串信息重构更接近原始代码的Lua源代码
"""

import os
import re
from typing import List, Dict, Any, Tuple

class LuaSourceReconstructor:
    def __init__(self):
        self.function_patterns = {
            'function_def': r'function\s+(\w+)',
            'local_function': r'local\s+function\s+(\w+)',
            'method_call': r'(\w+):(\w+)\(',
            'variable_assignment': r'(\w+)\s*=\s*',
            'if_statement': r'if\s+',
            'for_loop': r'for\s+',
            'while_loop': r'while\s+',
            'return_statement': r'return\s+'
        }
        
        self.game_modules = {
            'MetaDorianDriver': '元数据驱动系统',
            'DFMGameplay': '游戏玩法模块',
            'DFMGameHud': '用户界面模块', 
            'DFMAbility': '能力系统模块',
            'GPGameplay': '游戏玩法核心',
            'Breakthrough': '突破模式',
            'DFMQuest': '任务系统'
        }
    
    def analyze_strings(self, strings: List[str]) -> Dict[str, Any]:
        """分析字符串并分类"""
        analysis = {
            'functions': [],
            'variables': [],
            'constants': [],
            'comments': [],
            'imports': [],
            'game_objects': [],
            'ui_elements': [],
            'debug_messages': []
        }
        
        for string in strings:
            string = string.strip()
            if not string or len(string) < 2:
                continue
                
            # 函数名模式
            if self.is_function_name(string):
                analysis['functions'].append(string)
            # 变量名模式
            elif self.is_variable_name(string):
                analysis['variables'].append(string)
            # 常量模式
            elif self.is_constant(string):
                analysis['constants'].append(string)
            # 注释模式
            elif self.is_comment(string):
                analysis['comments'].append(string)
            # 导入模式
            elif self.is_import(string):
                analysis['imports'].append(string)
            # 游戏对象模式
            elif self.is_game_object(string):
                analysis['game_objects'].append(string)
            # UI元素模式
            elif self.is_ui_element(string):
                analysis['ui_elements'].append(string)
            # 调试消息模式
            elif self.is_debug_message(string):
                analysis['debug_messages'].append(string)
        
        return analysis
    
    def is_function_name(self, string: str) -> bool:
        """判断是否为函数名"""
        patterns = [
            r'^[A-Z][A-Za-z0-9_]*::[A-Za-z0-9_]+$',  # C++风格函数
            r'^[A-Z][A-Za-z0-9_]*_[A-Za-z0-9_]+_BS$',  # 蓝图函数
            r'^[A-Z][A-Za-z0-9_]*_[A-Za-z0-9_]+_ES$',  # 事件函数
            r'^[A-Z][A-Za-z0-9_]*_[A-Za-z0-9_]+_Implementation$',  # 实现函数
        ]
        return any(re.match(pattern, string) for pattern in patterns)
    
    def is_variable_name(self, string: str) -> bool:
        """判断是否为变量名"""
        patterns = [
            r'^[a-z][A-Za-z0-9_]*$',  # 小写开头的变量
            r'^[A-Z][A-Za-z0-9_]*$',  # 大写开头的常量
            r'^[a-z][A-Za-z0-9_]*\s*=$',  # 赋值语句
        ]
        return any(re.match(pattern, string) for pattern in patterns)
    
    def is_constant(self, string: str) -> bool:
        """判断是否为常量"""
        patterns = [
            r'^[A-Z_]+$',  # 全大写常量
            r'^\d+$',  # 数字常量
            r'^\d+\.\d+$',  # 浮点数常量
        ]
        return any(re.match(pattern, string) for pattern in patterns)
    
    def is_comment(self, string: str) -> bool:
        """判断是否为注释"""
        return string.startswith('--') or 'log' in string.lower() or 'print' in string.lower()
    
    def is_import(self, string: str) -> bool:
        """判断是否为导入语句"""
        return 'import' in string or 'require' in string or 'DFM.' in string
    
    def is_game_object(self, string: str) -> bool:
        """判断是否为游戏对象"""
        patterns = [
            r'^A[A-Z][A-Za-z0-9_]*$',  # Actor类
            r'^U[A-Z][A-Za-z0-9_]*$',  # UObject类
            r'^F[A-Z][A-Za-z0-9_]*$',  # 结构体
        ]
        return any(re.match(pattern, string) for pattern in patterns)
    
    def is_ui_element(self, string: str) -> bool:
        """判断是否为UI元素"""
        ui_keywords = ['Widget', 'HUD', 'UI', 'Button', 'Panel', 'Canvas', 'Overlay']
        return any(keyword in string for keyword in ui_keywords)
    
    def is_debug_message(self, string: str) -> bool:
        """判断是否为调试消息"""
        debug_keywords = ['log', 'print', 'error', 'warning', 'debug', 'hotfix']
        return any(keyword in string.lower() for keyword in debug_keywords)
    
    def generate_module_structure(self, analysis: Dict[str, Any]) -> str:
        """生成模块结构"""
        lines = []
        
        # 模块头部
        lines.append("-- Lua源代码重构")
        lines.append("-- 基于字节码分析重构的代码结构")
        lines.append("")
        
        # 导入语句
        if analysis['imports']:
            lines.append("-- 导入模块")
            for imp in analysis['imports'][:10]:  # 限制前10个
                lines.append(f"-- import {imp}")
            lines.append("")
        
        # 常量定义
        if analysis['constants']:
            lines.append("-- 常量定义")
            for const in analysis['constants'][:20]:  # 限制前20个
                lines.append(f"-- local {const}")
            lines.append("")
        
        # 游戏对象定义
        if analysis['game_objects']:
            lines.append("-- 游戏对象")
            for obj in analysis['game_objects'][:15]:  # 限制前15个
                lines.append(f"-- {obj}")
            lines.append("")
        
        # 函数定义
        if analysis['functions']:
            lines.append("-- 函数定义")
            for func in analysis['functions'][:20]:  # 限制前20个
                lines.append(f"-- function {func}")
                lines.append("--     -- 函数实现")
                lines.append("-- end")
                lines.append("")
        
        return "\n".join(lines)
    
    def generate_function_code(self, function_name: str, analysis: Dict[str, Any]) -> str:
        """生成函数代码"""
        lines = []
        
        # 函数签名
        if '::' in function_name:
            # C++风格函数
            class_name, method_name = function_name.split('::', 1)
            lines.append(f"function {class_name}:{method_name}()")
        else:
            # 普通函数
            lines.append(f"function {function_name}()")
        
        # 函数体
        lines.append("    -- 函数实现基于字节码分析重构")
        lines.append("    ")
        
        # 添加相关的变量和调用
        related_vars = [v for v in analysis['variables'] if function_name.split('_')[-1].lower() in v.lower()]
        for var in related_vars[:5]:
            lines.append(f"    local {var} = nil")
        
        # 添加调试信息
        debug_msgs = [msg for msg in analysis['debug_messages'] if function_name.split('_')[-1].lower() in msg.lower()]
        for msg in debug_msgs[:3]:
            lines.append(f"    -- {msg}")
        
        lines.append("    ")
        lines.append("    -- TODO: 需要根据实际逻辑完善")
        lines.append("end")
        
        return "\n".join(lines)
    
    def reconstruct_file(self, analysis_file: str, pseudo_file: str) -> str:
        """重构单个文件"""
        # 读取分析结果
        with open(analysis_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取字符串
        strings = []
        in_strings_section = False
        for line in content.split('\n'):
            if '提取的字符串:' in line:
                in_strings_section = True
                continue
            if in_strings_section and line.strip():
                if line.startswith('--') or line.startswith('文件:') or line.startswith('大小:'):
                    continue
                if line.strip().startswith(tuple('0123456789')):
                    # 提取字符串部分
                    parts = line.split('. ', 1)
                    if len(parts) > 1:
                        strings.append(parts[1].strip())
                else:
                    break
        
        # 分析字符串
        analysis = self.analyze_strings(strings)
        
        # 生成重构代码
        reconstructed_code = self.generate_module_structure(analysis)
        
        # 添加主要函数
        if analysis['functions']:
            reconstructed_code += "\n-- 主要函数实现\n"
            for func in analysis['functions'][:10]:  # 限制前10个主要函数
                reconstructed_code += "\n" + self.generate_function_code(func, analysis) + "\n"
        
        return reconstructed_code
    
    def process_all_files(self, input_dir: str, output_dir: str):
        """处理所有文件"""
        os.makedirs(output_dir, exist_ok=True)
        
        success_count = 0
        for i in range(1, 74):
            analysis_file = f"{input_dir}/file_{i}_analysis.txt"
            pseudo_file = f"{input_dir}/file_{i}_pseudo.lua"
            
            if os.path.exists(analysis_file):
                try:
                    reconstructed_code = self.reconstruct_file(analysis_file, pseudo_file)
                    
                    # 保存重构的代码
                    output_file = f"{output_dir}/file_{i}_reconstructed.lua"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(reconstructed_code)
                    
                    print(f"已重构: file_{i}_reconstructed.lua")
                    success_count += 1
                    
                except Exception as e:
                    print(f"重构 file_{i} 时出错: {e}")
        
        print(f"\n重构完成! 成功处理 {success_count} 个文件")
        print(f"输出目录: {output_dir}")

def main():
    reconstructor = LuaSourceReconstructor()
    
    # 重构所有文件
    input_dir = "decompiled_lua"
    output_dir = "reconstructed_lua"
    
    reconstructor.process_all_files(input_dir, output_dir)

if __name__ == "__main__":
    main()