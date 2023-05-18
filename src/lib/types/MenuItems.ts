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
		name: "Game",
		route: "/game"
	},
	{
		name: "Solo",
		route: "/solo"
	}
];

export default items;
