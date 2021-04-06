def deny_transaction(session_instance):
    transactions = session_instance.transaction.filter(status='active')
    for transaction in transactions:
        transaction.status = 'denied'
        transaction.save()
