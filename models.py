from django.db import models

AVG_COST_OF_LIVING = [
    ('Above Average','Above Average'),
    ('Average','Average'),
    ('Below Average','Below Average'),
]

class Places(models.Model):
    city = models.CharField(max_length=30, default="", blank=True, null=False)
    state = models.CharField(max_length=2, default="", blank=True, null=False)
    state_cost_index = models.DecimalField(default=0.00, max_digits=1000, decimal_places=1)
    cost_of_living_average = models.CharField(max_length=60, choices=AVG_COST_OF_LIVING)
    description = models.TextField(max_length=300, default="", blank=True, null=False)

    objects = models.Manager()

    def __str__(self):
        return self.city

