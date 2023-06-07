try:
    import io
    from io import BytesIO
    from google.cloud import storage
except Exception as e:
    print(e)

storage_client = storage.Client.from_service_account_json('service_account.json')