from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import asyncio

from telegram import Bot
from decouple import config

from .models import Task


@shared_task
def send_deadline_reminders():
    now = timezone.now()
    window_end = now + timedelta(hours=1)

    tasks = list(
        Task.objects.filter(
            deadline__gte=now,
            deadline__lte=window_end,
            status=False,
            reminded=False,
            user__telegram_chat_id__isnull=False,
        ).select_related('user')
    )

    if not tasks:
        return

    async def send_all():
        async with Bot(token=config('BOT_TOKEN')) as bot:
            for task in tasks:
                minutes_left = int((task.deadline - now).total_seconds() / 60)
                text = (
                    f'⏰ Reminder: "{task.title}" is due in ~{minutes_left} minute(s).\n'
                    f'Deadline: {task.deadline.strftime("%b %d, %Y · %H:%M")} UTC'
                )
                await bot.send_message(chat_id=task.user.telegram_chat_id, text=text)

    asyncio.run(send_all())

    for task in tasks:
        task.reminded = True
        task.save(update_fields=['reminded'])
