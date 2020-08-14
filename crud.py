"""CRUD Operations!
Function definitions to:
Create, Read, Update, Delete"""

# Importing the model classes from model.py
from model import db, User, Shop, Type, Feature, UserFeature, connect_to_db


#*********************** User related functions ******************************#

def create_user(email, password, home_zipcode):
    """Create a user, add user to db, return user."""

    user = User(email=email, password=password, home_zipcode=home_zipcode)
    db.session.add(user)
    db.session.commit()
    return user


def get_all_users():
    return db.session.query(User).all()


def get_user_by_id(id_num):
    return db.session.query(User).get(id_num)


def get_user_by_email(email):
    return db.session.query(User).filter_by(email=email).first()


#*********************** Shop related functions ******************************#

def create_shop(shop_id, name, lat, lng, address_num=None, address_street=None, zipcode=None):
    """Create a shop, add to db, return shop."""

    shop = Shop(shop_id=shop_id, name=name, address_num=address_num, 
                address_street=address_street, zipcode=zipcode, lat=lat, lng=lng)
    db.session.add(shop)
    db.session.commit()
    return shop


def get_all_shops():
    return db.session.query(Shop).all()


def get_shop_by_id(id_num):
    return db.session.query(Shop).get(id_num)


#*********************** Type related functions ******************************#

def create_type(name):
    """Create a type, add to db, return type."""

    new_type = Type(name=name)
    db.session.add(new_type)
    db.session.commit()
    return new_type


def get_all_types():
    return db.session.query(Type).all()


def get_type_by_id(id_num):
    return db.session.query(Type).get(id_num)


#*********************** Feature related functions ******************************#

def create_feature(name, type, description):
    """Create a feature, add to db, return feature."""

    feature = Feature(name=name, type=type, description=description)
    db.session.add(feature)
    db.session.commit()
    return feature


def get_all_features():
    return db.session.query(Feature).all()


def get_feature_by_id(id_num):
    return db.session.query(Feature).get(id_num)


#*********************** UserFeature related functions ******************************#

def create_user_feature(user, feature, shop, details, last_updated, liked,
                         not_tried=False, ranking=None, nickname=None):
    """Create a user feature, add to db, return user feature."""

    user_feature = UserFeature(user=user, feature=feature, shop=shop, 
                                details=details, nickname=nickname, 
                                not_tried=not_tried, liked=liked, 
                                ranking=ranking, last_updated=last_updated)
    db.session.add(user_feature)
    db.session.commit()
    return user_feature


def get_all_ufs_for_user(user):
    return db.session.query(UserFeature).filter_by(user=user).all()


def get_user_feature_by_id(id_num):
    return db.session.query(UserFeature).get(id_num)


if __name__ == '__main__':
    from server import app
    connect_to_db(app)






