#!/bin/env python
# -*- coding: utf-8 -*-
import os
import string
import random

# Printing colors.
OK_BLUE = '\033[94m'      # [*]
NOTE_GREEN = '\033[92m'   # [+]
FAIL_RED = '\033[91m'     # [-]
WARN_YELLOW = '\033[93m'  # [!]
ENDC = '\033[0m'
PRINT_OK = OK_BLUE + '[*]' + ENDC
PRINT_NOTE = NOTE_GREEN + '[+]' + ENDC
PRINT_FAIL = FAIL_RED + '[-]' + ENDC
PRINT_WARN = WARN_YELLOW + '[!]' + ENDC

# Type of printing.
OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.


# Utility class.
class Utilty:
    def __init__(self):
        return

    # Print metasploit's symbol.
    def print_message(self, type, message):
        if os.name == 'nt':
            if type == NOTE:
                print('[+] ' + message)
            elif type == FAIL:
                print('[-] ' + message)
            elif type == WARNING:
                print('[!] ' + message)
            elif type == NONE:
                print(message)
            else:
                print('[*] ' + message)
        else:
            if type == NOTE:
                print(PRINT_NOTE + ' ' + message)
            elif type == FAIL:
                print(PRINT_FAIL + ' ' + message)
            elif type == WARNING:
                print(PRINT_WARN + ' ' + message)
            elif type == NONE:
                print(NOTE_GREEN + message + ENDC)
            else:
                print(PRINT_OK + ' ' + message)

    # Print exception messages.
    def print_exception(self, e, message):
        self.print_message(WARNING, 'type:{}'.format(type(e)))
        self.print_message(WARNING, 'args:{}'.format(e.args))
        self.print_message(WARNING, '{}'.format(e))
        self.print_message(WARNING, message)

    # Create random string.
    def get_random_token(self, length):
        chars = string.digits + string.ascii_letters
        return ''.join([random.choice(chars) for _ in range(length)])

    # Transform attack_id to attack method's name.
    def transform_attack_method_name(self, attack_id):
        attack_full_name = ''
        if attack_id == 'data_poisoning_fc':
            attack_full_name = 'Feature Collision Attack'
        elif attack_id == 'data_poisoning_cp':
            attack_full_name = 'Convex Polytope Attack'
        elif attack_id == 'data_poisoning_bp':
            attack_full_name = 'Bullseye Polytope Attack'
        elif attack_id == 'model_poisoning_ni':
            attack_full_name = 'Node Injection Attack'
        elif attack_id == 'model_poisoning_mli':
            attack_full_name = 'Malicious Layer Injection Attack'
        elif attack_id == 'evasion_fgsm':
            attack_full_name = 'Fast Gradient Signed Method (FGSM)'
        elif attack_id == 'evasion_cnw':
            attack_full_name = 'Carlini and Wagner L_2 Attack'
        elif attack_id == 'evasion_jsma':
            attack_full_name = 'Jacobian Saliency Map Attack (JSMA)'
        elif attack_id == 'exfiltration_mi':
            attack_full_name = 'Membership Inference Attack'
        elif attack_id == 'exfiltration_lomi':
            attack_full_name = 'Label Only Membership Inference Attack'
        elif attack_id == 'exfiltration_minv':
            attack_full_name = 'Model Inversion Attack'
        else:
            attack_full_name = 'Unknown'
        return attack_full_name

    # Transform rank to integer.
    def transform_rank_to_number(self, rank):
        if rank == 'Secure':
            return 0
        elif rank == 'Normal':
            return 1
        elif rank == 'Weak':
            return 2
        else:
            return 3
