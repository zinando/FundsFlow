from myapp.functions import myfunctions as myfunc
from myapp.models import User


def generate_business_id(business_name: str) -> str:
    """ attaches a random 4-digit code to surname to form userid
        ensures userid is unique
    """
    def generate_random_code():
        """generates random code of 4-digits numbers and attaches it to the first-four letters of the business name"""
        code = myfunc.random_numbers(4)
        userid = "{}_{}".format(business_name.lower()[3:], code)
        if User.query.filter_by(business_id=userid).count() > 0:
            generate_business_id(business_name)
        return userid

    return generate_business_id(business_name)