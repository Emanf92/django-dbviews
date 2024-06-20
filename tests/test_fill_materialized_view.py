from django.test import TransactionTestCase

from penpineapples.models import Penpineapple
from pens.models import Pen
from pineapples.models import Pineapple


class TewstFillMaterializedView(TransactionTestCase):
    @staticmethod
    def test_create_one_item_only():
        Pineapple(
            size=12,
            price=300
        ).save()

        assert Pineapple.objects.count() == 1, "Pineapple should have been successfully created"

        assert Penpineapple.objects.count() == 0, "No Penpineapple should have been created since there are no pens"

    @staticmethod
    def test_create_both_items():
        pineapple = Pineapple(
            size=12,
            price=300
        )

        pineapple.save()

        Pen(
            color="red",
            price=300,
            pineapple=pineapple
        ).save()

        assert Pineapple.objects.count() == 1, "Pineapple should have been successfully created"
        assert Pen.objects.count() == 1, "Pen should have been successfully created"

        assert Penpineapple.objects.count() == 1, ("A Penpineapple should have been created since there are associated "
                                                   "pens and pienapples")
