from models import User


def get_user_by_email(db, email):

    return db.query(User).filter(
        User.email == email
    ).first()


def get_user_by_mobile(db, mobile):

    return db.query(User).filter(
        User.mobilenumber == mobile
    ).first()


def create_user(db, user):

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_email_login(db, email):

    return db.query(User).filter(
        User.email == email,
    ).first()


def get_user_by_id(db, userid):

    return db.query(User).filter(
        User.userid == userid
    ).first()