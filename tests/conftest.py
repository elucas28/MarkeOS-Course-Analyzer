import pytest
import os
from dotenv import load_dotenv
from unittest.mock import AsyncMock, patch

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

@pytest.fixture(autouse=True)
def mock_openhouter_client():
    """
    Mock do cliente OpenHouter para testes.
    Simula respostas da API sem fazer chamadas reais.
    """
    with patch('markeos.course_analyzer.OpenHouterClient') as mock_client:
        # Configura o mock para retornar uma análise simulada
        mock_instance = mock_client.return_value
        mock_instance.analyze_course = AsyncMock(return_value={
            "viability": "O curso apresenta alta viabilidade no mercado atual",
            "improvements": [
                "Adicionar módulos práticos",
                "Incluir mentoria personalizada",
                "Criar comunidade de alunos"
            ],
            "marketing_strategy": "Focar em marketing de conteúdo e mídia social",
            "suggested_price": "R$ 997,00",
            "market_potential": "Mercado em expansão com grande potencial",
            "recommendations": [
                "Criar conteúdo gratuito para atração",
                "Estabelecer parcerias estratégicas",
                "Implementar programa de afiliados"
            ],
            "competitors": [
                "Curso A - Foco em teoria",
                "Curso B - Mais caro",
                "Curso C - Menos completo"
            ],
            "trends": [
                "Aumento da demanda por cursos online",
                "Preferência por formato microlearning",
                "Crescimento do mobile learning"
            ],
            "channels": [
                "Instagram",
                "YouTube",
                "LinkedIn",
                "Email Marketing"
            ]
        })
        yield mock_client

@pytest.fixture
def test_env():
    """
    Configura variáveis de ambiente para teste
    """
    original_env = dict(os.environ)
    
    # Define variáveis de teste
    os.environ.update({
        'OPENHOUTER_API_URL': 'http://test.openhouter.com/v1',
        'OPENHOUTER_API_KEY': 'test_key_123',
        'COURSE_ANALYZER_PORT': '8010',
        'TEST_MODE': 'True'
    })
    
    yield
    
    # Restaura variáveis originais
    os.environ.clear()
    os.environ.update(original_env)