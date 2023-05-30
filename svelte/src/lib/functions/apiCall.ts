import { env } from "$env/dynamic/public";
let i, a: string;
export async function openApiCall(prompt: string, spirit: number): Promise<string> {
	try {
		const url =
			env.PUBLIC_URL +
			"/openai?prompt=" +
			encodeURIComponent(prompt) +
			"&spirit=" +
			encodeURIComponent(spirit);
		const response = await fetch(url);
		const data = await response.json();
		const awnser1 = data.response;
		i = awnser1.replace(".", "");
		a = cleanupAnswer(i);
	} catch (error) {
		console.error("Error:", error);
	}
	return a;
}

function cleanupAnswer(str: string) {
	const s = str.replace(/\[\[]&]+/g, "");
	return s;
}
