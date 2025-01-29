class RequestBuilder:
    @staticmethod
    def generate(
        method: str,
        jsonrpc: str,
        nano_id: str, 
        birth_date: str, 
        policy_number: str, 
        extra_params: dict = None
    ) -> dict:
        data = {
            "id": nano_id,
            "jsonrpc": jsonrpc,
            "method": method,
            "params": {
                "birthDate": birth_date,
                "omsNumber": policy_number
            }
        }
        if extra_params:
            data["params"].update(extra_params)
        return data
