import requests

from bs4 import BeautifulSoup

from .exceptions import (
    CSRFTokenNotFoundError, 
    APIRequestError
)
from .enums.emias_urls import (
    EmiasURLs, 
    MethodsPassport
)


class SessionManager:
    def init_session(
            self,
            nano_id: str,
            jwt_token: str = None
        ) -> requests.Session:
        session = requests.Session()
        csrf_token = self.get_csrf_token(session)
        session.headers.update({
            "csrf-token-name": "csrftoken",
            "csrf-token-value": csrf_token,
        })
        if jwt_token is None:
            jwt_token = self.create_anonymous_jwt(nano_id, session)
        session.headers.update({"jwt": jwt_token})
        return session

    def get_csrf_token(self, session: requests.Session) -> str:
        response = session.get(EmiasURLs.HOST.value)
        if response.status_code != 200:
            raise APIRequestError(
                f"Failed request with status code {response.status_code}"
            )
        soup = BeautifulSoup(response.text, "lxml")
        csrf_meta = soup.find('meta', attrs={'name': 'csrf-token-value'})
        if not csrf_meta:
            raise CSRFTokenNotFoundError(
                "CSRF token not found in the response."
            )
        
        return csrf_meta["content"]

    def create_anonymous_jwt(
            self, 
            nano_id: str, 
            session: requests.Session
    ) -> str:
        response = session.post(
            url= EmiasURLs.api_passport_build_url(
                MethodsPassport.CREATE_ANONYMOUS_JWT
            ),
            json= {
                "id": nano_id, 
                "jsonrpc": "2.0", 
                "method": "create_anonymous_jwt"
            }
        )
        if response.status_code != 200:
            raise APIRequestError(
                f"JWT creation failed with status code {response.status_code}"
            )
        return response.json().get("result")

    def process_response(self, response: requests.Response) -> dict:
        if response.status_code != 200:
            raise APIRequestError(
                f"Request failed with status code {response.status_code}"
            )
        data = response.json()
        
        if "error" in data:
            raise APIRequestError(f"API Error: {data['error']}")
        return data.get("result")
