import pytest
from pyemias.exceptions import InvalidPolicyNumberError
from pyemias.models.auth_model import AuthPolicyData

def test_invalid_policy_number():
    with pytest.raises(InvalidPolicyNumberError) as excinfo:
        AuthPolicyData(policy_number="1234567890", birth_date="1900-01-01")
    assert "Некорректный номер полиса: 1234567890" in str(excinfo.value)