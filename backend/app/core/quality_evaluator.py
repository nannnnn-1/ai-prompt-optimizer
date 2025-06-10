"""
提示词质量评估器模块
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import time

from .ai_client import AIClient


class QualityCriterion(Enum):
    """质量评估标准"""
    CLARITY = "clarity"
    COMPLETENESS = "completeness"
    STRUCTURE = "structure"
    SPECIFICITY = "specificity"
    ACTIONABILITY = "actionability"


@dataclass
class QualityScore:
    """质量评分"""
    criterion: QualityCriterion
    score: float
    max_score: float = 10.0
    description: str = ""
    
    @property
    def percentage(self) -> float:
        """获取百分比分数"""
        return (self.score / self.max_score) * 100


@dataclass
class QualityReport:
    """质量报告"""
    overall_score: float
    detailed_scores: Dict[str, QualityScore]
    issues: List[str]
    suggestions: List[str]
    strengths: List[str]
    processing_time: float
    
    @property
    def grade(self) -> str:
        """获取等级评价"""
        if self.overall_score >= 9:
            return "优秀"
        elif self.overall_score >= 8:
            return "良好"
        elif self.overall_score >= 7:
            return "中等"
        elif self.overall_score >= 6:
            return "及格"
        else:
            return "需改进"


class QualityEvaluator:
    """提示词质量评估器"""
    
    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client
        self.evaluation_criteria = self._load_evaluation_criteria()
        self.evaluation_templates = self._load_evaluation_templates()
    
    def _load_evaluation_criteria(self) -> Dict[QualityCriterion, str]:
        """加载评估标准"""
        return {
            QualityCriterion.CLARITY: "指令是否清晰明确，无歧义",
            QualityCriterion.COMPLETENESS: "是否包含必要的信息和上下文",
            QualityCriterion.STRUCTURE: "逻辑结构是否清晰有序",
            QualityCriterion.SPECIFICITY: "是否足够具体和详细",
            QualityCriterion.ACTIONABILITY: "AI是否能够有效执行指令"
        }
    
    def _load_evaluation_templates(self) -> Dict[str, str]:
        """加载评估模板"""
        return {
            "comprehensive": """
请对以下提示词进行全面的质量评估：

提示词：{prompt}

请从以下维度进行评分（1-10分）：

1. 清晰度 (Clarity) - 指令是否清晰明确，无歧义
2. 完整性 (Completeness) - 是否包含必要的信息和上下文
3. 结构性 (Structure) - 逻辑结构是否清晰有序
4. 具体性 (Specificity) - 是否足够具体和详细
5. 可执行性 (Actionability) - AI是否能够有效执行指令

请以JSON格式返回评估结果：
{{
    "scores": {{
        "clarity": 8,
        "completeness": 7,
        "structure": 6,
        "specificity": 8,
        "actionability": 9
    }},
    "overall_score": 7.6,
    "issues": [
        "问题1：具体描述存在的问题",
        "问题2：另一个需要改进的地方"
    ],
    "suggestions": [
        "建议1：具体的改进建议",
        "建议2：另一个优化方向"
    ],
    "strengths": [
        "优点1：提示词的突出优势",
        "优点2：值得保持的特点"
    ]
}}
""",
            
            "quick": """
请快速评估以下提示词的质量（1-10分）：

提示词：{prompt}

