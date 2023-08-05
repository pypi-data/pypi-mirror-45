======
fei-ws
======

Wrapper for the federation Equestre Internationale(FEI) Results Provider Web Service.
Works both with and without Django.

Only th new versions of the FEI web services are implemented.
It is known as FEIWSClient.
To use the clients supply your username and password when initializing the object or set FEI_WS_USERNAME and FEI_WS_PASSWORD in django config.
Data is returned, as is. No interpretation except for minor exception handling is used on the responses.
