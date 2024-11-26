export function getUserRole() {
    const token = localStorage.getItem("token");
    const userrole = localStorage.getItem("userrole");

    // Check if token exists and userrole matches expected roles
    if (token && (userrole === "User" || userrole === "Admin" || userrole === "Professional")) {
        return userrole;
    }

    return null; // Return null if there's no token or an unexpected role
}
