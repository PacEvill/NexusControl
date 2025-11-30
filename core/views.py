from django.shortcuts import render, redirect


def index(request):
    return redirect('dashboard')


def dashboard(request):
    # Dados de exemplo para sensores (simulando dados do Next.js)
    sensors = [
        {
            'id': 1,
            'name': 'Temperatura Sala de Servidores',
            'value': 22.5,
            'unit': '°C',
            'status': 'normal',
            'status_display': 'Normal',
            'last_update': '2023-06-15 14:30:45'
        },
        {
            'id': 2,
            'name': 'Umidade Ambiente',
            'value': 65.3,
            'unit': '%',
            'status': 'warning',
            'status_display': 'Atenção',
            'last_update': '2023-06-15 14:32:12'
        },
        {
            'id': 3,
            'name': 'Consumo de Energia',
            'value': 4.2,
            'unit': 'kW/h',
            'status': 'normal',
            'status_display': 'Normal',
            'last_update': '2023-06-15 14:29:58'
        },
        {
            'id': 4,
            'name': 'Temperatura CPU',
            'value': 78.9,
            'unit': '°C',
            'status': 'alert',
            'status_display': 'Alerta',
            'last_update': '2023-06-15 14:31:23'
        }
    ]
    
    context = {
        'title': 'Dashboard - SensorView',
        'sensors': sensors
    }
    return render(request, 'core/dashboard.html', context)


def login_view(request):
    return render(request, 'core/login.html', {})


def cadastro(request):
    return render(request, 'core/cadastro.html', {})


def contato(request):
    return render(request, 'core/contato.html', {})


def produto(request, produto_id=None):
    # produto_id optional, placeholder implementation
    return render(request, 'core/produto.html', {'produto_id': produto_id})


def catalogo(request):
    return render(request, 'core/catalogo.html', {})


def portfolio(request):
    return render(request, 'core/portfolio.html', {})


def servicos(request):
    return render(request, 'core/servicos.html', {})


def sobre(request):
    return render(request, 'core/sobre.html', {})


def faq(request):
    return render(request, 'core/faq.html', {})


def orcamento(request):
    return render(request, 'core/orcamento.html', {})


def guia_materiais(request):
    return render(request, 'core/guia-materiais.html', {})


def materiais(request):
    return render(request, 'core/materiais.html', {})
