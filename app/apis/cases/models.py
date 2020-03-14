from django.db import models
from app.apis.models import BaseModel
from django.utils import timezone


class CountryCases(models.Model):
    """
    CountryCases model
    """

    country = models.CharField(max_length=200, unique=True, primary_key=True)
    total_cases = models.BigIntegerField(db_index=True, unique=False, blank=True, null=True)
    new_cases = models.BigIntegerField(db_index=True, unique=False, blank=True, null=True)
    total_deaths = models.BigIntegerField(db_index=True, unique=False, blank=True, null=True)
    new_deaths = models.BigIntegerField(db_index=True, unique=False, blank=True, null=True)
    total_recovered = models.CharField(max_length=200, unique=False, blank=True, null=True)
    active_cases = models.BigIntegerField(db_index=True, unique=False, blank=True, null=True)
    serious_critical = models.BigIntegerField(db_index=True, unique=False, blank=True, null=True)
    cases_per_mill_pop = models.FloatField(max_length=50, db_index=True, unique=False, blank=True, null=True)
    flag = models.CharField(max_length=200, blank=True, null=True)
    last_update = models.DateTimeField(default=timezone.now)


    def __str__(self):
        """
        string representation
        of the model instance
        """
        return self.country


class GeneralStats(BaseModel):
    """
    CountryCases model
    """

    total_cases = models.BigIntegerField(db_index=True, unique=False)
    death_cases = models.BigIntegerField(db_index=True, unique=False)
    recovery_cases = models.BigIntegerField(db_index=True, unique=False)
    currently_infected = models.BigIntegerField(db_index=True, unique=False)
    cases_with_outcome = models.BigIntegerField(db_index=True, unique=False)
    mild_condition_active_cases = models.BigIntegerField(
        db_index=True, unique=False)
    critical_condition_active_cases = models.BigIntegerField(
        db_index=True, unique=False)
    recovered_closed_cases = models.BigIntegerField(
        db_index=True, unique=False)
    death_closed_cases = models.BigIntegerField(db_index=True, unique=False)
    last_update = models.DateTimeField()
