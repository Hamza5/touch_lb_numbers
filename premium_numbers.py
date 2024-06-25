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
        'three_times_code': three_times_code
    }
    other_numbers = sorted(set(numbers) - set(chain(*premium_numbers.values())))
    return premium_numbers, other_numbers
