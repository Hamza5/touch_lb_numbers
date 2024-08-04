from itertools import chain
import re

code = '(?:0?3|70|71|76|78|81)'
phone_number_re = re.compile(rf'^{code}\d{{6}}$')
aab_ccb_re = re.compile(rf'^{code}(\d)\1(\d)(\d)\3\2$')
abb_acc_re = re.compile(rf'^{code}(\d)(\d)\2\1(\d)\3$')
aa_cd_aa_re = re.compile(rf'^{code}(\d)\1(\d)(\d)\1\1$')
z3_ab_xc_ab_re = re.compile(rf'^0?3(\d)(\d)\d\d\1\2$')
ab_ac_ac_re = re.compile(rf'^{code}(\d)(\d)\1(\d)\1\3$')
z3_abc_bbc_re = re.compile(r'^0?3(\d)(\d)(\d)\2\2\3$')
z3_abc_adc_re = re.compile(r'^0?3(\d)(\d)(\d)\1\d\3$')
aba_aca_re = re.compile(rf'^{code}(\d)\d\1\1\d\1$')
xxx_abx_re = re.compile(rf'^{code}(\d)\1\1\d\d\1$')
code_ab_code_ab_re = re.compile(rf'^({code})(\d\d)\1\2$')
z3_70_ab_ac_ad_re = re.compile(r'^(?:0?3|70)(\d)\d\1\d\1\d$')
ab_ac_ab_re = re.compile(rf'^{code}(\d)(\d)\1\d\1\2$')
e1_a1_b1_c1_re = re.compile(r'^81\d1\d1\d1$')
z3_abb_ccd_re = re.compile(r'^0?3(\d)(\d)\2(\d)\3\d$')
z3_aa_bc_xx_re = re.compile(r'^0?3(\d)\1\d\d(\d)\2$')
z3_ab_cc_dd_re = re.compile(r'^0?3\d\d(\d)\1(\d)\2$')
z3_aab_ccd_re = re.compile(r'^0?3(\d)\1\d(\d)\2\d$')
xxx_abc_re = re.compile(rf'^{code}(\d)\1\1\d\d\d$')
z3_aca_bca_re = re.compile(r'^0?3(\d)(\d)\1\d\2\1$')
z3_bca_aca_re = re.compile(r'^0?3\d(\d)(\d)\2\1\2$')
z3_a_cd_cd_x_re = re.compile(r'^0?3\d(\d\d)\1\d$')


def has_digits_ordered_by_one_diff(number, digit_count, ascending=None):
    """
    Check if a number has the specified number of digits ordered by a difference of one.
    :param number: the number to check.
    :param digit_count: the number of digits.
    :param ascending: if True, the digits should be in ascending order, if False, the digits should be in descending
     order. If None, the order doesn't matter.
    :return: True if the number respects the condition, False otherwise.

    :Example:
    >>> has_digits_ordered_by_one_diff(3123450, 5)
    True
    >>> has_digits_ordered_by_one_diff(3123456, 5)
    True
    >>> has_digits_ordered_by_one_diff(312347, 5)
    False
    >>> has_digits_ordered_by_one_diff(5312345, 5)
    True
    >>> has_digits_ordered_by_one_diff(1276543, 5)
    True
    >>> has_digits_ordered_by_one_diff(329261, 5)
    False
    >>> has_digits_ordered_by_one_diff(3123450, 5, ascending=False)
    False
    >>> has_digits_ordered_by_one_diff(3123450, 5, ascending=True)
    True
    >>> has_digits_ordered_by_one_diff(329261, 3)
    False
    >>> has_digits_ordered_by_one_diff(312347, 4)
    True
    >>> has_digits_ordered_by_one_diff(787672, 5)
    False
    >>> has_digits_ordered_by_one_diff(845456, 5)
    False
    >>> has_digits_ordered_by_one_diff(878987, 5)
    False
    """
    number = str(number)
    ordered = False
    if ascending is None:
        return has_digits_ordered_by_one_diff(number, digit_count, ascending=True) or \
                has_digits_ordered_by_one_diff(number, digit_count, ascending=False)
    for i in range(0, len(number) - digit_count + 1):
        if ascending is True:
            ordered = all(int(number[j + 1]) - int(number[j]) == 1 for j in range(i, i + digit_count - 1))
        elif ascending is False:
            ordered = all(int(number[j + 1]) - int(number[j]) == -1 for j in range(i, i + digit_count - 1))
        if ordered:
            break
    return ordered


def diff_by_one_each_two_digits(number):
    """
    Check if the difference between each two digits is one.
    :param number: the number to check.
    :return: True if the difference between each two digits is one, False otherwise.

    :Example:
    >>> diff_by_one_each_two_digits(123456)
    False
    >>> diff_by_one_each_two_digits(767778)
    True
    >>> diff_by_one_each_two_digits(8687888990)
    True
    >>> diff_by_one_each_two_digits(252423)
    True
    >>> diff_by_one_each_two_digits(20191817)
    True
    >>> diff_by_one_each_two_digits(20191816)
    False
    """
    number = str(number)
    return all(abs(int(number[i:i + 2]) - int(number[i + 2: i + 4])) == 1 for i in range(0, len(number) - 3, 2))


