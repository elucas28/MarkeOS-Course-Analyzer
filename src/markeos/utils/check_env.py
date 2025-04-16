from dotenv import load_dotenv
import os
from pathlib import Path

def check_env():
    # Tenta carregar do diretório atual
    env_path = Path('.env')
    print(f"\nTentando carregar .env de: {env_path.absolute()}")
    load_dotenv(dotenv_path=env_path)
    
    # Tenta carregar do diretório do script
    script_dir_env = Path(__file__).parent / '.env'
    print(f"Tentando carregar .env de: {script_dir_env.absolute()}")
    load_dotenv(dotenv_path=script_dir_env)
    
    # Imprime informações de debug
    print("\nInformações de ambiente:")
    print(f"Diretório atual: {os.getcwd()}")
    print(f".env no diretório atual existe: {env_path.exists()}")
    print(f".env no diretório do script existe: {script_dir_env.exists()}")
    
    print("\nVariáveis carregadas:")
    print(f"OPENHOUTER_API_URL: {os.getenv('OPENHOUTER_API_URL')}")
    print(f"OPENHOUTER_API_KEY: {'*' * 10 if os.getenv('OPENHOUTER_API_KEY') else 'Não definida'}")
    print(f"COURSE_ANALYZER_PORT: {os.getenv('COURSE_ANALYZER_PORT')}")

    # Verifica se as variáveis necessárias estão definidas
    missing_vars = []
    if not os.getenv('OPENHOUTER_API_URL'):
        missing_vars.append('OPENHOUTER_API_URL')
    if not os.getenv('OPENHOUTER_API_KEY'):
        missing_vars.append('OPENHOUTER_API_KEY')
    
    if missing_vars:
        print("\nERRO: As seguintes variáveis de ambiente não estão definidas:")
        for var in missing_vars:
            print(f"- {var}")
        return False
    
    print("\nTodas as variáveis necessárias estão configuradas!")
    return True

if __name__ == "__main__":
    check_env()