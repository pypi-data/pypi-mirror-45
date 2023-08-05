from hs_infra.utils.string_utils import StringUtils


class MobileNumberUtils:
    @classmethod
    def normalize_mobile_number(cls, mobile_number: str) -> str:
        mobile_number = mobile_number.strip()
        mobile_number = StringUtils.digit_to_en(mobile_number)
        while mobile_number.startswith(('0', '+')):
            mobile_number = mobile_number[1:]
        if len(mobile_number) < 11 or len(mobile_number) > 13:
            raise ValueError('mobile number is not correct')
        return mobile_number
