# signal_app/models.py
from django.db import models
import random

class Signal(models.Model):
    GAME_CHOICES = [
        ('crash', 'Crash'),
        ('aviator', 'Aviator')
    ]
    
    value = models.DecimalField(max_digits=6, decimal_places=2)
    game_type = models.CharField(max_length=10, choices=GAME_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    @classmethod
    def generate_signal(cls, game_type):
        """Generate a new signal with random value"""
        value = round(random.uniform(1.1, 30.0), 2)
        from django.utils import timezone
        import datetime
        expires_at = timezone.now() + datetime.timedelta(seconds=random.randint(10, 20))
        
        return cls.objects.create(
            value=value,
            game_type=game_type,
            expires_at=expires_at
        )

class UserSignal(models.Model):
    user_id = models.BigIntegerField()
    signal = models.ForeignKey(Signal, on_delete=models.CASCADE)
    bookmaker = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user_id', 'signal']