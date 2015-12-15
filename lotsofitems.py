from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, SportItem, User

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Robo Barrista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()


# Boxe category
category1 = Category(name="Boxe")

session.add(category1)
session.commit()


sportItem1 = SportItem(name="Boxing Gloves", description="The best just got better with Fighting Sports' new Shock Suppression Gel series with exclusive S2 GEL technology.",
                      category=category1)

session.add(sportItem1)
session.commit()

sportItem2 = SportItem(name="Punching Bag", description="Durable Synthetic Leather shell is very tough and resilient, yet economical.",
                      category=category1)

session.add(sportItem2)
session.commit()

sportItem3 = SportItem(name="Mouthguard", description="A good quality mouthpiece is an important factor in protecting your jaw and alleviating impact",
                      category=category1)

session.add(sportItem3)
session.commit()


# Tennis category
category1 = Category(name="Tennis")

session.add(category1)
session.commit()


sportItem1 = SportItem(name="Tennis ball", description="The Babolat French Open ball will be the official tournament ball for the Roland-Garros.",
                      category=category1)

session.add(sportItem1)
session.commit()

sportItem2 = SportItem(name="Racket", description="This head light racket offers incredible precision and feel.",
                      category=category1)

session.add(sportItem2)
session.commit()


# Skiing category
category1 = Category(name="Skiing")

session.add(category1)
session.commit()


sportItem1 = SportItem(name="Skis", description="Fantastic float and insane stability.",
                      category=category1)

session.add(sportItem1)
session.commit()

sportItem2 = SportItem(name="Ski boot", description="Serious performance uphill and down. ",
                      category=category1)

session.add(sportItem2)
session.commit()




# Swimming category
category1 = Category(name="Swimming")

session.add(category1)
session.commit()


sportItem1 = SportItem(name="Swim goggles", description="The Speed Socket is one of the best competition goggles available",
                      category=category1)

session.add(sportItem1)
session.commit()

sportItem2 = SportItem(name="Swim Caps", description="Speedo's Silicone Swim Cap is the original silicone swim cap.",
                      category=category1)

session.add(sportItem2)
session.commit()

sportItem3 = SportItem(name="Swim Fins", description="Speedo designed the Short Blade Training fin's stiff silicone blade with a slightly larger surface area than the foot, allowing for more resistance and a greater propulsive force. ",
                      category=category1)

session.add(sportItem3)
session.commit()



# Horse riding category
category1 = Category(name="Horse riding")

session.add(category1)
session.commit()


sportItem1 = SportItem(name="Helmet", description="Lightweight, well ventilated, with side glide strap adjustment for a customized and quick-harness fit.",
                      category=category1)

session.add(sportItem1)
session.commit()

sportItem2 = SportItem(name="Rubber Reins", description="This Rubber Reins are designed to enable you keep an easy grip and control over your horse. The reins feature hook stud ends.",
                      category=category1)

session.add(sportItem2)
session.commit()

sportItem3 = SportItem(name="Saddle", description="Drop ring rigging with adjustable straps and chafe guard complete with girth stirrup leather, metal stirrups with vinyl covers, and brass fittings.  5 year tree warranty.",
                      category=category1)

session.add(sportItem3)
session.commit()



print "added sport items!"
