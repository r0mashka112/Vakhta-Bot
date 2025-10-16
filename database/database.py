from sqlalchemy.ext.asyncio import create_async_engine,\
    async_sessionmaker, AsyncSession

class Database:
    def __init__(self, url: str):
        self.engine = create_async_engine(
            url = url
        )

        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit = False,
            class_=AsyncSession
        )

    def get_session(self) -> AsyncSession:
        return self.session_factory()