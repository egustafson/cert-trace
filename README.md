x509 Certificate Tracing Tool
=============================

`cert-trace` allows you to input a certificate "chain" PEM and,
optionally, a CA PEM file.  It will show the signing linkage between
the individual certificates in the file(s).

Usage
-----

    usage: cert-trace [-h] [--ca CA] certs

    positional arguments:
      certs

    optional arguments:
      -h, --help  show this help message and exit
      --ca CA

Using the example certificate chain and CA files in this repo:

    > cert-trace spot-elfwerks-org-fullchain.pem --ca identrust-root-ca-x3.pem

    CA - loaded 1 certificates from identrust-root-ca-x3.pem
    ------
     CA-1: Subject:  CN=DST Root CA X3,O=Digital Signature Trust Co.
           Subject Key Identifier:        c4:a7:b1:a4:7b:2c:71:fa:db:e1:4b:90:75:ff:c4:15:60:85:89:10
           Issuer:   CN=DST Root CA X3,O=Digital Signature Trust Co.
           Valid:    2023-03-03 16:00:00+00:00 <-> 2028-03-03 16:00:00+00:00

    loaded 2 certificates from spot-elfwerks-org-fullchain.pem
    ------
        1: Subject:  CN=spot.elfwerks.org
           Subject Key Identifier:        26:90:08:21:ac:45:1a:e2:e1:09:ba:5c:0e:72:2a:e2:95:6b:f9:ac
           Issuer:   CN=Let's Encrypt Authority X3,O=Let's Encrypt,C=US
           Valid:    2023-02-02 16:00:00+00:00 <-> 2025-02-02 16:00:00+00:00
       (2) Authority Key Identifier:      a8:4a:6a:63:04:7d:dd:ba:e6:d1:39:b7:a6:45:65:ef:f3:a8:ec:a1

    ------
        2: Subject:  CN=Let's Encrypt Authority X3,O=Let's Encrypt,C=US
           Subject Key Identifier:        a8:4a:6a:63:04:7d:dd:ba:e6:d1:39:b7:a6:45:65:ef:f3:a8:ec:a1
           Issuer:   CN=DST Root CA X3,O=Digital Signature Trust Co.
           Valid:    2023-01-01 16:00:00+00:00 <-> 2024-01-01 16:00:00+00:00
    (CA-1) Authority Key Identifier:      c4:a7:b1:a4:7b:2c:71:fa:db:e1:4b:90:75:ff:c4:15:60:85:89:10

Note that the CA file is printed first and there is one certificate in
the PEM file which is a self-signed certificate.  The chain file,
which would be presented by the server side of the SSL connection has
two certificates:  1) the host certificate for spot.elfwerks.org, and
2) an intermediate signing certificate from the Let's Encrypt
project.  Finally, the Let's Encrypt, intermediate certificate is
signed by the CA certificate.  See the reference section for citations
that expand on signing chains in more detail.

Providing a CA file is optional.


Installation
------------

Install locally or in a virtual environment:

    > python setup.py develop

Install to the host system:

    > sudo -A python setup.py


Credits
-------

This script is possible because may other people built libraries that
were easy to remix.

1. https://github.com/hynek/pem
2. https://github.com/pyca/cryptography/


Reference
---------

* [Get your certificate chain
  right](https://medium.com/@superseb/get-your-certificate-chain-right-4b117a9c0fce),
  Sebastiaan van Steenis, Aug 2018
* [Certificate Chain
  Example](https://medium.com/two-cents/certificate-chain-example-e37d68c3a3f0),
  Aliaksandr Prysmakou, Dec 2017
* [IdenTrust DST Root CA
  X3](https://www.identrust.com/dst-root-ca-x3), source of the CA used
  in this example.  (expires Sep 2021)
* [spot.elfwerks.org certificate](https://crt.sh/?id=3675961133), the
  source of the host certificate used in this example.
