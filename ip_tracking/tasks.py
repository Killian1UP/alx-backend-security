from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from .models import RequestLog, SuspiciousIP, BlockedIP


@shared_task
def detect_anomalies():
    """
    Detect suspicious IPs based on request frequency and sensitive paths.
    Runs hourly.
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)

    # 1. Detect IPs with more than 100 requests in the last hour
    ip_counts = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago)
        .values("ip_address")
        .annotate(request_count=Count("id"))
        .order_by("-request_count")
    )

    for entry in ip_counts:
        ip = entry["ip_address"]
        count = entry["request_count"]
        if count > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                reason=f"High traffic: {count} requests in the last hour",
            )
            BlockedIP.objects.get_or_create(ip_address=ip)

    # 2. Detect requests to sensitive paths
    sensitive_paths = ["/admin", "/login"]
    suspicious_logs = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago,
        path__in=sensitive_paths,
    )

    for log in suspicious_logs:
        SuspiciousIP.objects.get_or_create(
            ip_address=log.ip_address,
            reason=f"Accessed sensitive path: {log.path}",
        )
        BlockedIP.objects.get_or_create(ip_address=log.ip_address)
