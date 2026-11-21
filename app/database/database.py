from app.core.config import Settings
from app.database.document.app_indexes.integrity_indexes import integrity_indexes
from app.database.document.app_indexes.lifecycle_indexes import lifecycle_indexes
from app.database.document.app_indexes.query_indexes import query_indexes
from app.repositories.repositories import init_document_repositories, init_relational_repositories


async def init_database(logger, my_app):
    """
        Centralizing databases initialization to avoid conflicts
    """

    if Settings.DATABASE_TYPE == "document":
        from app.database.document.document_db import document_db

        logger.info("Document Database Management System Selected")
        # Check document database activity
        # Throw an error when the connection failed
        try:
            await document_db.client.admin.command("ping")
            logger.info("Database connection established successfully")
        except Exception:
            logger.error("Database connection failed")
            raise

        # Load indexes
        try:
            # await drop_all_indexes(db)
            await integrity_indexes(document_db)
            await lifecycle_indexes(document_db)
            await query_indexes(document_db)
            logger.info("Database indexes initialized")
        except Exception:
            logger.error("Index initialization failed", exc_info=True)
            raise

        init_document_repositories(my_app, document_db)

    elif Settings.DATABASE_TYPE == "relational":
        from app.database.relationnal import relational_db

        logger.info("Relational Database Management System Selected")
        # Check database activity
        # Throw an error when the connection failed
        try:
            await relational_db.init_relational_database()
            logger.info("Database connection established successfully")
            await relational_db.create_tables()
            logger.info("Tables Loaded")
        except Exception:
            logger.error("Database connection failed")
            raise

        init_relational_repositories(my_app)

    else:
        logger.error("Unsupported database type")
        raise Exception("Unsupported database type")
