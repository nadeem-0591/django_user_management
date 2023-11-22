import logging
import time
import json
from datetime import datetime
from django.urls import resolve
from django.contrib.auth import get_user

logger = logging.getLogger(__name__)

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            user = getattr(request, 'user', None) or get_user(request)
        except Exception as e:
            user = None

        # Log the start of the request
        start_time = time.time()
        log_data = {
            "event": "Request Start",
            "method": request.method,
            "path": request.path,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)),
        }

        # Set username based on authentication status
        if user and user.is_authenticated:
            log_data["username"] = user.username
            # Add station_code to log_data if available
            if hasattr(user, 'station') and user.station:
                log_data["station_code"] = user.station.station_name
                log_data["station_ID"] = user.station.station_code
            # Add phone number to log_data if available
            log_data["phone"] = getattr(user, 'phone', None)
        else:
            log_data["username"] = "Anonymous"

        logger.info(json.dumps(log_data))

        response = self.get_response(request)

        # Log the end of the request
        end_time = time.time()
        duration = end_time - start_time
        log_data["event"] = "Request End"
        log_data["status_code"] = response.status_code
        log_data["duration"] = f"{duration:.2f}s"
        log_data["timestamp"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))

        try:
            # Resolve the view function name
            match = resolve(request.path_info)
            if hasattr(match.func, 'view_class'):
                log_data["view_function"] = match.func.view_class.__name__
            else:
                log_data["view_function"] = match.func.__name__
        except AttributeError:
            # If any attribute is missing, log as "Unknown"
            pass

        logger.info(json.dumps(log_data))

        return response
