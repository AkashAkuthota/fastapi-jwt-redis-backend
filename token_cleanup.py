from datetime import datetime, timedelta, timezone
import database_models
from database import session



def cleanup_tokens():
    db = session()
    try:
        now = datetime.now(timezone.utc)
        db.query(database_models.RevokedToken).filter(database_models.RevokedToken.expires_at < now).delete(synchronize_session=False)

        db.query(database_models.Refresh_Tokens).filter(database_models.Refresh_Tokens.expires_at < now).delete(synchronize_session=False)

        old_token = now - timedelta(days=1)

        db.query(database_models.Refresh_Tokens).filter(
        database_models.Refresh_Tokens.revoked_at != None,
        database_models.Refresh_Tokens.revoked_at < old_token).delete(synchronize_session=False)
    
        db.commit()
        print(f"Cleanup finished at {now}")
    except Exception as e:
        print(f"cleanup failed:{e}")
        db.rollback()
    finally:
        db.close()

