from django.db import models
from django.utils.translation import ugettext_lazy as _


class Topping(models.Model):
    name = models.CharField(
        _("Topping name"),
        max_length=256,
        primary_key=True
    )

    class Meta:
        verbose_name = _("Topping")
        verbose_name_plural = _("Toppings")


class Pizza(models.Model):
    name = models.CharField(
        _("Pizza name"),
        max_length=256,
        primary_key=True
    )
    toppings = models.ManyToManyField(
        Topping,
        related_name="pizzas",
        related_query_name="pizzas",
        verbose_name=_("Toppings")
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def toppings_srt(self):
        return ', '.join(self.toppings.all().values_list("name", flat=True))

    def __str__(self):
        return "{name} ({toppings})".format(name=self.name, toppings=str(self.toppings_srt))
