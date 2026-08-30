import requests
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Fabricante, Componente
from .serializers import FabricanteSerializer, ComponenteSerializer


class FabricanteViewSet(viewsets.ModelViewSet):
    queryset = Fabricante.objects.all()
    serializer_class = FabricanteSerializer


class ComponenteViewSet(viewsets.ModelViewSet):
    serializer_class = ComponenteSerializer

    def get_queryset(self):
        queryset = Componente.objects.select_related("fabricante").all()
        fabricante_id = self.request.query_params.get("fabricante")
        tipo = self.request.query_params.get("tipo")
        if fabricante_id:
            queryset = queryset.filter(fabricante_id=fabricante_id)
        if tipo:
            queryset = queryset.filter(tipo=tipo.upper())
        return queryset


# ---------------------------------------------------------------------------
# Consumo de API externa (endpoint gratuito, sem necessidade de chave)
# API utilizada: Fake Store API (https://fakestoreapi.com)
# Retorna um catálogo de produtos (incluindo a categoria "electronics").
# ---------------------------------------------------------------------------

FAKESTORE_URL = "https://fakestoreapi.com/products"
TIMEOUT_SEGUNDOS = 5


@api_view(["GET"])
def buscar_produtos_externos(request):
    categoria = request.query_params.get("categoria", "").strip()
    url = f"{FAKESTORE_URL}/category/{categoria}" if categoria else FAKESTORE_URL

    try:
        resposta = requests.get(url, timeout=TIMEOUT_SEGUNDOS)
        resposta.raise_for_status()
        dados = resposta.json()
    except requests.exceptions.RequestException:
        return Response(
            {"erro": "Não foi possível consultar a (Fake Store API)."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    if not dados:
        return Response(
            {"erro": f"Nenhum produto encontrado para a categoria '{categoria}'."},
            status=status.HTTP_404_NOT_FOUND,
        )

    produtos_encontrados = [
        {
            "id": item.get("id"),
            "titulo": item.get("title"),
            "preco": item.get("price"),
            "categoria": item.get("category"),
        }
        for item in dados
    ]

    return Response({"resultados": produtos_encontrados}, status=status.HTTP_200_OK)