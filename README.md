# MarkeOS Course Analyzer

Sistema de análise de cursos usando IA através da API OpenHouter.

## Descrição

O MarkeOS Course Analyzer é uma API que utiliza inteligência artificial para analisar propostas de cursos e fornecer insights valiosos sobre:
- Viabilidade do curso
- Estratégias de marketing
- Análise de mercado
- Recomendações práticas
- Precificação sugerida
- Análise de concorrência

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/elucas28/MarkeOS-Course-Analyzer.git
cd markeos
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

## Uso

### Iniciar o servidor

```bash
python -m markeos.course_analyzer
```

O servidor estará disponível em `http://localhost:8010`

### Exemplo de requisição

```python
import requests

url = "http://localhost:8010/analyze-course"
data = {
    "course_name": "Marketing Digital Avançado",
    "problem_solved": "Profissionais que precisam melhorar suas habilidades em marketing digital",
    "target_audience": "Profissionais de marketing, empreendedores e gestores",
    "marketing_budget": 5000.0,
    "course_format": "online",
    "duration": "8 semanas",
    "initial_description": "Curso completo abordando as principais estratégias de marketing digital"
}

response = requests.post(url, json=data)
task_id = response.json()["task_id"]

# Consultar resultado
status_url = f"http://localhost:8010/tasks/{task_id}"
status = requests.get(status_url).json()
```

## Endpoints

### POST /analyze-course

Inicia uma análise de curso. Requer um JSON com os seguintes campos:
- course_name: Nome do curso
- problem_solved: Problema que o curso resolve
- target_audience: Público-alvo
- marketing_budget: Orçamento de marketing
- course_format: Formato do curso (online, presencial, híbrido)
- duration: Duração total
- initial_description: Descrição adicional
- market_analysis: (opcional) Se deve incluir análise de mercado

### GET /tasks/{task_id}

Consulta o status e resultado de uma análise. Retorna:
- status: Status da análise (PENDING, PROCESSING, SUCCESS, ERROR)
- result: Resultado da análise (quando status=SUCCESS)
- error: Mensagem de erro (quando status=ERROR)

## Desenvolvimento

### Executar testes

```bash
pytest
```

### Verificar ambiente

```bash
python -m markeos.check_env
```

## Licença

MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contribuição

1. Fork o projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request