import binascii
import logging
import sha3
import uuid
import hmac
from collections import OrderedDict
from hashlib import sha512

import time
from bitcoin import ecdsa_raw_sign

logger = logging.getLogger('ambisafe_tenant')


class Crypt(object):
    def __init__(self, data, private_key):
        self.data = data
        self.private_key = private_key

    def get_recovery_tenant_signatures(self):
        nonce = uuid.uuid4()
        nonce_data = ''.join(['00000000000000000000000000000000',
                              nonce.hex])
        binary_nonce = binascii.unhexlify(nonce_data)
        binary_data = binascii.unhexlify(self.data)
        combined_data = binary_data + binary_nonce
        data_hash = sha3.sha3_256(combined_data).digest().encode('hex')
        v, r, s = ecdsa_raw_sign(data_hash, self.private_key)

        hex_s = hex(s)
        hex_r = hex(r)

        if hex_s.endswith('L'):
            hex_s = hex_s[:-1]
        if hex_r.endswith('L'):
            hex_r = hex_r[:-1]

        # Working around problem where first symbols of r and s could be cut off because of be zeros
        hex_s = '0x' + '0' * (66 - len(hex_s)) + hex_s[2:]
        hex_r = '0x' + '0' * (66 - len(hex_r)) + hex_r[2:]

        return {
            'nonce': str(nonce),
            'r': hex_r,
            's': hex_s,
            'v': int(v)
        }


def nonce():
    return int(time.time())


class HMAC(object):
    def __init__(self, api_key, key_secret, uri, data, nonce=None):
        self.api_key = api_key
        self.key_secret = key_secret
        self._nonce = nonce
        self.data = data
        self.uri = uri
        self._signature = None

    @property
    def nonce(self):
        if not self._nonce:
            self._nonce = nonce()
        return self._nonce

    @property
    def signature(self):
        if not self._signature:
            message = str(self.nonce) + self.api_key + self.uri
            if self.data:
                ordered_data = OrderedDict(sorted(self.data.items()))
                for param in ordered_data:
                    message += str(param) + str(ordered_data[param])
            logger.debug('Secondfactor message: {}'.format(str(message)))
            self._signature = hmac.new(key=self.key_secret.encode('utf-8'),
                                       msg=message.encode('utf-8'),
                                       digestmod=sha512).hexdigest()
            logger.debug('Secondfactor hmac signature: {}'
                         .format(self._signature))
        return self._signature
