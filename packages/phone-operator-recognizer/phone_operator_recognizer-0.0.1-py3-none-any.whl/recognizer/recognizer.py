import re


class PRecognizer(object):
    phone = None
    operators = [
        {
            '0': {'codes': [
                {
                    'value': 29,
                    'digits': [1, 3, 6, 9, ]
                },
                {
                    'value': 44,
                    'digits': '__all__'
                }
            ]},
        },
        {
            '1': {'codes': [
                {
                    'value': 29,
                    'digits': [2, 5, 7, 8, ]
                },
                {
                    'value': 33,
                    'digits': '__all__'
                }
            ]},
        },
        {
            '2': {'codes': [
                {
                    'value': 25,
                    'digits': '__all__'
                }
            ]}
        }
    ]

    operators_name = {
        '0': 'velcom',
        '1': 'МТС',
        '2': 'life:)',
    }

    def __init__(self, phone):
        self.phone = phone

    def parse(self):
        rule = re.compile(r'^\+?[0-9]{3}\s?[0-9]{2}\s?[0-9]{3}\s?[0-9]{2}\s?[0-9]{2}$')

        if rule.search(self.phone):
            return re.sub('[\+\s]', '', self.phone)
        return None

    def get_name(self, key):
        return self.operators_name[key]

    @property
    def detected(self):
        phone = self.parse()

        if phone is None:
            return None

        code, number = str(phone[3:5]), str(phone[5:])

        for operator in self.operators:
            for key, value in operator.items():
                codes = value.get('codes')
                for operator_code in codes:
                    val = operator_code.get('value')
                    digits = operator_code.get('digits')
                    if str(val) == code and isinstance(digits, str):
                        return self.get_name(key)
                    elif str(val) == code and isinstance(digits, list):
                        for digit in digits:
                            if str(digit) == number[0]:
                                return self.get_name(key)
        return None