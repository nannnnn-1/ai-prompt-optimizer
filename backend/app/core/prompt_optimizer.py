"""
提示词优化器模块
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import time
from dataclasses import dataclass

from .ai_client import AIClient


@dataclass
class OptimizationStrategy:
    """优化策略"""
    name: str
    description: str
    priority: int
    applicable_types: List[str]


@dataclass 
class OptimizationContext:
    """优化上下文"""
    optimization_type: str
    user_preferences: Optional[Dict[str, Any]] = None
    domain_knowledge: Optional[str] = None
    target_audience: Optional[str] = None


class PromptOptimizer(ABC):
    """提示词优化器基类"""
    
    @abstractmethod
    async def optimize(self, prompt: str, context: OptimizationContext) -> Dict[str, Any]:
        """优化提示词的抽象方法"""
        pass


class AIPromptOptimizer(PromptOptimizer):
    """基于AI的提示词优化器"""
    
    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client
        self.optimization_strategies = self._load_optimization_strategies()
        self.optimization_templates = self._load_optimization_templates()
    
    def _load_optimization_strategies(self) -> List[OptimizationStrategy]:
        """加载优化策略"""
        return [
            OptimizationStrategy(
                name="improve_clarity",
                description="提升指令清晰度",
                priority=1,
                applicable_types=["general", "code", "writing", "analysis"]
            ),
            OptimizationStrategy(
                name="add_structure",
                description="添加逻辑结构",
                priority=2,
                applicable_types=["general", "writing", "analysis"]
            ),
            OptimizationStrategy(
                name="add_context",
                description="补充上下文信息",
                priority=3,
                applicable_types=["general", "code", "writing", "analysis"]
            ),
            OptimizationStrategy(
                name="add_code_specifics",
                description="添加编程特定要求",
                priority=1,
                applicable_types=["code"]
            ),
            OptimizationStrategy(
                name="add_writing_guidelines",
                description="添加写作规范",
                priority=1,
                applicable_types=["writing"]
            ),
            OptimizationStrategy(
                name="add_analysis_framework",
                description="添加分析框架",
                priority=1,
                applicable_types=["analysis"]
            )
        ]
    
    def _load_optimization_templates(self) -> Dict[str, str]:
        """加载优化模板"""
        return {
            "general": """
请优化以下提示词，使其更加清晰、完整和具体：

原始提示词：{original_prompt}

优化要求：
1. 增强指令的清晰度和准确性
2. 补充必要的上下文信息
3. 改善逻辑结构
4. 确保AI能够准确理解和执行

请返回优化后的提示词，并说明主要改进点。
""",
            
            "code": """
请优化以下编程相关的提示词：

原始提示词：{original_prompt}

优化要求：
1. 明确编程语言和版本要求
2. 详细说明输入输出规格
3. 添加具体的技术要求
4. 提供代码示例或预期格式
5. 包含错误处理要求

请返回优化后的提示词，并说明主要改进点。
""",
            
            "writing": """
请优化以下写作相关的提示词：

原始提示词：{original_prompt}

优化要求：
1. 明确文体类型和风格要求
2. 指定目标受众和语调
3. 说明结构和格式要求
4. 添加字数或篇幅限制
5. 包含具体的内容要点

请返回优化后的提示词，并说明主要改进点。
""",
            
            "analysis": """
请优化以下分析相关的提示词：

原始提示词：{original_prompt}

优化要求：
1. 明确分析对象和范围
2. 指定分析框架和方法
3. 说明数据来源和要求
4. 定义输出格式和结构
5. 包含评估标准

