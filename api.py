import requests
from datetime import date

# Data atual
hoje = date.today()

# Número da semana (ISO: segunda-feira é o primeiro dia da semana)
numero_da_semana = hoje.isocalendar().week


def buscar_usuario(matricula):
    response = requests.get(f"http://api.quattoracademia.com:8888/alunos/?matricula={matricula}")
    return response.json()

def buscar_treino(grupo):
    response = requests.get(f"http://api.quattoracademia.com:8888/exercicio/?semana={numero_da_semana}&grupo={grupo}")
    return response.json()

def registrar_treino(treino):
    try:
        
        url = f"http://api.quattoracademia.com:8888/registrar/?matricula={treino['matricula']}&grupo={treino['grupo']}"  
        response = requests.post(url)
   
        if response.status_code == 200:
            return response.json()
        else:
            
            return {"error": f"Erro na API: {response.status_code}", "message": response.text}
    except requests.exceptions.RequestException as e:
        
        return {"error": "Erro na requisição", "message": str(e)}
    except ValueError as e:
        
        return {"error": "Erro ao decodificar JSON", "message": str(e)}

def buscar_historico(matricula):
    response = requests.get(f"http://api.quattoracademia.com:8888/historico/?matricula={matricula}")
    return response.json()
