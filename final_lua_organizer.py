#!/usr/bin/env python3
"""
最终Lua代码整理器
将解码后的Lua代码按功能模块重新组织并生成完整的项目结构
"""

import os
import re
from typing import List, Dict, Any, Tuple

class FinalLuaOrganizer:
    def __init__(self):
        self.module_categories = {
            'MetaDorianDriver': {
                'name': '元数据驱动系统',
                'keywords': ['MetaDorianDriver', 'MetaDorianManager', 'BattleFieldUtil', 'MTFlag', 'AddDorianFunction'],
                'files': []
            },
            'DFMGameplay': {
                'name': '游戏玩法模块',
                'keywords': ['DFMGameplay', 'PlayerCharacter', 'Character', 'Movement', 'Animation', 'Interactor'],
                'files': []
            },
            'DFMGameHud': {
                'name': '用户界面模块',
                'keywords': ['DFMGameHud', 'HUD', 'UI', 'Widget', 'Button', 'Panel', 'Map', 'Controller'],
                'files': []
            },
            'DFMAbility': {
                'name': '能力系统模块',
                'keywords': ['DFMAbility', 'Ability', 'Weapon', 'Tactical', 'Montage', 'BionicBird'],
                'files': []
            },
            'GPGameplay': {
                'name': '游戏玩法核心',
                'keywords': ['GPGameplay', 'GPCharacter', 'GPPhysics', 'InputManager', 'Weapon', 'Movement'],
                'files': []
            },
            'Breakthrough': {
                'name': '突破模式',
                'keywords': ['Breakthrough', 'FreeBuild', 'Fortification', 'Redeploy', 'Interactable'],
                'files': []
            },
            'DFMQuest': {
                'name': '任务系统',
                'keywords': ['DFMQuest', 'Quest', 'Egg', 'Forest', 'Mission', 'ClientProxy'],
                'files': []
            },
            'UI': {
                'name': 'UI框架',
                'keywords': ['UIUtil', 'WidgetLayout', 'Canvas', 'Overlay', 'ScrollBox', 'Widget'],
                'files': []
            },
            'Core': {
                'name': '核心系统',
                'keywords': ['Core', 'System', 'Manager', 'Util', 'Helper', 'Config'],
                'files': []
            },
            'Other': {
                'name': '其他模块',
                'keywords': [],
                'files': []
            }
        }
    
    def analyze_decoded_file(self, file_path: str) -> Dict[str, Any]:
        """分析解码后的文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        analysis = {
            'file_path': file_path,
            'file_name': os.path.basename(file_path),
            'content': content,
            'functions': [],
            'imports': [],
            'constants': [],
            'module_score': {}
        }
        
        # 提取函数
        function_pattern = r'function\s+([A-Za-z0-9_:]+)'
        functions = re.findall(function_pattern, content)
        analysis['functions'] = functions
        
        # 提取导入
        import_pattern = r'--\s+([A-Za-z0-9_.]+)'
        imports = re.findall(import_pattern, content)
        analysis['imports'] = imports
        
        # 提取常量
        constant_pattern = r'--\s+local\s+([A-Za-z0-9_]+)'
        constants = re.findall(constant_pattern, content)
        analysis['constants'] = constants
        
        # 计算模块匹配分数
        for module_name, module_info in self.module_categories.items():
            if module_name == 'Other':
                continue
            score = 0
            for keyword in module_info['keywords']:
                if keyword in content:
                    score += 1
            analysis['module_score'][module_name] = score
        
        return analysis
    
    def categorize_file(self, analysis: Dict[str, Any]) -> str:
        """分类文件"""
        # 找到得分最高的模块
        best_module = 'Other'
        best_score = 0
        
        for module_name, score in analysis['module_score'].items():
            if score > best_score:
                best_score = score
                best_module = module_name
        
        return best_module
    
    def create_project_structure(self, output_dir: str):
        """创建项目结构"""
        # 创建主目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 为每个模块创建目录
        for module_name, module_info in self.module_categories.items():
            module_dir = os.path.join(output_dir, module_name)
            os.makedirs(module_dir, exist_ok=True)
            
            # 创建子目录
            subdirs = ['src', 'config', 'utils', 'tests']
            for subdir in subdirs:
                os.makedirs(os.path.join(module_dir, subdir), exist_ok=True)
        
        # 创建根目录文件
        self.create_root_files(output_dir)
    
    def create_root_files(self, output_dir: str):
        """创建根目录文件"""
        # 创建主入口文件
        main_lua = os.path.join(output_dir, 'main.lua')
        with open(main_lua, 'w', encoding='utf-8') as f:
            f.write("""-- Lua项目主入口文件
-- 基于字节码解码重构的完整项目

