interface MenuItem {
	name: string;
	route: string;
}

const items: MenuItem[] = [
	{
		name: "Conjure",
		route: "/"
	},
	{
		name: "Solo",
		route: "/solo"
	},
	{
		name: "Browse",
		route: "/browse"
	},
	{
		name: "About Us",
		route: "/about-us"
	},
	{
		name: "Contact",
		route: "/contact"
	}
];

export default items;
