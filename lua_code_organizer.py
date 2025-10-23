#!/usr/bin/env python3
"""
Lua代码整理器
将重构的Lua代码按功能模块分类整理
"""

import os
import re
from typing import List, Dict, Any, Tuple

class LuaCodeOrganizer:
    def __init__(self):
        self.module_categories = {
            'MetaDorianDriver': {
                'name': '元数据驱动系统',
                'keywords': ['MetaDorianDriver', 'MetaDorianManager', 'BattleFieldUtil', 'MTFlag'],
                'files': []
            },
            'DFMGameplay': {
                'name': '游戏玩法模块',
                'keywords': ['DFMGameplay', 'PlayerCharacter', 'Character', 'Movement', 'Animation'],
                'files': []
            },
            'DFMGameHud': {
                'name': '用户界面模块',
                'keywords': ['DFMGameHud', 'HUD', 'UI', 'Widget', 'Button', 'Panel'],
                'files': []
            },
            'DFMAbility': {
                'name': '能力系统模块',
                'keywords': ['DFMAbility', 'Ability', 'Weapon', 'Tactical', 'Montage'],
                'files': []
            },
            'GPGameplay': {
                'name': '游戏玩法核心',
                'keywords': ['GPGameplay', 'GPCharacter', 'GPPhysics', 'InputManager'],
                'files': []
            },
            'Breakthrough': {
                'name': '突破模式',
                'keywords': ['Breakthrough', 'FreeBuild', 'Fortification', 'Redeploy'],
                'files': []
            },
            'DFMQuest': {
                'name': '任务系统',
                'keywords': ['DFMQuest', 'Quest', 'Egg', 'Forest', 'Mission'],
                'files': []
            },
            'UI': {
                'name': 'UI框架',
                'keywords': ['UIUtil', 'WidgetLayout', 'Canvas', 'Overlay', 'ScrollBox'],
                'files': []
            },
            'Other': {
                'name': '其他模块',
                'keywords': [],
                'files': []
            }
        }
    
    def analyze_file_content(self, file_path: str) -> Dict[str, Any]:
        """分析文件内容"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        analysis = {
            'file_path': file_path,
            'file_name': os.path.basename(file_path),
            'content': content,
            'functions': [],
            'imports': [],
            'comments': [],
            'module_score': {}
        }
        
        # 提取函数
        function_pattern = r'function\s+([A-Za-z0-9_:]+)'
        functions = re.findall(function_pattern, content)
        analysis['functions'] = functions
        
        # 提取导入
        import_pattern = r'-- import\s+([A-Za-z0-9_.]+)'
        imports = re.findall(import_pattern, content)
        analysis['imports'] = imports
        
        # 提取注释
        comment_pattern = r'--\s+([A-Za-z0-9_.,:;!?()\s]+)'
        comments = re.findall(comment_pattern, content)
        analysis['comments'] = comments
        
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
    
    def organize_files(self, input_dir: str, output_dir: str):
        """整理文件"""
        os.makedirs(output_dir, exist_ok=True)
        
        # 为每个模块创建目录
        for module_name, module_info in self.module_categories.items():
            module_dir = os.path.join(output_dir, module_name)
            os.makedirs(module_dir, exist_ok=True)
        
        # 分析所有文件
        file_analyses = []
        for i in range(1, 74):
            file_path = f"{input_dir}/file_{i}_reconstructed.lua"
            if os.path.exists(file_path):
                analysis = self.analyze_file_content(file_path)
                file_analyses.append(analysis)
        
        # 分类文件
        for analysis in file_analyses:
            category = self.categorize_file(analysis)
            self.module_categories[category]['files'].append(analysis)
            
            # 复制文件到对应目录
            dest_path = os.path.join(output_dir, category, analysis['file_name'])
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(analysis['content'])
        
        # 生成模块索引
        self.generate_module_index(output_dir)
        
        # 生成总体报告
        self.generate_summary_report(output_dir, file_analyses)
    
    def generate_module_index(self, output_dir: str):
        """生成模块索引"""
        index_content = []
        index_content.append("# Lua源代码模块索引")
        index_content.append("")
        index_content.append("## 模块分类")
        index_content.append("")
        
        for module_name, module_info in self.module_categories.items():
            if not module_info['files']:
                continue
                
            index_content.append(f"### {module_info['name']} ({module_name})")
            index_content.append(f"文件数量: {len(module_info['files'])}")
            index_content.append("")
            
            for file_info in module_info['files']:
                index_content.append(f"- {file_info['file_name']}")
                if file_info['functions']:
                    index_content.append(f"  - 函数: {', '.join(file_info['functions'][:5])}")
                if file_info['imports']:
                    index_content.append(f"  - 导入: {', '.join(file_info['imports'][:3])}")
            index_content.append("")
        
        # 保存索引文件
        index_file = os.path.join(output_dir, "README.md")
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(index_content))
    
    def generate_summary_report(self, output_dir: str, file_analyses: List[Dict[str, Any]]):
        """生成总体报告"""
        report_content = []
        report_content.append("# Lua源代码还原总结报告")
        report_content.append("")
        report_content.append(f"## 总体统计")
        report_content.append(f"- 总文件数: {len(file_analyses)}")
        report_content.append(f"- 总函数数: {sum(len(analysis['functions']) for analysis in file_analyses)}")
        report_content.append(f"- 总导入数: {sum(len(analysis['imports']) for analysis in file_analyses)}")
        report_content.append("")
        
        report_content.append("## 模块分布")
        for module_name, module_info in self.module_categories.items():
            if module_info['files']:
                report_content.append(f"- {module_info['name']}: {len(module_info['files'])} 个文件")
        report_content.append("")
        
        report_content.append("## 主要功能模块")
        report_content.append("")
        
        # 详细分析每个模块
        for module_name, module_info in self.module_categories.items():
            if not module_info['files']:
                continue
                
            report_content.append(f"### {module_info['name']}")
            report_content.append("")
            
            # 统计函数
            all_functions = []
            for file_info in module_info['files']:
                all_functions.extend(file_info['functions'])
            
            if all_functions:
                report_content.append("主要函数:")
                for func in all_functions[:10]:  # 显示前10个
                    report_content.append(f"- {func}")
                report_content.append("")
            
            # 统计导入
            all_imports = []
            for file_info in module_info['files']:
                all_imports.extend(file_info['imports'])
            
            if all_imports:
                unique_imports = list(set(all_imports))
                report_content.append("主要导入:")
                for imp in unique_imports[:10]:  # 显示前10个
                    report_content.append(f"- {imp}")
                report_content.append("")
        
        # 保存报告
        report_file = os.path.join(output_dir, "SUMMARY_REPORT.md")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_content))
    
    def create_combined_source(self, output_dir: str):
        """创建合并的源代码文件"""
        combined_content = []
        combined_content.append("-- Lua源代码合并文件")
        combined_content.append("-- 包含所有还原的Lua代码")
        combined_content.append("")
        
        for module_name, module_info in self.module_categories.items():
            if not module_info['files']:
                continue
                
            combined_content.append(f"-- ===== {module_info['name']} =====")
            combined_content.append("")
            
            for file_info in module_info['files']:
                combined_content.append(f"-- 文件: {file_info['file_name']}")
                combined_content.append("")
                combined_content.append(file_info['content'])
                combined_content.append("")
                combined_content.append("-- " + "="*50)
                combined_content.append("")
        
        # 保存合并文件
        combined_file = os.path.join(output_dir, "combined_lua_source.lua")
        with open(combined_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(combined_content))

def main():
    organizer = LuaCodeOrganizer()
    
    # 整理文件
    input_dir = "reconstructed_lua"
    output_dir = "organized_lua_source"
    
    organizer.organize_files(input_dir, output_dir)
    
    # 创建合并文件
    organizer.create_combined_source(output_dir)
    
    print(f"代码整理完成! 输出目录: {output_dir}")

if __name__ == "__main__":
    main()