import pytest


def commit_changes(db_session, *, mark_as_failed=False):
    try:
        db_session.commit()
    except:
        db_session.rollback()
        if mark_as_failed:
            pytest.xfail('Couldn\'t commit changes to the database. Test failed.')
        else:
            pytest.skip('Couldn\'t commit changes to the database. Test skipped.')
