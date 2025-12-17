#!/usr/bin/env python
#
# Copyright 2020 Eric Gustafson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
import binascii
import io
import pem
import sys

from cryptography import x509
from cryptography.x509 import AuthorityKeyIdentifier
from cryptography.x509 import SubjectKeyIdentifier
from datetime import datetime, timezone

class Cert:
    def __init__(self, pem):
        self.index = ""
        self.auth_index = ""
        self.cert = x509.load_pem_x509_certificate(pem.as_bytes())

    def subject(self):
        return self.cert.subject.rfc4514_string()

    def issuer(self):
        return self.cert.issuer.rfc4514_string()

    def subjectKeyId(self):
        id = None
        try:
            ski = self.cert.extensions.get_extension_for_class(SubjectKeyIdentifier).value
            id = binascii.hexlify(ski.digest,':').decode('utf-8')
        finally:
            return id

    def authorityKeyId(self):
        id = None
        try:
            aki = self.cert.extensions.get_extension_for_class(AuthorityKeyIdentifier).value
            id = binascii.hexlify(aki.key_identifier,':').decode('utf-8')
        finally:
            return id

    def set_index(self, idx):
        self.index = idx

    def set_auth_index(self, idx):
        self.auth_index = idx

    def date_is_valid(self):
        now = datetime.now(timezone.utc)
        if (self.cert.not_valid_after_utc >= now) and (self.cert.not_valid_before_utc) <= now:
            return True
        return False

    def show_date_validity(self):
        if self.date_is_valid():
            return("Valid:  ")
        return("INVALID:")

    def __str__(self):
        out = io.StringIO()
        print("------", file=out)
        print("{:>5}: Subject:  {}".format(self.index, self.subject()), file=out)
        print("       {}  {} <-> {}".format(self.show_date_validity(),
                                               self.cert.not_valid_before_utc,
                                               self.cert.not_valid_after_utc),
                                               file=out)
        print("       Subject Key Identifier:        {}".format(self.subjectKeyId()), file=out)
        print("       Issuer:   {}".format(self.issuer()), file=out)
        authKeyId = self.authorityKeyId()
        if authKeyId:
            if len(self.auth_index) > 0:
                i_index = "({})".format(self.auth_index)
            else:
                i_index = ""
            print("{:>6} Authority Key Identifier:      {}".format(i_index, authKeyId), file=out)
        return out.getvalue()


def trace2(chain, ca):
    cert_index  = {}  # keyed by subject key identifier
    cert_list   = []  # full list of certs (the index drops duplicates)
    print_stack = []  # ordered list of items to print
    print_stack.append("")
    if ca:
        ca_pems = pem.parse(ca.read())
        print_stack.append("CA - loaded {} certificates from {}".format(len(ca_pems), ca.name))
        ii = 0
        for data in ca_pems:
            ii = ii + 1
            idx = "CA-{}".format(ii)
            cert = Cert(data)
            cert.set_index(idx)
            cert_list.append(cert)
            if cert.subjectKeyId() not in cert_index: ## earliest key wins
                cert_index[cert.subjectKeyId()] = cert
            print_stack.append(cert)

    chain_pems = pem.parse(chain.read())
    print_stack.append("loaded {} certificates from {}".format(len(chain_pems), chain.name))
    ii = 0
    for data in chain_pems:
        ii = ii + 1
        idx = "{}".format(ii)
        cert = Cert(data)
        cert.set_index(idx)
        cert_list.append(cert)
        if cert.subjectKeyId() not in cert_index: ## earliest key wins
            cert_index[cert.subjectKeyId()] = cert
        print_stack.append(cert)

    for cert in cert_list:
        auth_key = cert.authorityKeyId()
        if auth_key:
            auth_cert = cert_index.get(auth_key, None)
            if auth_cert:
                cert.set_auth_index(auth_cert.index)

    for entry in print_stack:
        print(entry)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--ca", type=argparse.FileType('rb'))
    parser.add_argument("certs", type=argparse.FileType('rb'))
    return parser.parse_args()


def main():
    args = parse_args()
    trace2(args.certs, args.ca)


if __name__ == "__main__":
    sys.exit(main())

