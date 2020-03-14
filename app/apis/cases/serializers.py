from rest_framework import serializers
from django.utils import timezone
from datetime import datetime
from django.core.validators import MinValueValidator
from .models import CountryCases, GeneralStats
from .helpers.countries import countries_


class CountryStatsSerializer(serializers.ModelSerializer):
    """Serializers for creating and retrieving all countries stats"""

    class Meta:
        model = CountryCases
        fields = ('__all__')

    def to_representation(self, instance):
        data = {}
        data['country'] = instance.country
        data['country_abbreviation'] = countries_(instance.country)
        data['total_cases'] = '{:,}'.format(instance.total_cases)
        data['new_cases'] = '{:,}'.format(instance.new_cases)
        data['total_deaths'] = '{:,}'.format(instance.total_deaths)
        data['new_deaths'] = '{:,}'.format(instance.new_deaths)
        data['total_recovered'] = '{:,}'.format(int(instance.total_recovered)) if instance.total_recovered.upper() != 'N/A' else instance.total_recovered
        data['active_cases'] = '{:,}'.format(instance.active_cases)
        data['serious_critical'] = '{:,}'.format(instance.serious_critical)
        data['cases_per_mill_pop'] = '{:,}'.format(instance.cases_per_mill_pop)
        data['flag'] = instance.flag
        return data


class GeneralStatsSerializer(serializers.ModelSerializer):
    """Serializers for creating and retrieving general stats"""
    id = serializers.CharField(read_only=True)

    class Meta:
        model = GeneralStats
        fields = ('__all__')

    def to_representation(self, instance):
        to_tz = timezone.get_default_timezone()
        data = {}
        data['total_cases'] = instance.total_cases
        data['recovery_cases'] = instance.recovery_cases
        data['death_cases'] = instance.death_cases
        data['last_update'] = instance.last_update.astimezone(
            to_tz).strftime("%b, %d %Y, %H:%M, %Z")
        data['currently_infected'] = instance.currently_infected
        data['cases_with_outcome'] = instance.cases_with_outcome
        data['mild_condition_active_cases'] = instance.mild_condition_active_cases
        data['critical_condition_active_cases'] = instance.critical_condition_active_cases
        data['recovered_closed_cases'] = instance.recovered_closed_cases
        data['death_closed_cases'] = instance.death_closed_cases
        data['closed_cases_recovered_percentage'] = round(
            data['recovery_cases']/data['cases_with_outcome'], 2)*100
        data['closed_cases_death_percentage'] = 100 - \
            data['closed_cases_recovered_percentage']
        data['active_cases_mild_percentage'] = round(
            data['mild_condition_active_cases']/data['currently_infected'], 2)*100
        data['active_cases_critical_percentage'] = 100 - \
            data['active_cases_mild_percentage']
        data['general_death_rate'] = round(
            data['death_cases']/data['total_cases'], 2) * 100

        for i in data:
            if isinstance(data[i], int) or isinstance(data[i], float):
                data[i] = '{:,}'.format(data[i])
        return data
