import structlog

logger = structlog.get_logger()


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Логирование перед обработкой запроса
        logger.info('Processing request', request_path=request.path)

        response = self.get_response(request)

        # Логирование после обработки запроса
        logger.info('Processed request', request_path=request.path, response_status=response.status_code)

        return response
