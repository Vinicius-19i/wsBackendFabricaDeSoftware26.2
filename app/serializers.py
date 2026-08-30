from rest_framework import serializers
from .models import Fabricante, Componente


class ComponenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Componente
        fields = ["id", "nome", "tipo", "fabricante"]
        read_only_fields = ["id"]


class ComponenteResumidoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Componente
        fields = ["id", "nome", "tipo"]


class FabricanteSerializer(serializers.ModelSerializer):
    componentes = ComponenteResumidoSerializer(many=True, read_only=True)

    class Meta:
        model = Fabricante
        fields = [
            "id",
            "nome",
            "pais_origem",
            "site",
            "criado_em",
            "componentes",
        ]
        read_only_fields = ["id", "criado_em"]
