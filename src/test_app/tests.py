from django.test import TestCase
from django.db import IntegrityError

from test_app.models import Pizza, Topping


class ModelsTest(TestCase):
    """
    Тестирование поведения моделей
    """

    def setUp(self):
        self.toppings = (
            Topping(name='Cheese'),
            Topping(name='Pineapple'),
            Topping(name='Meat'),
            Topping(name='Vegetables'),
        )
        Topping.objects.bulk_create(self.toppings)

        self.pizzas = (
            Pizza(name='Pepperoni'),
            Pizza(name='Vegan'),
            Pizza(name='Super Pizza'),
        )
        Pizza.objects.bulk_create(self.pizzas)
        self.pizzas[0].toppings.set((self.toppings[0], self.toppings[2],))
        self.pizzas[1].toppings.set((self.toppings[0], self.toppings[1], self.toppings[3],))
        self.pizzas[2].toppings.set(self.toppings)
        list(map(lambda x: x.save(), self.pizzas))

    def test_pkey(self):
        with self.assertRaisesMessage(IntegrityError, 'UNIQUE'):
            Topping.objects.create(name='Cheese')
        with self.assertRaisesMessage(IntegrityError, 'UNIQUE'):
            Pizza.objects.create(name='Pepperoni')

    def test_toppings_str(self):
        self.assertEqual('Cheese, Meat', self.pizzas[0].toppings_srt)
