"""
自定义异常类
"""

from typing import Any, Dict, Optional


class PromptOptimizerException(Exception):
    """基础异常类"""
    
    def __init__(
        self, 
        message: str, 
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code or "UNKNOWN_ERROR"
        self.details = details or {}
        super().__init__(self.message)


class ValidationException(PromptOptimizerException):
    """数据验证异常"""
    
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            details={"field": field} if field else {}
        )


class DatabaseException(PromptOptimizerException):
    """数据库操作异常"""
    
    def __init__(self, message: str, operation: Optional[str] = None):
        super().__init__(
            message=message,
            error_code="DATABASE_ERROR",
            details={"operation": operation} if operation else {}
        )


class AIServiceException(PromptOptimizerException):
    """AI服务异常"""
    
    def __init__(self, message: str, service: Optional[str] = None):
        super().__init__(
            message=message,
            error_code="AI_SERVICE_ERROR",
            details={"service": service} if service else {}
        )


class OptimizationException(PromptOptimizerException):
    """提示词优化异常"""
    
    def __init__(self, message: str, prompt: Optional[str] = None):
        super().__init__(
            message=message,
            error_code="OPTIMIZATION_ERROR",
            details={"prompt": prompt[:100] + "..." if prompt and len(prompt) > 100 else prompt} if prompt else {}
        )


class AuthenticationException(PromptOptimizerException):
    """认证异常"""
    
    def __init__(self, message: str = "认证失败"):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR"
        )


class AuthorizationException(PromptOptimizerException):
    """授权异常"""
    
    def __init__(self, message: str = "权限不足"):
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR"
        )


class OptimizationFailedException(PromptOptimizerException):
    """优化失败异常"""
    pass


class ResourceNotFoundException(PromptOptimizerException):
    """资源未找到异常"""
    pass 