请返回优化后的提示词，并说明主要改进点。
"""
        }
    
    async def optimize(self, prompt: str, context: OptimizationContext) -> Dict[str, Any]:
        """
        优化提示词的主要方法
        
        Args:
            prompt: 原始提示词
            context: 优化上下文
            
        Returns:
            优化结果
        """
        start_time = time.time()
        
        # 1. 分析原始提示词
        analysis = await self._analyze_prompt(prompt)
        
        # 2. 确定优化策略
        strategies = self._determine_strategies(analysis, context)
        
        # 3. 应用优化策略
        optimized_prompt = await self._apply_strategies(prompt, strategies, context)
        
        # 4. 生成改进说明
        improvements = await self._generate_improvements(
            prompt, optimized_prompt, strategies, analysis
        )
        
        # 5. 评估优化效果
        optimized_analysis = await self._analyze_prompt(optimized_prompt)
        
        processing_time = time.time() - start_time
        
        return {
            "optimized_prompt": optimized_prompt,
            "improvements": improvements,
            "strategies_used": [s.name for s in strategies],
            "quality_score_before": analysis.get("overall_score", 5),
            "quality_score_after": optimized_analysis.get("overall_score", 5),
            "processing_time": processing_time,
            "analysis_before": analysis,
            "analysis_after": optimized_analysis
        }
    
    async def _analyze_prompt(self, prompt: str) -> Dict[str, Any]:
        """分析提示词特征"""
        return await self.ai_client.analyze_prompt_quality(prompt)
    
    def _determine_strategies(self, analysis: Dict, context: OptimizationContext) -> List[OptimizationStrategy]:
        """确定优化策略"""
        selected_strategies = []
        
        # 根据质量分析结果选择策略
        scores = analysis.get('scores', {})
        
        if scores.get("clarity", 10) < 7:
            selected_strategies.append(
                next(s for s in self.optimization_strategies if s.name == "improve_clarity")
            )
        
        if scores.get("structure", 10) < 7:
            selected_strategies.append(
                next(s for s in self.optimization_strategies if s.name == "add_structure")
            )
        
        if scores.get("completeness", 10) < 7:
            selected_strategies.append(
                next(s for s in self.optimization_strategies if s.name == "add_context")
            )
        
        # 根据优化类型添加特定策略
        type_specific_strategies = [
            s for s in self.optimization_strategies 
            if context.optimization_type in s.applicable_types and s.name.startswith(f"add_{context.optimization_type}")
        ]
        selected_strategies.extend(type_specific_strategies)
        
        # 去重并按优先级排序
        unique_strategies = list({s.name: s for s in selected_strategies}.values())
        unique_strategies.sort(key=lambda x: x.priority)
        
        return unique_strategies
    
    async def _apply_strategies(
        self, 
        prompt: str, 
        strategies: List[OptimizationStrategy], 
        context: OptimizationContext
    ) -> str:
        """应用优化策略"""
        
        # 选择合适的模板
        template = self.optimization_templates.get(context.optimization_type, self.optimization_templates["general"])
        
        # 构建优化请求
        optimization_prompt = template.format(original_prompt=prompt)
        
        # 添加策略特定的指导
        if strategies:
            strategy_guidance = "\n\n特别关注以下优化策略：\n"
            for strategy in strategies:
                strategy_guidance += f"- {strategy.description}\n"
            optimization_prompt += strategy_guidance
        
        # 添加用户偏好
        if context.user_preferences:
            preference_guidance = "\n\n用户偏好：\n"
            for key, value in context.user_preferences.items():
                preference_guidance += f"- {key}: {value}\n"
            optimization_prompt += preference_guidance
        
        # 调用AI进行优化
        messages = [
            {"role": "system", "content": "你是一个专业的提示词优化专家。请帮助用户优化提示词，使其更加清晰、完整、具体和有效。"},
            {"role": "user", "content": optimization_prompt}
        ]
        
        response = await self.ai_client._make_request_with_retry(messages, temperature=0.7)
        optimized_content = response.choices[0].message.content
        
        # 解析优化结果
        optimized_prompt, _ = self.ai_client._parse_optimization_result(optimized_content)
        
        return optimized_prompt
    
    async def _generate_improvements(
        self, 
        original_prompt: str, 
        optimized_prompt: str, 
        strategies: List[OptimizationStrategy],
        analysis: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """生成改进说明"""
        
        improvements = []
        
        # 基于应用的策略生成改进说明
        for strategy in strategies:
            improvements.append({
                "type": strategy.description,
                "description": f"应用了{strategy.description}策略，提升了提示词的{strategy.name.replace('_', '和')}",
                "strategy": strategy.name
            })
        
        # 基于质量分析生成具体改进
        issues = analysis.get('issues', [])
        suggestions = analysis.get('suggestions', [])
        
        for i, (issue, suggestion) in enumerate(zip(issues[:3], suggestions[:3])):
            improvements.append({
                "type": f"问题修复 {i+1}",
                "description": f"针对问题'{issue}'，实施了改进：{suggestion}",
                "issue": issue,
                "suggestion": suggestion
            })
        
        return improvements
    
    async def get_available_strategies(self, optimization_type: str) -> List[OptimizationStrategy]:
        """获取可用的优化策略"""
        return [
            strategy for strategy in self.optimization_strategies
            if optimization_type in strategy.applicable_types
        ]
    
    async def preview_optimization(self, prompt: str, context: OptimizationContext) -> Dict[str, Any]:
        """预览优化效果（不执行实际优化）"""
        analysis = await self._analyze_prompt(prompt)
        strategies = self._determine_strategies(analysis, context)
        
        return {
            "current_analysis": analysis,
            "recommended_strategies": [
                {
                    "name": s.name,
                    "description": s.description,
                    "priority": s.priority
                } for s in strategies
            ],
            "estimated_improvements": len(strategies)
        } 