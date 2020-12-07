from django.conf import settings
from django.db.models import F, Sum
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_recursive.fields import RecursiveField

from apps.budget.models import Budget, Function, Agency


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ('id', 'year', 'currency')


class BudgetAccountSerializer(serializers.ModelSerializer):
    children = serializers.ListSerializer(child=RecursiveField())
    label = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'initial_budget_investment', 'initial_budget_operation', 'initial_budget_aggregated',
                  'budget_investment', 'budget_operation', 'budget_aggregated',
                  'execution_investment', 'execution_operation', 'execution_aggregated',
                  'last_update', 'children', 'label', 'color', 'level', 'tree_id')

    def get_label(self, obj):
        return obj.get_taxonomy_label()

    def get_color(self, obj):
        color_index = 0
        execution_value = obj.execution_aggregated or 0

        # TODO: REMOVE ME
        if not obj.budget_aggregated:
            return settings.TREEMAP_EXECUTION_COLORS[color_index]

        execution_percent = execution_value / obj.budget_aggregated
        if 0.2 < execution_percent <= 0.4:
            color_index = 1
        if 0.4 < execution_percent <= 0.6:
            color_index = 2
        elif 0.6 < execution_percent <= 0.8:
            color_index = 3
        if 0.8 < execution_percent:
            color_index = 4
        return settings.TREEMAP_EXECUTION_COLORS[color_index]


class FunctionSerializer(BudgetAccountSerializer):
    class Meta:
        model = Function
        fields = BudgetAccountSerializer.Meta.fields


class AgencySerializer(BudgetAccountSerializer):
    class Meta:
        model = Agency
        fields = BudgetAccountSerializer.Meta.fields


class HistoricalParamsSerializer(serializers.Serializer):
    budget_account = serializers.ChoiceField(choices=['agencies', 'functions'])
    budget_account_id = serializers.IntegerField(required=False)


class HistoricalDataSerializer(serializers.Serializer):
    year = serializers.CharField()
    budget_aggregated = serializers.FloatField()
    execution_aggregated = serializers.FloatField()


class HistoricalSerializer(serializers.Serializer):
    data = HistoricalDataSerializer()
    name = serializers.CharField()
    id = serializers.IntegerField()


class BudgetViewset(ReadOnlyModelViewSet):
    model = Budget
    serializer_class = BudgetSerializer
    queryset = Budget.objects.all()

    @action(detail=True)
    def functions(self, request, pk=None):
        budget = self.get_object()
        qs = Function.objects.filter(budget=budget, level=0)
        serializer = FunctionSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def agencies(self, request, pk=None):
        budget = self.get_object()
        qs = Agency.objects.filter(budget=budget, level=0)
        serializer = AgencySerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def historical(self, request, pk=None):
        budget = self.get_object()
        country = budget.country

        params = HistoricalParamsSerializer(data=request.GET)
        params.is_valid(raise_exception=True)

        budget_account_model = None
        budget_account_param = params.validated_data['budget_account']
        budget_account_id = params.validated_data.get('budget_account_id', None)
        if budget_account_param == 'agencies':
            budget_account_model = Agency
        elif budget_account_param == 'functions':
            budget_account_model = Function

        data = {'code': None, 'name': None, 'data': []}

        if budget_account_id:
            # Get historical data from a specific budget.
            budget_account = budget_account_model.objects.select_related('budget').get(id=budget_account_id)
            code = budget_account.code
            name = budget_account.name
            if not code:
                # If BudgetAccount has no code, get historical data from parent.
                name = budget_account.parent.name
                code = budget_account.parent.code
                if not code:
                    # If parent has no code, return empty list
                    return Response(data)

            qs = budget_account_model.objects.filter(budget__country=country, code=code)\
                .values('budget_aggregated', 'execution_aggregated', year=F('budget__year'))
        else:
            # Get aggregated historical data for the country.
            name = country.name
            code = None
            qs = budget_account_model.objects.filter(budget__country=country, level=0).values(year=F('budget__year')) \
                .annotate(budget_aggregated=Sum('budget_aggregated'), execution_aggregated=Sum('execution_aggregated'))\
                .order_by('year')

        data_serializer = HistoricalDataSerializer(qs, many=True)

        data['name'] = name
        data['code'] = code
        data['data'] = data_serializer.data
        serializer = HistoricalSerializer(data=data)

        return Response(serializer.initial_data)
