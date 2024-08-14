
# from datetime import timedelta
# from django.utils import timezone
# from blog_api.models import DigitalMarketPost
# from apscheduler.schedulers.background import BackgroundScheduler
# import pytz

# def display(minutes=2):
#     threshold_date = timezone.now() - timedelta(minutes=minutes)
#     try:
#         old_posts = DigitalMarketPost.objects.filter(isDelete__lt=threshold_date, isActivate=False)
#         deleted_count = 0
#         for post in old_posts:
#             print(f"Deleting post created at {post.created_at}, title: {post.title}")
#             post.delete()
#             deleted_count += 1
#     except Exception as e:
#         print(f"Error in display: {str(e)}")

# scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Calcutta'))   
# def start_scheduler():
#     scheduler.add_job(display, 'interval', seconds=30)  # Adjusted to run every minute
#     scheduler.start()
