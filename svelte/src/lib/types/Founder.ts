export interface Founder {
	name: string;
	studentNumber: string;
	portrait: string;
}

const founders: Founder[] = [
	{
		name: "Mohammed Malloul",
		studentNumber: "500760524",
		portrait: "src/lib/assets/images/mohammed.png"
	},
	{
		name: "Casper Sluitman",
		studentNumber: "500854999",
		portrait: "src/lib/assets/images/casper.png"
	},
	{
		name: "Kamiel de Visser",
		studentNumber: "500838438",
		portrait: "src/lib/assets/images/kamiel.png"
	},
	{
		name: "Ngoc Ben Nguyen",
		studentNumber: "500831536",
		portrait: "src/lib/assets/images/ben.png"
	},
	{
		name: "Kevin Langbroek ",
		studentNumber: "500847564",
		portrait: "src/lib/assets/images/kevin.png"
	}
];

export default founders;
