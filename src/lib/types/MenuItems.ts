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
		route: "/profile"
	},
	{
	},
    {
		route: "/game"
		name: "Game",
    },
    {
		name: "Solo",
		route: "/solo"
	},
	{
		name: "Game",
		route: "/game"
	}
];

export default items;
