from app.models.user import User
from app.models.repository import Repository

def get(username, name):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return None
    repo = Repository.query.filter_by(owner_id=user.id, name=name).first()
    if repo is None:
        return None
    return repo

def get_by_origin_id(origin_id, imported_from='GitHub'):
    return Repository.query.filter_by(
        origin_id=origin_id,
        imported_from=imported_from
    ).first()
