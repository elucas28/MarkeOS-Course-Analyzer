from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
import os
import json
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks, HTTPException
import uuid
from dotenv import load_dotenv
from pathlib import Path
import aiohttp

# Carrega variáveis de ambiente do arquivo .env
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Debug: Imprime as variáveis de ambiente carregadas
print("Variáveis de ambiente carregadas:")
print(f"OPENAI_API_KEY: {'*' * 10 if os.getenv('OPENAI_API_KEY') else 'Não definida'}")
print(f"OPENAI_MODEL: {os.getenv('OPENAI_MODEL')}")
print(f"COURSE_ANALYZER_PORT: {os.getenv('COURSE_ANALYZER_PORT')}")

class CourseAnalysisRequest(BaseModel):
    """Modelo para requisição de análise de curso"""
    course_name: str = Field(..., description="Nome do curso")
    problem_solved: str = Field(..., description="Problema que o curso resolve")
    target_audience: str = Field(..., description="Público-alvo do curso")
    marketing_budget: float = Field(..., description="Orçamento disponível para marketing")
    course_format: str = Field(..., description="Formato do curso (online, presencial, híbrido)")
    duration: str = Field(..., description="Duração total do curso")
    initial_description: str = Field(..., description="Descrição adicional do curso")
    market_analysis: bool = Field(default=True, description="Se deve incluir análise de mercado")

class CourseAnalysisResponse(BaseModel):
    """Modelo para resposta da análise de curso"""
    technical_sheet: str = Field(..., description="Ficha técnica completa do curso")
    market_analysis: Optional[Dict[str, Any]] = Field(None, description="Análise de mercado detalhada")
    recommendations: List[str] = Field(default_factory=list, description="Lista de recomendações")

class OpenRouterClient:
    """Cliente para integração com a API do OpenRouter"""
    
    def __init__(self):
        """Inicializa o cliente OpenRouter"""
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "openai/gpt-4.1")
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY deve estar definida nas variáveis de ambiente")
        
        print(f"Inicializando OpenRouter Client com modelo {self.model}")
    
    async def analyze_course(self, course_data: CourseAnalysisRequest) -> Dict[str, Any]:
        """
        Envia dados do curso para análise via API OpenRouter
        
        Args:
            course_data: Dados do curso para análise
            
        Returns:
            Dict com resultado da análise
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://markeos.com",
            "X-Title": "MarkeOS Course Analyzer"
        }
        
        prompt = self._format_analysis_prompt(course_data)
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "Você é um especialista em análise de cursos e marketing digital."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        try:
            print(f"Fazendo requisição para OpenRouter usando modelo {self.model}")
            print(f"Headers: {headers}")
            print(f"Payload: {json.dumps(payload, indent=2)}")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    json=payload,
                    headers=headers
                ) as response:
                    if response.status != 200:
                        error_data = await response.text()
                        print(f"Erro na API OpenRouter: Status {response.status}, Response: {error_data}")
                        raise ValueError(f"Erro na API OpenRouter: {error_data}")
                    
                    response_data = await response.json()
                    print(f"Resposta recebida: {json.dumps(response_data, indent=2)}")
                    
                    # Extrai o conteúdo da resposta
                    content = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')
                    
                    # Tenta extrair o JSON da resposta
                    try:
                        # Remove possíveis textos antes e depois do JSON
                        json_start = content.find('{')
                        json_end = content.rfind('}') + 1
                        if json_start >= 0 and json_end > json_start:
                            json_str = content[json_start:json_end]
                            return json.loads(json_str)
                        else:
                            raise ValueError("JSON não encontrado na resposta")
                    except json.JSONDecodeError:
                        print(f"Erro ao decodificar JSON da resposta: {content}")
                        raise ValueError("Resposta não contém JSON válido")
                    
        except aiohttp.ClientError as e:
            print(f"Erro de conexão: {str(e)}")
            raise ConnectionError(f"Erro de conexão com OpenRouter API: {str(e)}")
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar resposta: {str(e)}")
            raise ValueError("Resposta inválida da API OpenRouter")
    
    def _format_analysis_prompt(self, course_data: CourseAnalysisRequest) -> str:
        """
        Formata o prompt para análise do curso
        
        Args:
            course_data: Dados do curso
            
        Returns:
            String com o prompt formatado
        """
        return f"""
        Analise as seguintes informações sobre um curso e gere uma análise detalhada:

        Nome do Curso: {course_data.course_name}
        Problema Resolvido: {course_data.problem_solved}
        Público-alvo: {course_data.target_audience}
        Orçamento de Marketing: R$ {course_data.marketing_budget:.2f}
        Formato: {course_data.course_format}
        Duração: {course_data.duration}
        
        Descrição Adicional:
        {course_data.initial_description}

        Por favor, forneça uma análise detalhada incluindo:
        1. Avaliação da viabilidade do curso
        2. Sugestões específicas de melhorias
        3. Estratégias de marketing recomendadas considerando o orçamento
        4. Preço sugerido com justificativa
        5. Análise do potencial de mercado
        6. Recomendações práticas para implementação
        7. Análise da concorrência e diferenciação
        8. Tendências do mercado relacionadas
        9. Canais de distribuição recomendados

        Retorne a análise em formato JSON com as seguintes chaves:
        - viability: Análise de viabilidade
        - improvements: Lista de sugestões de melhorias
        - marketing_strategy: Estratégias de marketing detalhadas
        - suggested_price: Preço sugerido com justificativa
        - market_potential: Análise do potencial de mercado
        - recommendations: Lista de recomendações práticas
        - competitors: Análise da concorrência
        - trends: Tendências relevantes
        - channels: Canais de distribuição
        """

class CourseAnalyzer:
    """Agente especializado em análise de cursos"""
    
    def __init__(self):
        """Inicializa o CourseAnalyzer"""
        self.openrouter_client = OpenRouterClient()
        self.app = FastAPI(title="Course Analyzer API", description="API para análise de cursos")
        self.tasks = {}
        self.add_routes()
    
    def add_routes(self):
        """Adiciona rotas à API FastAPI"""
        
        @self.app.post("/analyze-course")
        async def analyze_course(request: CourseAnalysisRequest, background_tasks: BackgroundTasks):
            """
            Endpoint para analisar um curso
            
            Args:
                request: Requisição de análise de curso
                background_tasks: Objeto BackgroundTasks do FastAPI
                
            Returns:
                dict: Resposta com ID da tarefa
            """
            task_id = str(uuid.uuid4())
            self.tasks[task_id] = {"status": "PENDING"}
            
            background_tasks.add_task(self._process_analysis, task_id, request)
            
            return {"task_id": task_id, "status": "PENDING"}
        
        @self.app.get("/tasks/{task_id}")
        async def get_analysis_task(task_id: str):
            """
            Endpoint para obter o status de uma tarefa de análise
            
            Args:
                task_id: ID da tarefa
                
            Returns:
                dict: Status da tarefa
            """
            if task_id not in self.tasks:
                raise HTTPException(status_code=404, detail="Task not found")
            
            return self.tasks[task_id]
    
    async def _process_analysis(self, task_id: str, course_data: CourseAnalysisRequest):
        """
        Processa a análise do curso em background
        
        Args:
            task_id: ID da tarefa
            course_data: Dados do curso
        """
        try:
            self.tasks[task_id]["status"] = "PROCESSING"
            
            # Obtém análise via OpenRouter
            analysis_result = await self.openrouter_client.analyze_course(course_data)
            
            # Gera ficha técnica
            technical_sheet = self._generate_technical_sheet(course_data, analysis_result)
            
            # Prepara resultado
            result = {
                'technical_sheet': technical_sheet,
                'market_analysis': {
                    'market_potential': analysis_result.get('market_potential'),
                    'competitors': analysis_result.get('competitors', []),
                    'trends': analysis_result.get('trends', []),
                    'channels': analysis_result.get('channels', [])
                },
                'recommendations': analysis_result.get('recommendations', []),
                'timestamp': datetime.now().isoformat()
            }
            
            self.tasks[task_id]["status"] = "SUCCESS"
            self.tasks[task_id]["result"] = result
            
        except Exception as e:
            print(f"Erro ao processar análise: {str(e)}")
            self.tasks[task_id]["status"] = "ERROR"
            self.tasks[task_id]["error"] = str(e)
            self.tasks[task_id]["error_type"] = e.__class__.__name__
    
    def _generate_technical_sheet(
        self,
        course_data: CourseAnalysisRequest,
        analysis_result: Dict[str, Any]
    ) -> str:
        """
        Gera a ficha técnica do curso
        
        Args:
            course_data: Dados do curso
            analysis_result: Resultado da análise
            
        Returns:
            String formatada com a ficha técnica
        """
        return f"""# Ficha Técnica do Curso