请评估其总体质量并说明主要优缺点。
返回JSON格式：
{{
    "overall_score": 7,
    "brief_analysis": "简要分析",
    "main_issues": ["主要问题"],
    "quick_suggestions": ["快速建议"]
}}
"""
        }
    
    async def evaluate(self, prompt: str, mode: str = "comprehensive") -> QualityReport:
        """
        评估提示词质量
        
        Args:
            prompt: 要评估的提示词
            mode: 评估模式 ("comprehensive" 或 "quick")
            
        Returns:
            质量报告
        """
        start_time = time.time()
        
        try:
            if mode == "comprehensive":
                result = await self._comprehensive_evaluation(prompt)
            elif mode == "quick":
                result = await self._quick_evaluation(prompt)
            else:
                raise ValueError(f"不支持的评估模式: {mode}")
            
            processing_time = time.time() - start_time
            
            # 构建详细评分
            detailed_scores = {}
            if 'scores' in result:
                for criterion, score in result['scores'].items():
                    if hasattr(QualityCriterion, criterion.upper()):
                        quality_criterion = QualityCriterion(criterion)
                        detailed_scores[criterion] = QualityScore(
                            criterion=quality_criterion,
                            score=float(score),
                            description=self.evaluation_criteria[quality_criterion]
                        )
            
            return QualityReport(
                overall_score=float(result.get('overall_score', 5.0)),
                detailed_scores=detailed_scores,
                issues=result.get('issues', []),
                suggestions=result.get('suggestions', []),
                strengths=result.get('strengths', []),
                processing_time=processing_time
            )
            
        except Exception as e:
            # 返回默认的错误报告
            processing_time = time.time() - start_time
            return QualityReport(
                overall_score=5.0,
                detailed_scores={},
                issues=[f"评估过程出错: {str(e)}"],
                suggestions=["请检查提示词内容并重试"],
                strengths=[],
                processing_time=processing_time
            )
    
    async def _comprehensive_evaluation(self, prompt: str) -> Dict[str, Any]:
        """全面评估"""
        template = self.evaluation_templates["comprehensive"]
        evaluation_prompt = template.format(prompt=prompt)
        
        messages = [
            {
                "role": "system", 
                "content": "你是一个专业的提示词质量评估专家。请严格按照JSON格式进行评估，确保评分客观准确。"
            },
            {
                "role": "user", 
                "content": evaluation_prompt
            }
        ]
        
        response = await self.ai_client._make_request_with_retry(messages, temperature=0.3)
        content = response.choices[0].message.content
        
        return self._parse_evaluation_result(content)
    
    async def _quick_evaluation(self, prompt: str) -> Dict[str, Any]:
        """快速评估"""
        template = self.evaluation_templates["quick"]
        evaluation_prompt = template.format(prompt=prompt)
        
        messages = [
            {
                "role": "system", 
                "content": "你是一个提示词质量评估专家。请快速评估并以JSON格式返回。"
            },
            {
                "role": "user", 
                "content": evaluation_prompt
            }
        ]
        
        response = await self.ai_client._make_request_with_retry(messages, temperature=0.3)
        content = response.choices[0].message.content
        
        result = self._parse_evaluation_result(content)
        
        # 将快速评估结果转换为标准格式
        if 'brief_analysis' in result:
            result['issues'] = result.get('main_issues', [])
            result['suggestions'] = result.get('quick_suggestions', [])
            result['strengths'] = []
            # 为快速评估生成基本的详细评分
            overall = result.get('overall_score', 5)
            result['scores'] = {
                'clarity': overall,
                'completeness': overall,
                'structure': overall,
                'specificity': overall,
                'actionability': overall
            }
        
        return result
    
    def _parse_evaluation_result(self, content: str) -> Dict[str, Any]:
        """解析评估结果"""
        try:
            import json
            
            # 提取JSON部分
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
            elif "{" in content and "}" in content:
                start = content.find("{")
                end = content.rfind("}") + 1
                json_str = content[start:end]
            else:
                json_str = content
            
            result = json.loads(json_str)
            return result
            
        except Exception as e:
            # 如果解析失败，返回默认结果
            return {
                "scores": {
                    "clarity": 5,
                    "completeness": 5,
                    "structure": 5,
                    "specificity": 5,
                    "actionability": 5
                },
                "overall_score": 5,
                "issues": ["无法准确解析评估结果"],
                "suggestions": ["请重新提交评估请求"],
                "strengths": []
            }
    
    async def evaluate_by_criterion(self, prompt: str, criterion: QualityCriterion) -> QualityScore:
        """按单一标准评估"""
        criterion_description = self.evaluation_criteria[criterion]
        
        evaluation_prompt = f"""
请专门从"{criterion.value}"的角度评估以下提示词：

提示词：{prompt}

评估标准：{criterion_description}

