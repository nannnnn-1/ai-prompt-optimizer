"""
提示词分析器模块
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import re
import time

from .ai_client import AIClient


class PromptType(Enum):
    """提示词类型"""
    GENERAL = "general"
    CODE = "code"
    WRITING = "writing"
    ANALYSIS = "analysis"
    CREATIVE = "creative"
    INSTRUCTION = "instruction"
    QUESTION = "question"


class ComplexityLevel(Enum):
    """复杂度级别"""
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"


@dataclass
class PromptFeatures:
    """提示词特征"""
    word_count: int
    sentence_count: int
    avg_sentence_length: float
    question_count: int
    imperative_count: int
    technical_terms: List[str]
    has_examples: bool
    has_constraints: bool
    has_context: bool
    readability_score: float


@dataclass
class PromptStructure:
    """提示词结构"""
    has_clear_goal: bool
    has_context: bool
    has_instructions: bool
    has_examples: bool
    has_constraints: bool
    has_output_format: bool
    structure_score: float
    missing_elements: List[str]


@dataclass
class AnalysisResult:
    """分析结果"""
    prompt_type: PromptType
    complexity_level: ComplexityLevel
    features: PromptFeatures
    structure: PromptStructure
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    processing_time: float


class PromptAnalyzer:
    """提示词分析器"""
    
    def __init__(self, ai_client: Optional[AIClient] = None):
        self.ai_client = ai_client
        self.technical_terms_patterns = self._load_technical_patterns()
        self.structure_patterns = self._load_structure_patterns()
    
    def _load_technical_patterns(self) -> Dict[str, List[str]]:
        """加载技术术语模式"""
        return {
            "programming": [
                r"\b(function|class|method|variable|array|object|string|integer|boolean)\b",
                r"\b(python|javascript|java|c\+\+|html|css|sql|api|json|xml)\b",
                r"\b(algorithm|data structure|database|framework|library)\b"
            ],
            "data_analysis": [
                r"\b(data|dataset|analysis|statistics|correlation|regression)\b",
                r"\b(chart|graph|visualization|metrics|kpi|trend)\b",
                r"\b(pandas|numpy|matplotlib|sql|excel|csv)\b"
            ],
            "writing": [
                r"\b(article|essay|blog|content|copy|narrative|story)\b",
                r"\b(tone|style|audience|voice|structure|format)\b",
                r"\b(introduction|conclusion|paragraph|thesis|argument)\b"
            ],
            "academic": [
                r"\b(research|study|theory|hypothesis|methodology|analysis)\b",
                r"\b(citation|reference|literature|review|paper|journal)\b",
                r"\b(abstract|conclusion|findings|results|discussion)\b"
            ]
        }
    
    def _load_structure_patterns(self) -> Dict[str, str]:
        """加载结构模式"""
        return {
            "goal_indicators": r"\b(create|write|generate|analyze|explain|describe|calculate|solve|design|build)\b",
            "context_indicators": r"\b(given|assuming|in the context of|considering|based on|for)\b",
            "instruction_indicators": r"\b(please|should|must|need to|required|ensure|make sure)\b",
            "example_indicators": r"\b(for example|such as|like|including|instance|sample)\b",
            "constraint_indicators": r"\b(limit|maximum|minimum|no more than|at least|within|between)\b",
            "format_indicators": r"\b(format|structure|organize|layout|arrange|present as)\b"
        }
    
    async def analyze(self, prompt: str, use_ai: bool = True) -> AnalysisResult:
        """
        分析提示词
        
        Args:
            prompt: 要分析的提示词
            use_ai: 是否使用AI进行深度分析
            
        Returns:
            分析结果
        """
        start_time = time.time()
        
        # 基础特征分析
        features = self._analyze_features(prompt)
        
        # 结构分析
        structure = self._analyze_structure(prompt)
        
        # 类型识别
        prompt_type = self._identify_type(prompt, features)
        
        # 复杂度评估
        complexity_level = self._assess_complexity(prompt, features, structure)
        
        # 优缺点分析
        strengths, weaknesses = self._analyze_strengths_weaknesses(features, structure)
        
        # 改进建议
        suggestions = self._generate_suggestions(features, structure, weaknesses)
        
        # AI深度分析（可选）
        if use_ai and self.ai_client:
            ai_insights = await self._ai_analysis(prompt)
            strengths.extend(ai_insights.get('strengths', []))
            weaknesses.extend(ai_insights.get('weaknesses', []))
            suggestions.extend(ai_insights.get('suggestions', []))
        
        processing_time = time.time() - start_time
        
        return AnalysisResult(
            prompt_type=prompt_type,
            complexity_level=complexity_level,
            features=features,
            structure=structure,
            strengths=list(set(strengths)),  # 去重
            weaknesses=list(set(weaknesses)),
            suggestions=list(set(suggestions)),
            processing_time=processing_time
        )
    
    def _analyze_features(self, prompt: str) -> PromptFeatures:
        """分析提示词特征"""
        # 基础统计
        words = prompt.split()
        sentences = re.split(r'[.!?]+', prompt)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        word_count = len(words)
        sentence_count = len(sentences)
        avg_sentence_length = word_count / max(sentence_count, 1)
        
        # 问句和祈使句计数
        question_count = len(re.findall(r'\?', prompt))
        imperative_pattern = r'\b(please|write|create|make|do|generate|analyze|explain|describe)\b'
        imperative_count = len(re.findall(imperative_pattern, prompt.lower()))
        
        # 技术术语识别
        technical_terms = self._identify_technical_terms(prompt)
        
        # 结构元素检测
        has_examples = bool(re.search(r'\b(example|for instance|such as|like)\b', prompt.lower()))
        has_constraints = bool(re.search(r'\b(limit|maximum|minimum|within|between)\b', prompt.lower()))
        has_context = bool(re.search(r'\b(given|assuming|context|background|scenario)\b', prompt.lower()))
        
        # 可读性评分 (简化版本)
        readability_score = self._calculate_readability(prompt, avg_sentence_length, word_count)
        
        return PromptFeatures(
            word_count=word_count,
            sentence_count=sentence_count,
            avg_sentence_length=avg_sentence_length,
            question_count=question_count,
            imperative_count=imperative_count,
            technical_terms=technical_terms,
            has_examples=has_examples,
            has_constraints=has_constraints,
            has_context=has_context,
            readability_score=readability_score
        )
    
    def _analyze_structure(self, prompt: str) -> PromptStructure:
        """分析提示词结构"""
        prompt_lower = prompt.lower()
        
        # 检测结构元素
        has_clear_goal = bool(re.search(self.structure_patterns["goal_indicators"], prompt_lower))
        has_context = bool(re.search(self.structure_patterns["context_indicators"], prompt_lower))
        has_instructions = bool(re.search(self.structure_patterns["instruction_indicators"], prompt_lower))
        has_examples = bool(re.search(self.structure_patterns["example_indicators"], prompt_lower))
        has_constraints = bool(re.search(self.structure_patterns["constraint_indicators"], prompt_lower))
        has_output_format = bool(re.search(self.structure_patterns["format_indicators"], prompt_lower))
        
        # 计算结构评分
        structure_elements = [
            has_clear_goal, has_context, has_instructions, 
            has_examples, has_constraints, has_output_format
        ]
        structure_score = sum(structure_elements) / len(structure_elements) * 10
        
        # 识别缺失元素
        missing_elements = []
        if not has_clear_goal:
            missing_elements.append("明确的目标")
        if not has_context:
            missing_elements.append("上下文信息")
        if not has_instructions:
            missing_elements.append("具体指令")
        if not has_examples:
            missing_elements.append("示例说明")
        if not has_constraints:
            missing_elements.append("约束条件")
        if not has_output_format:
            missing_elements.append("输出格式")
        
        return PromptStructure(
            has_clear_goal=has_clear_goal,
            has_context=has_context,
            has_instructions=has_instructions,
            has_examples=has_examples,
            has_constraints=has_constraints,
            has_output_format=has_output_format,
            structure_score=structure_score,
            missing_elements=missing_elements
        )
    
    def _identify_technical_terms(self, prompt: str) -> List[str]:
        """识别技术术语"""
        prompt_lower = prompt.lower()
        technical_terms = []
        
        for category, patterns in self.technical_terms_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, prompt_lower)
                technical_terms.extend(matches)
        
        return list(set(technical_terms))  # 去重
    
    def _identify_type(self, prompt: str, features: PromptFeatures) -> PromptType:
        """识别提示词类型"""
        prompt_lower = prompt.lower()
        
        # 编程相关
        if any(term in features.technical_terms for term in ['python', 'javascript', 'function', 'code', 'api']):
            return PromptType.CODE
        
        # 写作相关
        if any(word in prompt_lower for word in ['write', 'article', 'essay', 'content', 'story']):
            return PromptType.WRITING
        
        # 分析相关
        if any(word in prompt_lower for word in ['analyze', 'analysis', 'data', 'statistics', 'evaluate']):
            return PromptType.ANALYSIS
        
        # 创意相关
        if any(word in prompt_lower for word in ['creative', 'imagine', 'brainstorm', 'invent', 'design']):
            return PromptType.CREATIVE
        
        # 问题相关
        if features.question_count > 0:
            return PromptType.QUESTION
        
        # 指令相关
        if features.imperative_count > 0:
            return PromptType.INSTRUCTION
        
        return PromptType.GENERAL
    
    def _assess_complexity(self, prompt: str, features: PromptFeatures, structure: PromptStructure) -> ComplexityLevel:
        """评估复杂度"""
        complexity_score = 0
        
        # 长度影响
        if features.word_count > 100:
            complexity_score += 2
        elif features.word_count > 50:
            complexity_score += 1
        
        # 句子复杂度
        if features.avg_sentence_length > 20:
            complexity_score += 2
        elif features.avg_sentence_length > 15:
            complexity_score += 1
        
        # 技术术语
        if len(features.technical_terms) > 5:
            complexity_score += 2
        elif len(features.technical_terms) > 2:
            complexity_score += 1
        
        # 结构复杂度
        if structure.structure_score > 8:
            complexity_score += 2
        elif structure.structure_score > 6:
            complexity_score += 1
        
        # 多任务
        task_indicators = len(re.findall(r'\b(and|also|additionally|furthermore|moreover)\b', prompt.lower()))
        if task_indicators > 3:
            complexity_score += 2
        elif task_indicators > 1:
            complexity_score += 1
        
        # 映射到复杂度级别
        if complexity_score >= 8:
            return ComplexityLevel.VERY_COMPLEX
        elif complexity_score >= 6:
            return ComplexityLevel.COMPLEX
        elif complexity_score >= 3:
            return ComplexityLevel.MEDIUM
        else:
            return ComplexityLevel.SIMPLE
    
    def _calculate_readability(self, prompt: str, avg_sentence_length: float, word_count: int) -> float:
        """计算可读性评分（简化版Flesch读易性测试）"""
        # 简化的可读性计算
        if word_count == 0:
            return 0
        
        # 计算平均音节数（简化：假设每个单词平均1.5个音节）
        avg_syllables_per_word = 1.5
        
        # Flesch公式的简化版本
        readability = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        
        # 标准化到0-10分
        if readability >= 90:
            return 10
        elif readability >= 80:
            return 9
        elif readability >= 70:
            return 8
        elif readability >= 60:
            return 7
        elif readability >= 50:
            return 6
        elif readability >= 30:
            return 5
        else:
            return max(0, readability / 30 * 5)
    
    def _analyze_strengths_weaknesses(self, features: PromptFeatures, structure: PromptStructure) -> tuple[List[str], List[str]]:
        """分析优缺点"""
        strengths = []
        weaknesses = []
        
        # 分析优点
        if features.word_count >= 20:
            strengths.append("提示词长度适中，包含足够信息")
        if features.has_examples:
            strengths.append("包含示例，有助于理解")
        if features.has_constraints:
            strengths.append("有明确的约束条件")
        if features.has_context:
            strengths.append("提供了上下文信息")
        if structure.has_clear_goal:
            strengths.append("目标明确")
        if structure.structure_score >= 7:
            strengths.append("结构清晰完整")
        if features.readability_score >= 7:
            strengths.append("可读性良好")
        
        # 分析缺点
        if features.word_count < 10:
            weaknesses.append("提示词过于简短，信息不足")
        if features.word_count > 200:
            weaknesses.append("提示词过长，可能影响理解")
        if not features.has_examples and features.word_count < 30:
            weaknesses.append("缺少示例说明")
        if not structure.has_clear_goal:
            weaknesses.append("目标不够明确")
        if structure.structure_score < 5:
            weaknesses.append("结构不够完整")
        if features.readability_score < 5:
            weaknesses.append("可读性需要改进")
        if features.avg_sentence_length > 25:
            weaknesses.append("句子过长，影响理解")
        
        return strengths, weaknesses
    
    def _generate_suggestions(self, features: PromptFeatures, structure: PromptStructure, weaknesses: List[str]) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        # 基于缺失的结构元素
        if structure.missing_elements:
            suggestions.extend([f"建议添加{element}" for element in structure.missing_elements])
        
        # 基于特征分析
        if features.word_count < 10:
            suggestions.append("增加更多详细信息和说明")
        if features.word_count > 200:
            suggestions.append("简化表述，突出重点")
        if not features.has_examples:
            suggestions.append("添加具体示例帮助理解")
        if features.avg_sentence_length > 25:
            suggestions.append("将长句拆分为短句")
        if features.readability_score < 6:
            suggestions.append("使用更简单的词汇和表达")
        
        # 基于缺点
        for weakness in weaknesses:
            if "目标不够明确" in weakness:
                suggestions.append("明确说明期望的输出或结果")
            elif "结构不够完整" in weakness:
                suggestions.append("按照逻辑顺序组织内容")
        
        return suggestions
    
    async def _ai_analysis(self, prompt: str) -> Dict[str, Any]:
        """AI深度分析"""
        if not self.ai_client:
            return {}
        
        analysis_prompt = f"""