## Informações Básicas
- Nome: {course_data.course_name}
- Problema Resolvido: {course_data.problem_solved}
- Público-Alvo: {course_data.target_audience}

## Aspectos Financeiros
- Orçamento Marketing: R$ {course_data.marketing_budget:.2f}
- Preço Sugerido: {analysis_result.get('suggested_price', 'Não disponível')}

## Estrutura do Curso
- Formato: {course_data.course_format}
- Duração: {course_data.duration}

## Análise de Viabilidade
{analysis_result.get('viability', 'Análise não disponível')}

## Estratégia de Marketing
{analysis_result.get('marketing_strategy', 'Estratégia não disponível')}

## Canais de Distribuição Recomendados
{self._format_list(analysis_result.get('channels', []))}

## Análise de Mercado
- Potencial de Mercado: {analysis_result.get('market_potential', 'Não disponível')}
- Principais Concorrentes: {self._format_list(analysis_result.get('competitors', []))}
- Tendências Relevantes: {self._format_list(analysis_result.get('trends', []))}

## Sugestões de Melhorias
{self._format_list(analysis_result.get('improvements', []))}

## Recomendações Práticas
{self._format_list(analysis_result.get('recommendations', []))}

Data da Análise: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
"""
    
    def _format_list(self, items: List[str]) -> str:
        """
        Formata uma lista de itens como lista com marcadores
        
        Args:
            items: Lista de itens
            
        Returns:
            String formatada
        """
        if not items:
            return "- Não disponível"
        return "\n".join(f"- {item}" for item in items)

# Cria a instância do aplicativo
analyzer = CourseAnalyzer()
app = analyzer.app

def run_course_analyzer_service():
    """Inicia o serviço de análise de cursos"""
    import uvicorn
    port = int(os.getenv("COURSE_ANALYZER_PORT", "8010"))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    run_course_analyzer_service()