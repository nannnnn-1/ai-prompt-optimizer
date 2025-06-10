import os
import asyncio
import tiktoken
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

from ..config import settings
from ..utils.exceptions import AIServiceException


@dataclass
class AIUsageStats:
    """AI使用统计"""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost_estimate: float = 0.0


@dataclass
class OptimizationResult:
    """优化结果"""
    optimized_prompt: str
    improvements: List[Dict[str, str]]
    quality_score_before: int
    quality_score_after: int
    usage_stats: AIUsageStats
    processing_time: float


class AIClient:
    """AI服务客户端"""
    
    def __init__(self):
        self.client = None
        self.model = settings.OPENAI_MODEL
        self.encoding = None
        
        # 定价（每1K tokens的价格，以USD为单位）
        self.pricing = {
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "Qwen/Qwen2.5-7B-Instruct": {"input": 0.0007, "output": 0.0007},  # 硅基流动qwen价格
            "Qwen/Qwen2.5-14B-Instruct": {"input": 0.0014, "output": 0.0014},
            "Qwen/Qwen2.5-32B-Instruct": {"input": 0.0021, "output": 0.0021},
            "Qwen/Qwen2.5-72B-Instruct": {"input": 0.0056, "output": 0.0056}
        }
    
    def _ensure_client_initialized(self):
        """确保客户端已初始化"""
        if self.client is None:
            if not settings.OPENAI_API_KEY:
                raise AIServiceException("OpenAI API Key未配置，请设置OPENAI_API_KEY环境变量")
            
            self.client = AsyncOpenAI(
                api_key=settings.OPENAI_API_KEY,
                base_url=settings.OPENAI_BASE_URL
            )
            
        if self.encoding is None:
            try:
                # 对于qwen模型，使用通用编码
                if "Qwen" in self.model:
                    self.encoding = tiktoken.get_encoding("cl100k_base")
                else:
                    self.encoding = tiktoken.encoding_for_model(self.model)
            except Exception:
                # 如果获取编码失败，使用默认编码
                self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        """计算文本的token数量"""
        try:
            self._ensure_client_initialized()
            return len(self.encoding.encode(text))
        except Exception:
            # 如果编码失败，使用简单估算
            return len(text) // 4
    
    def estimate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """估算API调用成本"""
        model_pricing = self.pricing.get(self.model, {"input": 0.002, "output": 0.002})
        
        input_cost = (prompt_tokens / 1000) * model_pricing["input"]
        output_cost = (completion_tokens / 1000) * model_pricing["output"]
        
        return input_cost + output_cost
    
    async def _make_request_with_retry(
        self, 
        messages: List[Dict[str, str]], 
        max_retries: int = 3,
        temperature: float = 0.7
    ) -> ChatCompletion:
        """带重试机制的API请求"""
        self._ensure_client_initialized()
        last_exception = None
        
        for attempt in range(max_retries):
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=1500
                )
                return response
            except Exception as e:
                last_exception = e
                if attempt < max_retries - 1:
                    # 指数退避
                    wait_time = 2 ** attempt
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    break
        
        raise AIServiceException(f"AI服务请求失败: {str(last_exception)}")
    
    async def analyze_prompt_quality(self, prompt: str) -> Dict[str, Any]:
        """分析提示词质量"""
        
        analysis_prompt = f"""
请分析以下提示词的质量，从以下几个维度评分（1-10分）：

提示词：{prompt}

评估维度：
1. 清晰度 - 指令是否明确易懂
2. 完整性 - 是否包含必要的上下文信息
3. 结构性 - 逻辑结构是否清晰
4. 具体性 - 是否足够具体详细
5. 可执行性 - AI是否能够有效执行

请返回JSON格式结果，包含：
- 各维度评分
- 总体评分
- 主要问题列表
- 改进建议

JSON格式：
{{
    "scores": {{
        "clarity": 8,
        "completeness": 7,
        "structure": 6,
        "specificity": 8,
        "actionability": 9
    }},
    "overall_score": 8,
    "issues": ["问题1", "问题2"],
    "suggestions": ["建议1", "建议2"]
}}
"""
        
        messages = [
            {"role": "system", "content": "你是一个专业的提示词质量评估专家。请严格按照JSON格式回复。"},
            {"role": "user", "content": analysis_prompt}
        ]
        
        start_time = time.time()
        response = await self._make_request_with_retry(messages, temperature=0.3)
        processing_time = time.time() - start_time
        
        try:
            import json
            content = response.choices[0].message.content
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
            result["processing_time"] = processing_time
            
            return result
        except Exception as e:
            # 如果JSON解析失败，返回默认结果
            return {
                "scores": {
                    "clarity": 5,
                    "completeness": 5,
                    "structure": 5,
                    "specificity": 5,
                    "actionability": 5
                },
                "overall_score": 5,
                "issues": ["无法准确分析提示词质量"],
                "suggestions": ["请提供更清晰的提示词"],
                "processing_time": processing_time
            }
    
    async def optimize_prompt(self, original_prompt: str, optimization_type: str = "general") -> OptimizationResult:
        """优化提示词"""
        
        start_time = time.time()
        
        # 1. 分析原始提示词质量
        analysis = await self.analyze_prompt_quality(original_prompt)
        
        # 2. 生成优化提示词
        optimization_prompt = self._create_optimization_prompt(original_prompt, optimization_type, analysis)
        
        messages = [
            {"role": "system", "content": "你是一个专业的提示词优化专家。请帮助用户优化提示词，使其更加清晰、完整、具体和有效。"},
            {"role": "user", "content": optimization_prompt}
        ]
        
        response = await self._make_request_with_retry(messages, temperature=0.7)
        
        # 3. 解析优化结果
        optimized_content = response.choices[0].message.content
        optimized_prompt, improvements = self._parse_optimization_result(optimized_content)
        
        # 4. 分析优化后的质量
        optimized_analysis = await self.analyze_prompt_quality(optimized_prompt)
        
        # 5. 计算使用统计
        prompt_tokens = sum([self.count_tokens(msg["content"]) for msg in messages])
        completion_tokens = self.count_tokens(optimized_content)
        total_tokens = prompt_tokens + completion_tokens
        cost_estimate = self.estimate_cost(prompt_tokens, completion_tokens)
        
        usage_stats = AIUsageStats(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cost_estimate=cost_estimate
        )
        
        processing_time = time.time() - start_time
        
        return OptimizationResult(
            optimized_prompt=optimized_prompt,
            improvements=improvements,
            quality_score_before=analysis.get("overall_score", 5),
            quality_score_after=optimized_analysis.get("overall_score", 5),
            usage_stats=usage_stats,
            processing_time=processing_time
        )
    
    def _create_optimization_prompt(self, original_prompt: str, optimization_type: str, analysis: Dict) -> str:
        """创建优化提示词"""
        base_prompt = f"""
请优化以下提示词，使其更加有效：

原始提示词：
{original_prompt}

质量分析结果：
- 清晰度：{analysis.get('scores', {}).get('clarity', 5)}/10
- 完整性：{analysis.get('scores', {}).get('completeness', 5)}/10  
- 结构性：{analysis.get('scores', {}).get('structure', 5)}/10
- 具体性：{analysis.get('scores', {}).get('specificity', 5)}/10
- 可执行性：{analysis.get('scores', {}).get('actionability', 5)}/10

主要问题：{', '.join(analysis.get('issues', []))}

优化要求：
1. 针对识别出的问题进行改进
2. 保持原始意图不变
3. 增强清晰度和具体性
4. 改善逻辑结构
5. 确保AI可以有效执行

请返回以下格式的结果：

优化后的提示词：
[在这里写优化后的完整提示词]

改进说明：
1. [改进点1：具体说明改进内容]
2. [改进点2：具体说明改进内容]
3. [改进点3：具体说明改进内容]
"""
        
        # 根据优化类型添加特定要求
        if optimization_type == "code":
            base_prompt += "\n\n特别注意：这是代码相关的提示词，请确保包含具体的编程要求、技术规范和预期输出格式。"
        elif optimization_type == "writing":
            base_prompt += "\n\n特别注意：这是写作相关的提示词，请确保包含文体要求、目标受众、风格指导和结构要求。"
        elif optimization_type == "analysis":
            base_prompt += "\n\n特别注意：这是分析相关的提示词，请确保包含分析框架、评估标准、数据要求和输出格式。"
        
        return base_prompt
    
    def _parse_optimization_result(self, content: str) -> tuple[str, List[Dict[str, str]]]:
        """解析优化结果"""
        lines = content.strip().split('\n')
        
        optimized_prompt = ""
        improvements = []
        
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            
            if "优化后的提示词" in line:
                current_section = "prompt"
                current_content = []
            elif "改进说明" in line:
                if current_section == "prompt":
                    optimized_prompt = '\n'.join(current_content).strip()
                current_section = "improvements"
                current_content = []
            elif line.startswith(('1.', '2.', '3.', '4.', '5.', '-', '•')):
                if current_section == "improvements":
                    improvement_text = line.lstrip('1234567890.-• ').strip()
                    if ':' in improvement_text:
                        type_part, desc_part = improvement_text.split(':', 1)
                        improvements.append({
                            "type": type_part.strip(),
                            "description": desc_part.strip()
                        })
                    else:
                        improvements.append({
                            "type": "改进",
                            "description": improvement_text
                        })
            elif line and current_section:
                current_content.append(line)
        
        # 处理最后一个部分
        if current_section == "prompt" and not optimized_prompt:
            optimized_prompt = '\n'.join(current_content).strip()
        
        # 如果解析失败，使用整个内容作为优化结果
        if not optimized_prompt:
            optimized_prompt = content.strip()
        
        # 如果没有解析到改进说明，创建默认的
        if not improvements:
            improvements = [
                {"type": "整体优化", "description": "提升了提示词的清晰度和可执行性"}
            ]
        
        return optimized_prompt, improvements
    
    async def batch_optimize(self, prompts: List[str], optimization_type: str = "general") -> List[OptimizationResult]:
        """批量优化提示词"""
        tasks = [self.optimize_prompt(prompt, optimization_type) for prompt in prompts]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理异常结果
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                # 创建错误结果
                error_result = OptimizationResult(
                    optimized_prompt=prompts[i],
                    improvements=[{"type": "错误", "description": f"优化失败: {str(result)}"}],
                    quality_score_before=0,
                    quality_score_after=0,
                    usage_stats=AIUsageStats(),
                    processing_time=0.0
                )
                final_results.append(error_result)
            else:
                final_results.append(result)
        
        return final_results
    
    async def get_optimization_suggestions(self, prompt: str) -> List[str]:
        """获取优化建议（不执行实际优化）"""
        analysis = await self.analyze_prompt_quality(prompt)
        return analysis.get("suggestions", [])
    
    async def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        try:
            # 如果没有配置API key，返回配置缺失状态
            if not settings.OPENAI_API_KEY:
                return {
                    "status": "configuration_missing",
                    "model": self.model,
                    "error": "OpenAI API Key未配置",
                    "api_available": False
                }
            
            test_messages = [
                {"role": "user", "content": "Hello"}
            ]
            
            start_time = time.time()
            response = await self._make_request_with_retry(test_messages, max_retries=1)
            response_time = time.time() - start_time
            
            return {
                "status": "healthy",
                "model": self.model,
                "response_time": response_time,
                "api_available": True
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "model": self.model,
                "error": str(e),
                "api_available": False
            }


# 全局AI客户端实例
ai_client = AIClient() 