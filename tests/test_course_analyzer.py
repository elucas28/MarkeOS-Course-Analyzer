import pytest
from fastapi.testclient import TestClient
from .course_analyzer import CourseAnalyzer, CourseAnalysisRequest

@pytest.fixture
def client():
    analyzer = CourseAnalyzer()
    return TestClient(analyzer.app)

@pytest.fixture
def sample_course_request():
    return {
        "course_name": "Marketing Digital Avançado",
        "problem_solved": "Profissionais que precisam melhorar suas habilidades em marketing digital",
        "target_audience": "Profissionais de marketing, empreendedores e gestores",
        "marketing_budget": 5000.0,
        "course_format": "online",
        "duration": "8 semanas",
        "initial_description": "Curso completo abordando as principais estratégias de marketing digital",
        "market_analysis": True
    }

def test_analyze_course_endpoint(client, sample_course_request):
    """Testa o endpoint de análise de curso"""
    response = client.post("/analyze-course", json=sample_course_request)
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "PENDING"

def test_get_task_status(client, sample_course_request):
    """Testa o endpoint de status da tarefa"""
    # Primeiro cria uma tarefa
    response = client.post("/analyze-course", json=sample_course_request)
    task_id = response.json()["task_id"]
    
    # Então verifica o status
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data

def test_invalid_task_id(client):
    """Testa a resposta para um ID de tarefa inválido"""
    response = client.get("/tasks/invalid-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_invalid_course_request(client):
    """Testa a validação dos dados do curso"""
    invalid_request = {
        "course_name": "Teste",
        # Omitindo campos obrigatórios
    }
    response = client.post("/analyze-course", json=invalid_request)
    assert response.status_code == 422  # Erro de validação

def test_course_analysis_request_model():
    """Testa a validação do modelo CourseAnalysisRequest"""
    valid_data = {
        "course_name": "Teste",
        "problem_solved": "Problema teste",
        "target_audience": "Público teste",
        "marketing_budget": 1000.0,
        "course_format": "online",
        "duration": "4 semanas",
        "initial_description": "Descrição teste"
    }
    request = CourseAnalysisRequest(**valid_data)
    assert request.course_name == "Teste"
    assert request.marketing_budget == 1000.0
    assert request.market_analysis is True  # Valor padrão