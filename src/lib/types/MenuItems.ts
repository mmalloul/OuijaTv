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
		name: "Visit",
		route: "/game"
	},
	{
		name: "Solo",
		route: "/solo"
	}
];

export default items;
