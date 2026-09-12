from decimal import Decimal
from typing import List, Dict, Tuple
from .models import Box

class BoxSelectionService:
    @staticmethod
    def _can_contain_item(item_dims: Tuple[float, float, float], box_dims: Tuple[float, float, float]) -> bool:
        """
        Determines if an item fits inside a box by checking whether the sorted 
        item dimensions (length, width, height) are all less than or equal to 
        the sorted box dimensions, allowing any 3D rotation orientation.
        """
        sorted_item = sorted(item_dims)
        sorted_box = sorted(box_dims)
        return (
            sorted_item[0] <= sorted_box[0] and
            sorted_item[1] <= sorted_box[1] and
            sorted_item[2] <= sorted_box[2]
        )

    @classmethod
    def recommend_box(cls, items: List[Dict]) -> Dict:
        if not items:
            return {"status": "error", "message": "The items list cannot be empty."}

        total_weight = Decimal("0.0")
        total_volume = 0.0
        parsed_items = []

        # Validate each item payload
        for idx, item in enumerate(items):
            try:
                length = float(item['length'])
                width = float(item['width'])
                height = float(item['height'])
                weight = Decimal(str(item['weight']))
                quantity = int(item.get('quantity', 1))
            except (KeyError, ValueError, TypeError):
                return {
                    "status": "error",
                    "message": f"Item at index {idx} has missing or malformed numeric dimensions/weight."
                }

            if length <= 0 or width <= 0 or height <= 0 or weight <= 0 or quantity <= 0:
                return {
                    "status": "error",
                    "message": f"Item at index {idx} must have strictly positive dimensions, weight, and quantity."
                }

            total_volume += (length * width * height) * quantity
            total_weight += weight * quantity

            for _ in range(quantity):
                parsed_items.append((length, width, height))

        # Query boxes with sufficient weight capacity, evaluated from lowest to highest cost
        candidate_boxes = Box.objects.filter(max_weight__gte=total_weight).order_by('cost')

        for box in candidate_boxes:
            box_dims = (float(box.length), float(box.width), float(box.height))

            # Condition 1: Box volume must accommodate the combined item volume
            if box.volume < total_volume:
                continue

            # Condition 2: Every individual item must fit within internal box dimensions
            all_items_fit = True
            for item_dims in parsed_items:
                if not cls._can_contain_item(item_dims, box_dims):
                    all_items_fit = False
                    break

            if all_items_fit:
                return {
                    "status": "success",
                    "box": {
                        "id": box.id,
                        "name": box.name,
                        "dimensions": {
                            "length": float(box.length),
                            "width": float(box.width),
                            "height": float(box.height),
                        },
                        "max_weight": float(box.max_weight),
                        "cost": float(box.cost),
                    },
                    "order_summary": {
                        "total_items": len(parsed_items),
                        "total_volume_cm3": round(total_volume, 2),
                        "total_weight_kg": float(total_weight),
                    }
                }

        return {
            "status": "not_found",
            "message": "No available box meets both the dimension and weight requirements for this order."
        }