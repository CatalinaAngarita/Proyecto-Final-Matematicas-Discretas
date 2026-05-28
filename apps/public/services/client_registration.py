from apps.clients.models import Client


def get_or_create_client(first_name: str, last_name: str, phone: str) -> Client:
    client, created = Client.objects.get_or_create(
        phone=phone,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
        },
    )
    if not created:
        needs_update = False
        if client.first_name != first_name:
            client.first_name = first_name
            needs_update = True
        if client.last_name != last_name:
            client.last_name = last_name
            needs_update = True
        if needs_update:
            client.save(update_fields=['first_name', 'last_name', 'updated_at'])
    return client
