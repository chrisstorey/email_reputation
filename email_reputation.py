import dns.resolver
import uvicorn
from fastapi import FastAPI

email_lookup = FastAPI()

with open("rolebased.txt", "r") as f1:
    roles = [line.rstrip() for line in f1]
    print(roles)

with open("disposable.txt", "r") as f2:
    disposable = [line.rstrip() for line in f2]
    print(disposable)

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']
dns.resolver.default_resolver.timeout = 20


@email_lookup.get("/")
async def root():
    return {"message": "Hello World"}


@email_lookup.get("/rolebased/{email_address}")
async def rolebased(email_address: str):
    email_address_to_search = email_address.split("@", 1)[0]
    for role in roles:
        if email_address_to_search == role:
            return {email_address: "is_role_based"}
    return {"is_role_based": False}


@email_lookup.get("/disposable/{email_address}")
async def disposable(email_address: str):
    email_address_to_search = email_address.split("@", 1)[1]
    for dispose in disposable:
        if email_address_to_search == dispose:
            return {"is_disposable": True}
    return {"is_disposable": False}


@email_lookup.get("/check_mx/{email_address}")
def check_mx(email_address: str):
    print(email_address)
    print(email_address.split("@", 1)[1])
    try:
        response_output = dns.resolver.default_resolver.query(email_address.split("@", 1)[1], 'MX').response.answer[0][
            0].exchange
        return {"MX_Record": "OK", "MX_value": str(response_output)}
    except dns.resolver.NoAnswer:
        return {"MX_record": "No answer"}
    except dns.resolver.Timeout:
        return {"MX_Record": "Timeout"}
    except dns.resolver.NXDOMAIN:
        return {"MX_Record": "DNS name does not exist"}


@email_lookup.get("/check_all/{email_address}")
async def check_all(email_address: str):
    a = (disposable(email_address)
         b = str(rolebased(email_address))
    c = str(check_mx(email_address))
    return {"a": a, "b": b, "c": c}


if __name__ == "__main__":
    uvicorn.run(email_lookup, host="localhost", port=8000)
