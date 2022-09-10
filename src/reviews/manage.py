import click
import asyncio

from fastapi_users.exceptions import UserAlreadyExists

from adapters.persistence import auth


@click.group()
def manage() -> None:
    return


async def create_user_(email: str, password: str, is_superuser: bool = False):
    try:
        async with auth.get_async_session_context() as session:
            async with auth.get_user_db_context(session) as user_db:
                async with auth.get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        auth.UserCreate(
                            email=email, password=password, is_superuser=is_superuser, is_active=True, is_verified=True
                        )
                    )
                    print(f"User created {user}")
    except UserAlreadyExists:
        print(f"User {email} already exists")

@click.command(help="Creates a new user")
@click.option("--email", required=True, help="User email")
@click.option("--password", required=True, help="User password")
@click.option("--is_superuser", is_flag=True, default=False, help="Create superuser flag")
def create_user(email, password, is_superuser) -> None:
    asyncio.run(create_user_(email, password, is_superuser))

manage.add_command(create_user)


if __name__ == "__main__":
    manage()
