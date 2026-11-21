from app.core.config import Settings
from app.repositories.document.authentication_repositories.email_validation_code_document_repository import \
    EmailValidationCodeDocumentRepository
from app.repositories.document.authentication_repositories.password_recovery_token_document_repository import \
    PasswordRecoveryTokenDocumentRepository
from app.repositories.document.authentication_repositories.refresh_token_document_repository import \
    RefreshTokenDocumentRepository
from app.repositories.document.authentication_repositories.user_document_repository import UserDocumentRepository
from app.repositories.document.authorization_repositories.permission_document_repository import \
    PermissionDocumentRepository
from app.repositories.document.authorization_repositories.role_document_repository import RoleDocumentRepository
from app.repositories.document.authorization_repositories.role_permission_document_repository import \
    RolePermissionDocumentRepository
from app.repositories.document.authorization_repositories.user_role_document_repository import \
    UserRoleDocumentRepository
from app.repositories.relational.authentication_repositories.email_validation_code_relational_repository import \
    EmailValidationCodeRelationalRepository
from app.repositories.relational.authentication_repositories.password_recovery_token_relational_repository import \
    PasswordRecoveryTokenRelationalRepository
from app.repositories.relational.authentication_repositories.refresh_token_relational_repository import \
    RefreshTokenRelationalRepository
from app.repositories.relational.authentication_repositories.user_relational_repository import UserRelationalRepository
from app.repositories.relational.authorization_repositories.permission_relational_repository import \
    PermissionRelationalRepository
from app.repositories.relational.authorization_repositories.role_permission_relational_repository import \
    RolePermissionRelationalRepository
from app.repositories.relational.authorization_repositories.role_relational_repository import RoleRelationalRepository
from app.repositories.relational.authorization_repositories.user_role_relational_repository import \
    UserRoleRelationalRepository

"""
    Getting repositories through fastapi state
    Now we only return the already created instance of 
    repositories instead of creating them on each request
"""
def _define_authentication_document_repositories(my_app, document_db):
    my_app.state.user_repository = UserDocumentRepository(document_db[Settings.USERS_COLLECTION])
    my_app.state.email_validation_repository = EmailValidationCodeDocumentRepository(document_db[Settings.EMAIL_VALIDATION_CODE_COLLECTION])
    my_app.state.refresh_token_repository = RefreshTokenDocumentRepository(document_db[Settings.REFRESH_TOKENS_COLLECTION])
    my_app.state.password_recovery_token_repository = PasswordRecoveryTokenDocumentRepository(document_db[Settings.PASSWORD_RECOVERY_TOKENS_COLLECTION])

def _define_authentication_relational_repositories(my_app):
    my_app.state.user_repository = UserRelationalRepository(Settings.SQLALCHEMY_METADATA.tables[f"{Settings.USERS_COLLECTION}"])
    my_app.state.email_validation_repository = EmailValidationCodeRelationalRepository(Settings.SQLALCHEMY_METADATA.tables[f"{Settings.EMAIL_VALIDATION_CODE_COLLECTION}"])
    my_app.state.refresh_token_repository = RefreshTokenRelationalRepository(Settings.SQLALCHEMY_METADATA.tables[f"{Settings.REFRESH_TOKENS_COLLECTION}"])
    my_app.state.password_recovery_token_repository = PasswordRecoveryTokenRelationalRepository(Settings.SQLALCHEMY_METADATA.tables[f"{Settings.PASSWORD_RECOVERY_TOKENS_COLLECTION}"])

def _define_authorization_document_repositories(my_app, document_db):
    my_app.state.role_repository = RoleDocumentRepository(document_db[Settings.ROLES_COLLECTION])
    my_app.state.permission_repository = PermissionDocumentRepository(document_db[Settings.PERMISSIONS_COLLECTION])
    my_app.state.role_permission_repository = RolePermissionDocumentRepository(document_db[Settings.ROLE_PERMISSIONS_COLLECTION])
    my_app.state.user_role_repository = UserRoleDocumentRepository(document_db[Settings.USER_ROLES_COLLECTION])

def _define_authorization_relational_repositories(my_app):
    my_app.state.role_repository = RoleRelationalRepository(Settings.SQLALCHEMY_METADATA.tables[f"{Settings.ROLES_COLLECTION}"])
    my_app.state.permission_repository = PermissionRelationalRepository(Settings.SQLALCHEMY_METADATA.tables[f"{Settings.PERMISSIONS_COLLECTION}"])
    my_app.state.role_permission_repository = RolePermissionRelationalRepository(Settings.SQLALCHEMY_METADATA.tables[f"{Settings.ROLE_PERMISSIONS_COLLECTION}"])
    my_app.state.user_role_repository = UserRoleRelationalRepository(Settings.SQLALCHEMY_METADATA.tables[f"{Settings.USER_ROLES_COLLECTION}"])


def init_document_repositories(my_app, document_db):
    _define_authentication_document_repositories(my_app, document_db)
    _define_authorization_document_repositories(my_app, document_db)

def init_relational_repositories(my_app):
    _define_authorization_relational_repositories(my_app)
    _define_authentication_relational_repositories(my_app)