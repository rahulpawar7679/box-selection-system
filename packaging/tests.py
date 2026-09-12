from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from .models import Box
from .services import BoxSelectionService

class BoxSelectionLogicTests(TestCase):
    def setUp(self):
        self.box_small = Box.objects.create(
            name="Small Parcel",
            length=Decimal("15.0"),
            width=Decimal("15.0"),
            height=Decimal("10.0"),
            max_weight=Decimal("2.0"),
            cost=Decimal("20.00")
        )
        self.box_medium = Box.objects.create(
            name="Medium Parcel",
            length=Decimal("30.0"),
            width=Decimal("20.0"),
            height=Decimal("15.0"),
            max_weight=Decimal("5.0"),
            cost=Decimal("45.00")
        )
        self.box_large = Box.objects.create(
            name="Large Box",
            length=Decimal("50.0"),
            width=Decimal("40.0"),
            height=Decimal("30.0"),
            max_weight=Decimal("20.0"),
            cost=Decimal("90.00")
        )

    def test_3d_rotation_fit(self):
        """Item (14x8x12) fits into Small Box (15x15x10) when rotated."""
        items = [{"length": 14, "width": 8, "height": 12, "weight": 1.0, "quantity": 1}]
        result = BoxSelectionService.recommend_box(items)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["box"]["name"], "Small Parcel")

    def test_weight_limit_triggers_box_upgrade(self):
        """Item fits inside Small Parcel by volume, but requires Medium Parcel due to weight."""
        items = [{"length": 10, "width": 10, "height": 5, "weight": 3.5, "quantity": 1}]
        result = BoxSelectionService.recommend_box(items)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["box"]["name"], "Medium Parcel")

    def test_item_exceeds_all_box_dimensions(self):
        """Item exceeding all available box dimensions returns not_found."""
        items = [{"length": 100, "width": 60, "height": 50, "weight": 2.0, "quantity": 1}]
        result = BoxSelectionService.recommend_box(items)
        self.assertEqual(result["status"], "not_found")

    def test_invalid_negative_dimensions(self):
        """Non-positive dimensions return an error."""
        items = [{"length": -10, "width": 5, "height": 5, "weight": 1.0}]
        result = BoxSelectionService.recommend_box(items)
        self.assertEqual(result["status"], "error")


class BoxSelectionAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.box = Box.objects.create(
            name="Standard Box",
            length=Decimal("25.0"),
            width=Decimal("20.0"),
            height=Decimal("15.0"),
            max_weight=Decimal("5.0"),
            cost=Decimal("30.00")
        )

    def test_recommend_box_api_success(self):
        payload = {
            "items": [
                {"length": 10, "width": 10, "height": 5, "weight": 1.0, "quantity": 2}
            ]
        }
        response = self.client.post(
            reverse('recommend-box'),
            data=payload,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertEqual(response.json()["box"]["name"], "Standard Box")

    def test_recommend_box_api_malformed_json(self):
        response = self.client.post(
            reverse('recommend-box'),
            data="plain-text-payload",
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)