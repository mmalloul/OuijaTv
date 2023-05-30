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
	{
		name: "solo2",
		route: "solo2"
	}
];

export default items;
