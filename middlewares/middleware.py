import time

import structlog

logger = structlog.get_logger()


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info('Processing request', request_path=request.path)

        start_time = time.time()

        try:
            response = self.get_response(request)
        except Exception as e:
            logger.error('An error occurred', request_path=request.path, error=str(e))
            raise

        response_time = int((time.time() - start_time) * 1000)

        logger.info(
            'Processed request',
            request_path=request.path,
            response_status=response.status_code,
            response_time=response_time
        )

        return response
