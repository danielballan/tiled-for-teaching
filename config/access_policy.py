import enum

from tiled.access_policies import NO_ACCESS


R_ACCESS = {"read:metadata", "read:data"}
RW_ACCESS = {"create", "write:metadata", "write:data"} | R_ACCESS


class Role(enum.Enum):
    instructor = "instructor"
    student = "student"


SCOPES_BY_ROLE = {
    Role.instructor: RW_ACCESS,
    Role.student: R_ACCESS,
    None: set(),
}


class AccessPolicy:
    """
    Grant read-write access to instructors and read access to students.
    """

    def __init__(self, *, students, instructors, provider):
        self.provider = provider
        self.students = set(students)
        self.instructors = set(instructors)

    def _get_id(self, principal):
        # Get the id (i.e. username) of this Principal for the
        # associated authentication provider.
        for identity in principal.identities:
            if identity.provider == self.provider:
                id = identity.id
                break
        else:
            raise ValueError(
                f"Principcal {principal} has no identity from "
                f"provider {self.provider}. "
                f"Its identities are: {principal.identities}"
            )
        return id

    def _get_role(self, principal):
        id = self._get_id(principal)
        if id in self.instructors:
            return Role.instructor
        elif id in self.students:
            return Role.student

    def allowed_scopes(self, node, principal):
        role = self._get_role(principal)
        scopes = SCOPES_BY_ROLE[role]
        return scopes

    def filters(self, node, principal, scopes):
        role = self._get_role(principal)
        allowed_scopes = SCOPES_BY_ROLE[role]
        if not scopes.issubset(allowed_scopes):
            return NO_ACCESS
        # Do no filtering;
        # if you can access anything, you can access everything.
        return []
