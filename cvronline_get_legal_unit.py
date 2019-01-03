""" cvronline-get-legal-unit program """
#
# Copyright (c) 2019, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import requests
import xmltodict
import logging

SOAP_V2 = """\
<?xml version='1.0' encoding='utf-8'?>
<soap-env:Envelope
    xmlns:ns_oio_auth_code="http://rep.oio.dk/cpr.dk/xml/schemas/core/2005/03/18/"
    xmlns:ns_oio_build_ident="http://rep.oio.dk/ebxml/xml/schemas/dkcc/2003/02/13/"
    xmlns:ns_oio_street_and_zip="http://rep.oio.dk/ebxml/xml/schemas/dkcc/2005/03/15/"
    xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/"
>
    <soap-env:Body>
        <ns0:GetLegalUnitRequest
            xmlns:ns0="http://rep.oio.dk/eogs/xml.wsdl/" level="10"
        >
            <ns1:InvocationContext
                xmlns:ns1="http://serviceplatformen.dk/xml/schemas/InvocationContext/1/"
            >
                <ns1:ServiceAgreementUUID>{service_agreement}</ns1:ServiceAgreementUUID>
                <ns1:UserSystemUUID>{user_system}</ns1:UserSystemUUID>
                <ns1:UserUUID>{user}</ns1:UserUUID>
                <ns1:ServiceUUID>{service}</ns1:ServiceUUID>
            </ns1:InvocationContext>
            <ns2:LegalUnitIdentifier
                xmlns:ns2="http://rep.oio.dk/eogs/xml.schema/"
            >{cvrnumber}</ns2:LegalUnitIdentifier>
        </ns0:GetLegalUnitRequest>
    </soap-env:Body>
</soap-env:Envelope>
"""

SOAP_V3 = """\
<?xml version='1.0' encoding='utf-8'?>
<soapenv:Envelope
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:ns="http://rep.oio.dk/eogs/xml/2/"
    xmlns:ns1="http://serviceplatformen.dk/xml/schemas/CallContext/1/"
    xmlns:ns2="http://serviceplatformen.dk/xml/schemas/InvocationContext/1/"
    xmlns:x.="http://rep.oio.dk/eogs/xml.wsdl/"
    xmlns:x.1="http://rep.oio.dk/eogs/xml.schema/"
>
   <soapenv:Header/>
   <soapenv:Body>
      <ns:GetLegalUnitRequest>
         <ns2:InvocationContext>
            <ns2:ServiceAgreementUUID>{service_agreement}</ns2:ServiceAgreementUUID>
            <ns2:UserSystemUUID>{user_system}</ns2:UserSystemUUID>
            <ns2:UserUUID>{user}</ns2:UserUUID>
            <ns2:ServiceUUID>{service}</ns2:ServiceUUID>
         </ns2:InvocationContext>
         <x.:GetLegalUnitRequest level="10">
            <x.1:LegalUnitIdentifier>{cvrnumber}</x.1:LegalUnitIdentifier>
         </x.:GetLegalUnitRequest>
      </ns:GetLegalUnitRequest>
   </soapenv:Body>
</soapenv:Envelope>
"""

logger = logging.getLogger("cvr")


class GetLegalUnitError(Exception):
     pass


def shortkeys(path, key, value):
    if ":" in key:
        return key.split(":")[-1], value
    if key[0] == "@":
        return key.split("@")[-1], value


def parse_response_v2(response):
    result = xmltodict.parse(response.text,
                             process_namespaces=True,
                             postprocessor=shortkeys)
    try:
        return result["Envelope"]["Body"]["GetLegalUnitResponse"]["LegalUnit"]
    except LookupError:
        raise LookupError("Legalunit not found")

def parse_response_v3(response):
    pass



_services = {
    "93a48b42-3945-11e2-9724-d4bed98c63db": {
        "url": "https://prod.serviceplatformen.dk/service/CVROnline/CVROnline/1", # noqa
        "parser": parse_response_v2,
        "soap": SOAP_V2
    },
    "c0daecde-e278-43b7-84fd-477bfeeea027": {
        "url": "https://prod.serviceplatformen.dk/service/CVR/Online/2",
        "parser": parse_response_v3,
        "soap": SOAP_V3
    }
}


def get_legal_unit(certificate, **kwargs):
    _service = _services[kwargs["service"]]
    encoded_xml = _service["soap"].format(**kwargs).encode('utf-8')

    response = requests.post(
        data=encoded_xml,
        url=_service["url"],
        cert=certificate,
    )
    if not response.status_code == requests.status_codes.codes.ok:
        try:
            result = xmltodict.parse(response.text)
            errdesc = " ".join(result["soap:Envelope"]["soap:Body"][
                               "soap:Fault"]["faultstring"].split())
        except Exception as e:
            errdesc = "{status_code} / {exception}".format(
                status_code=str(response.status_code),
                exception=str(e)
            )
        raise GetLegalUnitError(errdesc)
    else:
        return _service["parser"](response)

if __name__ == '__main__':
    import configparser, pprint
    config = configparser.ConfigParser()
    config.read("config.ini")
    config = config["sp_cvr"]
    result = get_legal_unit(**config, cvrnumber="25052943")
    pprint.pprint(result)