def get_premium_numbers(numbers):
    numbers_str = list(map(str, numbers))
    ab_only = [int(number_str) for number_str in numbers_str if phone_number_re.match(number_str)
               and len(set(number_str[-6:])) == 2]
    aab_ccb = [int(number_str) for number_str in numbers_str if aab_ccb_re.match(number_str)]
    abb_acc = [int(number_str) for number_str in numbers_str if abb_acc_re.match(number_str)]
    aa_cd_aa = [int(number_str) for number_str in numbers_str if aa_cd_aa_re.match(number_str)]
    z3_ab_xc_ab = [int(number_str) for number_str in numbers_str if z3_ab_xc_ab_re.match(number_str)]
    ab_ac_ac = [int(number_str) for number_str in numbers_str if ab_ac_ac_re.match(number_str)]
    z3_abc_bbc = [int(number_str) for number_str in numbers_str if z3_abc_bbc_re.match(number_str)]
    z3_abc_adc = [int(number_str) for number_str in numbers_str if z3_abc_adc_re.match(number_str)]
    aba_aca = [int(number_str) for number_str in numbers_str if aba_aca_re.match(number_str)]
    xxx_abx = [int(number_str) for number_str in numbers_str if xxx_abx_re.match(number_str)]
    code_ab_code_ab = [int(number_str) for number_str in numbers_str if code_ab_code_ab_re.match(number_str)]
    z3_70_ab_ac_ad = [int(number_str) for number_str in numbers_str if z3_70_ab_ac_ad_re.match(number_str)]
    ab_ac_ab = [int(number_str) for number_str in numbers_str if ab_ac_ab_re.match(number_str)]
    e1_a1_b1_c1 = [int(number_str) for number_str in numbers_str if e1_a1_b1_c1_re.match(number_str)]
    abc_only = [int(number_str) for number_str in numbers_str if phone_number_re.match(number_str)
                and len(set(number_str[-6:])) == 3]
    z3_abb_ccd = [int(number_str) for number_str in numbers_str if z3_abb_ccd_re.match(number_str)]
    z3_aa_bc_xx = [int(number_str) for number_str in numbers_str if z3_aa_bc_xx_re.match(number_str)]
    z3_ab_cc_dd = [int(number_str) for number_str in numbers_str if z3_ab_cc_dd_re.match(number_str)]
    abc_mod_10 = [int(number_str) for number_str in numbers_str if phone_number_re.match(number_str) and
                  abs(int(number_str[-6:-3]) - int(number_str[-3:])) % 10 == 0 and number_str[-6] == number_str[-3]]
    three_times_code = [int(number_str) for number_str in numbers_str if number_str.count(number_str[:2]) >= 3]
    z3_aab_ccd = [int(number_str) for number_str in numbers_str if z3_aab_ccd_re.match(number_str)]
    xxx_abc = [int(number_str) for number_str in numbers_str if xxx_abc_re.match(number_str)]
    five_digits_ordered = [int(number_str) for number_str in numbers_str if
                           has_digits_ordered_by_one_diff(number_str[-6:], 5, ascending=True) or
                           has_digits_ordered_by_one_diff(number_str[-6:], 5, ascending=False)]
    z3_aca_bca = [int(number_str) for number_str in numbers_str if z3_aca_bca_re.match(number_str)]
    z3_bca_aca = [int(number_str) for number_str in numbers_str if z3_bca_aca_re.match(number_str)]
    z3_a_cd_cd_x = [int(number_str) for number_str in numbers_str if z3_a_cd_cd_x_re.match(number_str)]
    ascending_and_descending = [
        int(number_str) for number_str in numbers_str
        if phone_number_re.match(number_str) and (
                (has_digits_ordered_by_one_diff(number_str[-6:-3], 3, ascending=True) and
                 has_digits_ordered_by_one_diff(number_str[-3:], 3, ascending=False)) or
                (has_digits_ordered_by_one_diff(number_str[-6:-3], 3, ascending=False) and
                 has_digits_ordered_by_one_diff(number_str[-3:], 3, ascending=True))
        )
    ]
    premium_numbers = {
        'ab_only': ab_only,
        'aab_ccb': aab_ccb,
        'abb_acc': abb_acc,
        'aa_cd_aa': aa_cd_aa,
        '03_ab_xc_ab': z3_ab_xc_ab,
        'ab_ac_ac': ab_ac_ac,
        '03_abc_bbc': z3_abc_bbc,
        '03_abc_adc': z3_abc_adc,
        'aba_aca': aba_aca,
        'xxx_abx': xxx_abx,
        'code_ab_code_ab': code_ab_code_ab,
        '03_70_ab_ac_ad': z3_70_ab_ac_ad,
        'ab_ac_ab': ab_ac_ab,
        '81_a1_b1_c1': e1_a1_b1_c1,
        'abc_only': abc_only,
        '03_abb_ccd': z3_abb_ccd,
        '03_aa_bc_xx': z3_aa_bc_xx,
        '03_ab_cc_dd': z3_ab_cc_dd,
        'abc_mod_10': abc_mod_10,
        'three_times_code': three_times_code,
        '03_aab_ccd': z3_aab_ccd,
        'xxx_abc': xxx_abc,
        'five_digits_ordered': five_digits_ordered,
        '03_aca_bca': z3_aca_bca,
        '03_bca_aca': z3_bca_aca,
        '03_a_cd_cd_x': z3_a_cd_cd_x,
        'ascending_and_descending': ascending_and_descending
    }
    other_numbers = sorted(set(numbers) - set(chain(*premium_numbers.values())))
    return premium_numbers, other_numbers
