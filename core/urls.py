from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('contato/', views.contato, name='contato'),
    path('produto/<str:produto_id>/', views.produto, name='produto'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('servicos/', views.servicos, name='servicos'),
    path('sobre/', views.sobre, name='sobre'),
    path('faq/', views.faq, name='faq'),
    path('orcamento/', views.orcamento, name='orcamento'),
    path('guia-materiais/', views.guia_materiais, name='guia_materiais'),
    path('materiais/', views.materiais, name='materiais'),
]
