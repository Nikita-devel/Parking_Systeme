from fastapi import Request, Depends, HTTPException, status

from src.database.models import Role, User
from src.services.auth import auth_service


class RoleAccess:
    """
    Custom dependency for role-based access control.

    This dependency is used to check if the user has the required role to access
    a particular route.

    Args:
        allowed_roles (list[Role]): A list of roles that are allowed to access the route.

    Raises:
        HTTPException: If the user does not have the required role, a 403 FORBIDDEN status
            exception is raised.

    Example:
        ```python
        # Example usage in a FastAPI route
        @app.get("/admin", dependencies=[Depends(RoleAccess([Role.admin]))])
        async def admin_route():
            return {"message": "Admin access granted"}
        ```
    """
    def __init__(self, allowed_roles: list[Role]):
        """
        Create an instance of RoleAccess.

        :param allowed_roles: List[Role]: The list of roles allowed to access the resource.
        """
        self.allowed_roles = allowed_roles

    async def __call__(
        self, request: Request, user: User = Depends(auth_service.get_current_user)
    ):
        """
        Call method to check if the user has the required role.

        Args:
            request (Request): The FastAPI request.
            user (User): The current authenticated user.

        Raises:
            HTTPException: If the user does not have the required role, a 403 FORBIDDEN status
                exception is raised.
        """
        print(user.role, self.allowed_roles)
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN"
            )
