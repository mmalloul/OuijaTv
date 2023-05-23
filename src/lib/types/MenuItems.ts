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
		route: ""
	},
];

export default items;
