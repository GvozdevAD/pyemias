from pydantic import BaseModel, ConfigDict
from typing import Optional

class SpecialitiesResponse(BaseModel):
    model_config = ConfigDict(extra='allow')

    code: int
    name: str
    male: bool
    female: bool
    areaType: list
    therapeutic: bool
    isMultipleLpuSpeciality: bool
    isComplaintSpeciality: bool


class Room(BaseModel):
    model_config = ConfigDict(extra='allow')

    id: int
    number: str
    lpuId: int
    lpuShortName: str
    addressPointId: int
    defaultAddress: str
    availabilityDate: str

class ComplexResource(BaseModel):
    model_config = ConfigDict(extra='allow')

    id: int
    name: str
    room: Optional[Room] = None

class ReceptionType(BaseModel):
    model_config = ConfigDict(extra='allow')

    code: str
    name: str
    primary: str
    home: str

class MainDoctor(BaseModel):
    model_config = ConfigDict(extra='allow')

    specialityName: str
    specialityId: int
    firstName: str
    lastName: str
    secondName: Optional[str] = None
    mejiId: int
    employeeId: int

class DoctorsInfoResponse(BaseModel):
    model_config = ConfigDict(extra='allow')
    
    id: int
    lpuId: int
    name: str
    arType: int
    specialityChangeAbility: bool
    arSpecialityId: int
    arSpecialityName: str
    mainDoctor: MainDoctor
    receptionType: list[ReceptionType]
    ldpType: list  
    samplingType: list  
    complexResource: list[ComplexResource]
    district: Optional[bool] = None
    replacement: Optional[bool] = None
    nondistrict: Optional[bool] = None
    availableByReferral: Optional[bool] = None

