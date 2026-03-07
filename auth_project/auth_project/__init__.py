from .celery import app as celery_app

# Ye line ensures ki jab Django start ho, toh Celery app load ho jaye.
__all__ = ("celery_app",)