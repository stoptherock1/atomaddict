from database.model import app

def create_users(session):
    session.add_all([User(email = 'miles@davis', nickname = 'Miles Davis', password = 'milespass'),
                     User(email = 'john@coltrane', nickname = 'John Coltrane', password = 'coltranepass'),
                     User(email = 'freddie@mercury', nickname = 'Freddie Mercury', password = 'mercurypass'),
                     User(email = 'nick@cave', nickname = 'Nick Cave', password = 'cavepass'),
                     User(email = 'stevieray@vaughan', nickname = 'Stevie Ray Vaughan', password = 'vaughanpass'),
                     User(email = 'tom@waits', nickname = 'Tom Waits', password = 'waitspass'),
                     User(email = 'johnlee@hooker', nickname = 'John Lee Hooker', password = 'hookerpass'),
                     User(email = 'elvis@presley', nickname = 'Elvis Presley', password = 'presleypass')])
    session.commit()


if __name__ == '__main__':
#     app.run(debug=True)
    from database.model import db
    from database.model.models import User, Tag
    from sqlalchemy.orm.session import sessionmaker
    Session = sessionmaker(bind=db.engine)
    session = Session()
    
#     create_users(session=session)
    
    users = session.query(User).all()
    for u in users:
        print u
        
    u = users[0]
    u.articles
    for u in users:
        for i in u.articles:
            print i
        
    
    
    
    

