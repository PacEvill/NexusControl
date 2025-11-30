# NexusControl

![Status de Build](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Django](https://img.shields.io/badge/django-5.0-green)
![Licença](https://img.shields.io/badge/license-MIT-orange)

**NexusControl** é um Centro de Comando IoT pronto para produção construído com Django, projetado para monitorar e gerenciar redes de sensores em tempo real. Possui um dashboard responsivo, atualizações ao vivo via WebSocket e uma API REST segura para ingestão de dados.

## 🏗 Arquitetura

```mermaid
graph TD
    A["Região (ex: Campus)"] --> B["Local (ex: Sala de Servidores)"]
    B --> C["Sensor (ex: Sensor Temp 01)"]
    C -->|Enviar Dados (API)| D[Backend NexusControl]
    D -->|WebSocket| E[Dashboard ao Vivo]
    D -->|Persistir| F[PostgreSQL]
```

## 🚀 Início Rápido

### Docker (Recomendado)

A maneira mais rápida de rodar o NexusControl é usando Docker Compose.

```bash
# Clonar o repositório
git clone https://github.com/seuusuario/nexus-control.git
cd nexus-control

# Criar arquivo de ambiente
cp .env.example .env

# Iniciar serviços
docker-compose up --build
```

Acesse o dashboard em [http://localhost:8000](http://localhost:8000).

### Desenvolvimento Local

1. **Configuração do Ambiente**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

2. **Banco de Dados e População**

    ```bash
    python manage.py migrate
    python manage.py populate_data       # Cria tipos de sensores e sensores de teste
    python manage.py populate_locations  # Cria regiões e vincula sensores
    ```

3. **Rodar Servidor**

    ```bash
    # Use daphne para suporte a WebSocket
    daphne -b 0.0.0.0 -p 8000 sensorview.asgi:application
    ```

## 🔌 Referência da API

O NexusControl expõe uma API REST segura para sensores.

### Autenticação

Obtenha um token JWT para autenticar requisições.

```bash
curl -X POST http://localhost:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "password"}'
```

### Enviar Leitura de Sensor

**POST** `/api/v1/sensors/{id}/reading/`

```bash
curl -X POST http://localhost:8000/api/v1/sensors/1/reading/ \
     -H "Authorization: Bearer <SEU_TOKEN_DE_ACESSO>" \
     -H "Content-Type: application/json" \
     -d '{"value": 25.5}'
```

## 🧪 Testes

Execute a suíte de testes automatizados para garantir a integridade do sistema:

```bash
python manage.py test sensors
```

## 🎨 Funcionalidades

- **Dashboard em Tempo Real**: Atualizações ao vivo via WebSockets (Django Channels).
- **Centro de Comando**: Visualização agregada por Região.
- **Exportação de Dados**: Capacidades de exportação para CSV e JSON.
- **Seguro**: Autenticação JWT e configuração baseada em ambiente.
- **Modo Escuro**: Suporte nativo a modo escuro.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT.