请给出1-10分的评分，并简要说明理由。
返回JSON格式：
{{
    "score": 8,
    "reasoning": "评分理由"
}}
"""
        
        messages = [
            {
                "role": "system", 
                "content": "你是一个提示词质量评估专家。请专注于指定的评估维度。"
            },
            {
                "role": "user", 
                "content": evaluation_prompt
            }
        ]
        
        try:
            response = await self.ai_client._make_request_with_retry(messages, temperature=0.3)
            content = response.choices[0].message.content
            result = self._parse_evaluation_result(content)
            
            return QualityScore(
                criterion=criterion,
                score=float(result.get('score', 5)),
                description=result.get('reasoning', criterion_description)
            )
            
        except Exception:
            return QualityScore(
                criterion=criterion,
                score=5.0,
                description=f"评估{criterion.value}时出错"
            )
    
    async def compare_prompts(self, prompt1: str, prompt2: str) -> Dict[str, Any]:
        """比较两个提示词的质量"""
        report1 = await self.evaluate(prompt1)
        report2 = await self.evaluate(prompt2)
        
        # 计算改进度
        score_improvement = report2.overall_score - report1.overall_score
        
        detailed_comparison = {}
        for criterion in report1.detailed_scores:
            if criterion in report2.detailed_scores:
                diff = report2.detailed_scores[criterion].score - report1.detailed_scores[criterion].score
                detailed_comparison[criterion] = {
                    "before": report1.detailed_scores[criterion].score,
                    "after": report2.detailed_scores[criterion].score,
                    "improvement": diff,
                    "improvement_percentage": (diff / 10.0) * 100
                }
        
        return {
            "overall_improvement": score_improvement,
            "overall_improvement_percentage": (score_improvement / 10.0) * 100,
            "detailed_comparison": detailed_comparison,
            "report_before": report1,
            "report_after": report2,
            "recommendation": self._get_comparison_recommendation(score_improvement)
        }
    
    def _get_comparison_recommendation(self, improvement: float) -> str:
        """获取比较建议"""
        if improvement >= 2:
            return "显著改进：优化效果很好，建议采用优化后的版本"
        elif improvement >= 1:
            return "明显改进：优化有效，建议采用优化后的版本"
        elif improvement >= 0.5:
            return "轻微改进：有一定优化效果，可以考虑采用"
        elif improvement >= -0.5:
            return "基本相当：两个版本质量相近，可根据其他因素选择"
        else:
            return "质量下降：建议保持原版本或进一步优化"
    
    async def get_improvement_suggestions(self, prompt: str) -> List[Dict[str, Any]]:
        """获取详细的改进建议"""
        report = await self.evaluate(prompt)
        
        suggestions = []
        
        # 基于各维度评分提供建议
        for criterion_name, score_obj in report.detailed_scores.items():
            if score_obj.score < 7:
                suggestions.append({
                    "criterion": criterion_name,
                    "current_score": score_obj.score,
                    "target_score": 8.0,
                    "priority": "高" if score_obj.score < 5 else "中",
                    "suggestions": await self._get_criterion_suggestions(prompt, score_obj.criterion)
                })
        
        return suggestions
    
    async def _get_criterion_suggestions(self, prompt: str, criterion: QualityCriterion) -> List[str]:
        """获取特定标准的改进建议"""
        # 这里可以基于不同标准提供具体建议
        general_suggestions = {
            QualityCriterion.CLARITY: [
                "使用更明确的动词和名词",
                "避免使用模糊或歧义的表述",
                "将复杂指令分解为简单步骤"
            ],
            QualityCriterion.COMPLETENESS: [
                "添加必要的背景信息",
                "说明期望的输出格式",
                "包含相关的约束条件"
            ],
            QualityCriterion.STRUCTURE: [
                "使用编号或标记组织内容",
                "按逻辑顺序排列指令",
                "使用段落分隔不同部分"
            ],
            QualityCriterion.SPECIFICITY: [
                "提供具体的例子",
                "明确数量、时间等具体要求",
                "详细说明操作步骤"
            ],
            QualityCriterion.ACTIONABILITY: [
                "确保指令可操作",
                "提供足够的信息让AI执行",
                "避免过于抽象的要求"
            ]
        }
        
        return general_suggestions.get(criterion, ["继续优化这个维度"]) 