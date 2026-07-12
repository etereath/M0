from validate_contracts import validate_openapi_refs


if __name__ == "__main__":
    validate_openapi_refs()
    print("PASS: OpenAPI parsed and all local references resolve")
