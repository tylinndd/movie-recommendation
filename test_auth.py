"""
Test script to verify authentication setup
Run this after installing all dependencies
"""

try:
    from main import app, db, User, Watchlist, WatchedList, bcrypt
    print("✅ All imports successful!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nPlease install missing packages:")
    print("pip install Flask-SQLAlchemy Flask-Login Flask-Bcrypt Flask-CORS")
    exit(1)

def test_database():
    """Test database creation and operations"""
    print("\n🔍 Testing database...")
    
    with app.app_context():
        # Create tables
        try:
            db.create_all()
            print("✅ Database tables created successfully!")
        except Exception as e:
            print(f"❌ Database creation failed: {e}")
            return False
        
        # Test user creation
        try:
            # Check if test user exists
            existing_user = User.query.filter_by(username="test_user_123").first()
            if existing_user:
                db.session.delete(existing_user)
                db.session.commit()
            
            hashed_pw = bcrypt.generate_password_hash("testpass123").decode('utf-8')
            test_user = User(
                username="test_user_123",
                email="test@example.com",
                password=hashed_pw
            )
            db.session.add(test_user)
            db.session.commit()
            print("✅ Test user created successfully!")
            
            # Verify password hashing
            if bcrypt.check_password_hash(test_user.password, "testpass123"):
                print("✅ Password hashing and verification working!")
            else:
                print("❌ Password verification failed!")
                return False
            
            # Test watchlist
            test_watchlist_item = Watchlist(
                user_id=test_user.id,
                movie_title="Test Movie",
                movie_data='{"title": "Test Movie"}'
            )
            db.session.add(test_watchlist_item)
            db.session.commit()
            print("✅ Watchlist item created successfully!")
            
            # Test watched list
            test_watched_item = WatchedList(
                user_id=test_user.id,
                movie_title="Watched Movie",
                movie_data='{"title": "Watched Movie"}',
                rating=8.5
            )
            db.session.add(test_watched_item)
            db.session.commit()
            print("✅ Watched list item created successfully!")
            
            # Verify relationships
            user_watchlist = Watchlist.query.filter_by(user_id=test_user.id).all()
            user_watched = WatchedList.query.filter_by(user_id=test_user.id).all()
            
            if len(user_watchlist) == 1 and len(user_watched) == 1:
                print("✅ User relationships working correctly!")
            else:
                print("❌ User relationships not working correctly!")
                return False
            
            # Cleanup
            Watchlist.query.filter_by(user_id=test_user.id).delete()
            WatchedList.query.filter_by(user_id=test_user.id).delete()
            User.query.filter_by(username="test_user_123").delete()
            db.session.commit()
            print("✅ Test data cleaned up successfully!")
            
        except Exception as e:
            print(f"❌ Database operations failed: {e}")
            return False
    
    return True

def test_config():
    """Test Flask configuration"""
    print("\n🔍 Testing Flask configuration...")
    
    if app.config.get('SECRET_KEY'):
        print("✅ SECRET_KEY is configured")
    else:
        print("⚠️  SECRET_KEY not set (using default)")
    
    if app.config.get('SQLALCHEMY_DATABASE_URI'):
        print(f"✅ Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    else:
        print("❌ Database URI not configured")
        return False
    
    return True

def main():
    print("=" * 50)
    print("🎬 Movie Recommendation System - Auth Test")
    print("=" * 50)
    
    # Test configuration
    config_ok = test_config()
    
    # Test database
    db_ok = test_database()
    
    print("\n" + "=" * 50)
    if config_ok and db_ok:
        print("✅ All tests passed!")
        print("\nYou can now run the application:")
        print("  python main.py")
        print("\nThen visit: http://localhost:5000")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    print("=" * 50)

if __name__ == '__main__':
    main()

