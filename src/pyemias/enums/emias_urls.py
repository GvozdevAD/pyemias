from enum import Enum


class MethodsEmc(Enum):
    CREATE_APPOINTMENT = "/?createAppointment"
    DIGITAL_PRESCRIPTION = "/?digitalPrescription"
    GET_APPOINTMENT_RECEPTIONS_BY_PATIENT = "/?getAppointmentReceptionsByPatient"
    GET_ASSIGNMENTS_INFO = "/?getAssignmentsInfo"
    GET_AVAILABLE_RESOURCE_SCHEDULE_INFO = "/?getAvailableResourceScheduleInfo"
    GET_LPU_LIST_FOR_SPECIALITY = "/?getLpuListForSpeciality"
    GET_DOCTORS_INFO = "/?getDoctorsInfo"
    GET_PATIENT_INFO3 = "/?getPatientInfo3"
    GET_REFERRALS_INFO = "/?getReferralsInfo"
    GET_SPECIALITIES_INFO = "/?getSpecialitiesInfo"

class MethodsPassport(Enum):
    CREATE_ANONYMOUS_JWT = "/?create_anonymous_jwt"

class EmiasURLs(Enum):
    HOST = "https://emias.info"
    API_EMC_V1 = "/api/emc/appointment-eip/v1"
    API_PASSPORT = "/api/passport/v2"
    API_NOTIFY = "/api/notify/v1/?list_notify"

    @classmethod
    def emc_api_build_url(cls, method: MethodsEmc) -> str:
        return f"{cls.HOST.value}{cls.API_EMC_V1.value}{method.value}"
    
    @classmethod
    def api_passport_build_url(cls, method: MethodsPassport) -> str:
        return f"{cls.HOST.value}{cls.API_PASSPORT.value}{method.value}"