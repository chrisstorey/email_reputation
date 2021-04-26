import dns.resolver
from fastapi import FastAPI

email_lookup = FastAPI()

with open("rolebased.txt", "r") as f1:
    roles = [line.rstrip() for line in f1]
    print(roles)

with open("disposable.txt", "r") as f2:
    disposable = [line.rstrip() for line in f2]
    print(disposable)

dns.resolver.default_resolver = dns.resolver.Resolver(configure=True)
# dns.resolver.default_resolver.nameservers = ['8.8.8.8']
dns.resolver.default_resolver.timeout = 20


@email_lookup.get("/")
async def root():
    return {"message": "Hello World"}


@email_lookup.get("/rolebased/{email_address}")
async def read_item(email_address: str):
    email_address_to_search = email_address.split("@", 1)[0]
    for role in roles:
        if email_address_to_search == role:
            return {"is_role_based": True}
    return {"is_role_based": False}


@email_lookup.get("/disposable/{email_address}")
async def read_item(email_address: str):
    email_address_to_search = email_address.split("@", 1)[1]
    for dispose in disposable:
        if email_address_to_search == dispose:
            return {"is_disposable": True}
    return {"is_disposable": False}


@email_lookup.get("/check_mx/{email_address}")
async def read_item(email_address: str):
    print(email_address)
    print(email_address.split("@", 1)[1])
    try:
        print("here")
        answers = dns.resolver.default_resolver.resolve(email_address.split("@", 1)[1], 'MX')
        print(answers)
    except dns.resolver.NoAnswer:
        answers = {"MX_record": "No answer"}
    except dns.resolver.Timeout:
        answers = {"MX_Record": "Timeout"}
    else:
        answers = {"MX_Record": "OK"}
    finally:
        print(answers)
        return answers
