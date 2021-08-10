CARDGROUP_NAME_ALREADY_EXIST = {
    'status': 'ALREADY_EXIST',
    'constraintName': 'UQ_CARDGROUP_NAME'
}

CLIENT_IS_NULL = {
    'status': 'INCORRECT_PARAMS',
    'errorDesc': 'CLIENT_IS_NULL'
}

CLIENT_DOES_NOT_EXIST = {
    'status': 'INTEGRITY_VIOLATION',
    'constraintName': 'FK_CARDGROUP_CLIENT'
}

NOT_FOUND = {
    'status': 'NOT_FOUND'
}

DIFFERENT_CLIENTS = {
    'status': 'INCORRECT_PARAMS',
    'errorDesc': 'CARD_GROUP_DIFFERENT_CLIENTS'
}

DIFFERENT_CLIENT = {
    'status': 'DIFFERENT_CLIENT'
}

FK_CARDGROUP_PARENT = {
    'constraintName': 'FK_CARDGROUP_PARENT',
    'status': 'INTEGRITY_VIOLATION'
}
