interface MenuItem {
    name: string;
    route: string;
}

const items: MenuItem[] = [
    {
        name: "Home",
        route: "/"
    },
    {
        name: "Profile",
        route: "/profile",
    },
    {
        name: "About",
        route: "/about"
    },
    {
        name: "Contacts",
        route: "/contacts"
    }
]

export default items;