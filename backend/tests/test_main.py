"""
主应用测试
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """测试客户端"""
    return TestClient(app)


def test_root_endpoint(client: TestClient):
    """测试根路径"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["version"] == "1.0.0"


def test_simple_health_check(client: TestClient):
    """测试简单健康检查"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_api_health_check(client: TestClient):
    """测试API健康检查"""
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data


def test_database_health_check(client: TestClient):
    """测试数据库健康检查"""
    response = client.get("/api/v1/health/db")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database" in data


def test_detailed_health_check(client: TestClient):
    """测试详细健康检查"""
    response = client.get("/api/v1/health/detailed")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "components" in data
    assert "database" in data["components"]
    assert "configuration" in data["components"]


def test_api_docs_available_in_debug():
    """测试API文档在调试模式下可用"""
    # 当DEBUG=True时，docs应该可用
    client = TestClient(app)
    response = client.get("/docs")
    # 在测试环境中，这应该返回200或重定向
    assert response.status_code in [200, 307] 