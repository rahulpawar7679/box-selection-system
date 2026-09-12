import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Box
from .services import BoxSelectionService

@csrf_exempt
@require_http_methods(["POST"])
def recommend_box_view(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"status": "error", "message": "Malformed JSON payload."}, status=400)

    items = data.get("items")
    if not isinstance(items, list):
        return JsonResponse({"status": "error", "message": "'items' field must be a list."}, status=400)

    result = BoxSelectionService.recommend_box(items)
    if result["status"] == "error":
        return JsonResponse(result, status=400)
    elif result["status"] == "not_found":
        return JsonResponse(result, status=404)

    return JsonResponse(result, status=200)

@require_http_methods(["GET"])
def list_boxes_view(request):
    boxes = Box.objects.all().order_by('cost')
    payload = [
        {
            "id": b.id,
            "name": b.name,
            "length": float(b.length),
            "width": float(b.width),
            "height": float(b.height),
            "max_weight": float(b.max_weight),
            "cost": float(b.cost),
        }
        for b in boxes
    ]
    return JsonResponse({"boxes": payload}, status=200)