-- 导入核心模块
require 'MetaDorianDriver.src.init'
require 'DFMGameplay.src.init'
require 'DFMGameHud.src.init'
require 'DFMAbility.src.init'
require 'GPGameplay.src.init'
require 'Breakthrough.src.init'
require 'DFMQuest.src.init'
require 'UI.src.init'
require 'Core.src.init'

-- 初始化系统
print("Lua项目初始化完成")
""")
        
        # 创建README文件
        readme_file = os.path.join(output_dir, 'README.md')
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write("""# Lua源代码项目

## 项目概述
这是基于Lua字节码解码重构的完整源代码项目，包含游戏系统的各个功能模块。

## 模块结构
- **MetaDorianDriver**: 元数据驱动系统
- **DFMGameplay**: 游戏玩法模块
- **DFMGameHud**: 用户界面模块
- **DFMAbility**: 能力系统模块
- **GPGameplay**: 游戏玩法核心
- **Breakthrough**: 突破模式
- **DFMQuest**: 任务系统
- **UI**: UI框架
- **Core**: 核心系统

## 使用方法
1. 确保Lua环境已安装
2. 运行 `lua main.lua` 启动项目
3. 根据需要修改各模块的配置

## 注意事项
- 代码基于字节码分析重构，部分逻辑需要根据实际需求完善
- 建议在修改前备份原始文件
""")
    
    def organize_files(self, input_dir: str, output_dir: str):
        """整理文件"""
        # 创建项目结构
        self.create_project_structure(output_dir)
        
        # 分析所有文件
        file_analyses = []
        for i in range(1, 74):
            file_path = f"{input_dir}/file_{i}_decoded.lua"
            if os.path.exists(file_path):
                analysis = self.analyze_decoded_file(file_path)
                file_analyses.append(analysis)
        
        # 分类文件
        for analysis in file_analyses:
            category = self.categorize_file(analysis)
            self.module_categories[category]['files'].append(analysis)
            
            # 复制文件到对应目录
            dest_path = os.path.join(output_dir, category, 'src', analysis['file_name'])
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(analysis['content'])
        
        # 生成模块初始化文件
        self.generate_module_init_files(output_dir)
        
        # 生成项目文档
        self.generate_project_documentation(output_dir, file_analyses)
    
    def generate_module_init_files(self, output_dir: str):
        """生成模块初始化文件"""
        for module_name, module_info in self.module_categories.items():
            if not module_info['files']:
                continue
            
            init_file = os.path.join(output_dir, module_name, 'src', 'init.lua')
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write(f"""-- {module_info['name']} 模块初始化文件
-- 自动生成于 {__import__('datetime').datetime.now()}

print("正在初始化 {module_info['name']} 模块...")

-- 导入模块文件
""")
                
                for file_info in module_info['files']:
                    base_name = os.path.splitext(file_info['file_name'])[0]
                    f.write(f"-- require '{base_name}'\n")
                
                f.write(f"""
-- 模块初始化完成
print("{module_info['name']} 模块初始化完成")
""")
    
    def generate_project_documentation(self, output_dir: str, file_analyses: List[Dict[str, Any]]):
        """生成项目文档"""
        # 生成API文档
        api_doc = os.path.join(output_dir, 'API_DOCUMENTATION.md')
        with open(api_doc, 'w', encoding='utf-8') as f:
            f.write("# API文档\n\n")
            
            for module_name, module_info in self.module_categories.items():
                if not module_info['files']:
                    continue
                
                f.write(f"## {module_info['name']}\n\n")
                
                # 收集所有函数
                all_functions = []
                for file_info in module_info['files']:
                    all_functions.extend(file_info['functions'])
                
                if all_functions:
                    f.write("### 主要函数\n")
                    for func in all_functions[:20]:  # 限制前20个
                        f.write(f"- `{func}`\n")
                    f.write("\n")
        
        # 生成项目统计
        stats_file = os.path.join(output_dir, 'PROJECT_STATS.md')
        with open(stats_file, 'w', encoding='utf-8') as f:
            f.write("# 项目统计\n\n")
            f.write(f"## 总体统计\n")
            f.write(f"- 总文件数: {len(file_analyses)}\n")
            f.write(f"- 总函数数: {sum(len(a['functions']) for a in file_analyses)}\n")
            f.write(f"- 总常量数: {sum(len(a['constants']) for a in file_analyses)}\n\n")
            
            f.write("## 模块分布\n")
            for module_name, module_info in self.module_categories.items():
                if module_info['files']:
                    f.write(f"- {module_info['name']}: {len(module_info['files'])} 个文件\n")

def main():
    organizer = FinalLuaOrganizer()
    
    # 整理文件
    input_dir = "decoded_lua_source"
    output_dir = "final_lua_project"
    
    organizer.organize_files(input_dir, output_dir)
    
    print(f"最终项目整理完成! 输出目录: {output_dir}")
    print("项目结构已创建，包含完整的模块化组织")

if __name__ == "__main__":
    main()