# cvr get legal unit

This is an implementation of getting and parsing the SOAP data from *get_legal_unit* at Serviceplatformens CVR-Online service.

The module has one siginificant entrypoint: *get_legal_unit*, which is called in the following way:

    data = get_legal_unit(
        certificate="path/to/foces-certificate",
        service_agreenemt="1d41f10c-0f3b-11e9-be4c-0050560112ea",
        user_system="1d41f10c-0f3b-11e9-be4c-0050560112ea",
        user="1d41f10c-0f3b-11e9-be4c-0050560112ea",
        service="c0daecde-e278-43b7-84fd-477bfeeea027"
    )

The returned value is a python dict with data from the significant part of the answer from the online service.

These values are examples illustrating an invocation context acquired from Serviceplatformen, consiting of these 4 uuids. 

The last value 'service' is real.

"service" can be:

* **"93a48b42-3945-11e2-9724-d4bed98c63db"**, corresponding to version 2 of the CVR-Online service
* **"c0daecde-e278-43b7-84fd-477bfeeea027"**, corresponding to version 3 of the CVR-Online service

