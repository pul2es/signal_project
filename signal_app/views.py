# signal_app/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Signal, UserSignal
from django.utils import timezone
import json

def index(request):
    game_type = request.GET.get('game', 'crash')
    user_id = request.GET.get('user_id')
    bookmaker = request.GET.get('bookmaker')
    language = request.GET.get('lang', 'uz')
    
    context = {
        'game_type': game_type,
        'user_id': user_id,
        'bookmaker': bookmaker,
        'language': language
    }
    return render(request, 'signal_app/index.html', context)

@csrf_exempt
def get_current_signal(request):
    game_type = request.GET.get('game', 'crash')
    current_signal = Signal.objects.filter(
        game_type=game_type,
        is_active=True,
        expires_at__gt=timezone.now()
    ).first()
    
    if current_signal:
        return JsonResponse({
            'value': str(current_signal.value),
            'expires_at': current_signal.expires_at.timestamp()
        })
    return JsonResponse({'value': '0.00', 'expires_at': None})

@csrf_exempt
def save_user_signal(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        signal_id = data.get('signal_id')
        bookmaker = data.get('bookmaker')
        
        UserSignal.objects.create(
            user_id=user_id,
            signal_id=signal_id,
            bookmaker=bookmaker
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)