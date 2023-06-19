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
