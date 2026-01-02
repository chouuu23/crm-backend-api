from accounts.models import Table

def available_tables(date, time, seats):
    reserved_tables = Table.objects.filter(
        reservations__date=date,
        reservations__time=time
    )

    return Table.objects.filter(
        seats=seats
    ).exclude(
        id__in=reserved_tables.values_list("id", flat=True)
    )
