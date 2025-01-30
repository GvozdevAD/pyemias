from datetime import date
from pydantic import BaseModel, AfterValidator
from typing import Optional
from typing_extensions import Annotated

from ..exceptions import InvalidPolicyNumberError

def validate_policy_number(policy_number: str) -> str:
    if len(policy_number)!=16:
        raise InvalidPolicyNumberError(policy_number)
    return policy_number

class AuthPolicyData(BaseModel):
    policy_number: Annotated[str, AfterValidator(validate_policy_number)]
    birth_date: date
    jwt: Optional[str] = None

