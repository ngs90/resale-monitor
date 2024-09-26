from database import UserSubscription, TicketAvailability, Session


def register_user_subscribe(user_psid):
    with Session() as session:
        add_psid = UserSubscription(user_psid=user_psid)
        session.add(add_psid)
        session.commit()
    
def register_user_unsubscribe(user_psid):
    with Session() as session:
        remove_psid = session.query(UserSubscription).filter(UserSubscription.user_psid == user_psid).first()
        if remove_psid:
            session.delete(remove_psid)
            session.commit()

def register_ticket_availability(availability):
    with Session() as session: 
        is_available = TicketAvailability(availability=availability)
        session.add(is_available)
        session.commit()