请深度分析以下提示词的特点：

提示词：{prompt}

请从以下角度进行分析：
1. 主要优点（最多3个）
2. 主要缺点（最多3个）
3. 改进建议（最多3个）

返回JSON格式：
{{
    "strengths": ["优点1", "优点2", "优点3"],
    "weaknesses": ["缺点1", "缺点2", "缺点3"],
    "suggestions": ["建议1", "建议2", "建议3"]
}}
"""
        
        messages = [
            {
                "role": "system",
                "content": "你是一个专业的提示词分析专家。请提供客观、具体的分析。"
            },
            {
                "role": "user",
                "content": analysis_prompt
            }
        ]
        
        try:
            response = await self.ai_client._make_request_with_retry(messages, temperature=0.3)
            content = response.choices[0].message.content
            
            import json
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
            elif "{" in content and "}" in content:
                start = content.find("{")
                end = content.rfind("}") + 1
                json_str = content[start:end]
            else:
                json_str = content
            
            return json.loads(json_str)
            
        except Exception:
            return {}
    
    def get_analysis_summary(self, result: AnalysisResult) -> str:
        """获取分析摘要"""
        return f"""
提示词分析摘要：
- 类型：{result.prompt_type.value}
- 复杂度：{result.complexity_level.value}
- 字数：{result.features.word_count}
- 结构评分：{result.structure.structure_score:.1f}/10
- 可读性：{result.features.readability_score:.1f}/10
- 主要优点：{len(result.strengths)}个
- 需改进点：{len(result.weaknesses)}个
- 改进建议：{len(result.suggestions)}个
""" 