from logger import Logger
import requests
import os

service_health_logger = Logger("services_health.log")


def get_system_health():
    health_status = {}

    # List of services to check
    services = {
        'Service A': os.getenv('SERVICE_A_URL', 'http://service-a/health'),
        'Service B': os.getenv('SERVICE_B_URL', 'http://service-b/health'),
        'Service C': os.getenv('SERVICE_C_URL', 'http://service-c/health'),
    }

    for service_name, url in services.items():
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                health_status[service_name] = {
                    'status': 'up',
                    'message': response.json().get('message', 'Service is running'),
                    'details': None
                }
                service_health_logger.info(
                    f"{service_name} is healthy",
                    {"url": url, "status_code": response.status_code}
                )
            else:
                health_status[service_name] = {
                    'status': 'down',
                    'message': f'Service returned status code {response.status_code}',
                    'details': response.text
                }
                service_health_logger.error(
                    f"{service_name} returned error status",
                    {"url": url, "status_code": response.status_code, "response": response.text}
                )
                
        except requests.exceptions.RequestException as e:
            health_status[service_name] = {
                'status': 'down',
                'message': 'Service unavailable',
                'details': str(e)
            }
            service_health_logger.error(
                f"{service_name} is unreachable",
                {"url": url, "error": str(e)}
            )

    return health_status