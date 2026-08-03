from django.shortcuts import render
import httpx
from django.http import JsonResponse,StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def home(request):
    return render(request, 'home.html')

FASTAPI_URL="http://127.0.0.1:8001"

@csrf_exempt
async def chat(request):
    if request.method=="POST":
        try:
            body = json.loads(request.body.decode('utf-8'))
            query = body.get("query")
            thread_id = body.get("thread_id")
            updated_queries = body.get("updated_query") 
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)

        payload = {
            "query":query,
            "updated_query":updated_queries if updated_queries else None,
            "thread_id":thread_id
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response=await client.post(f"{FASTAPI_URL}/start", json=payload)
            data=response.json()

        if data.get("status")=="pending_review":
            return JsonResponse({
                "status":"pending_review",
                "thread_id":data.get("thread_id"),
                "sub_queries":data.get("sub_query")
            })

        elif data.get("status")=="completed":
            return JsonResponse({
                "status": "completed",
                "thread_id": data.get("thread_id"),
                "output": data.get("Output")
            })

    return render(request,'chat.html')