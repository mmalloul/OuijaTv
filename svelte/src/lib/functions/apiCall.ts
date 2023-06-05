import { env } from "$env/dynamic/public";

let falseData: string, cleanString: string;

export async function openApiCall(prompt: string, spirit: number): Promise<string> {
	try {
		const promptEncoded = encodeURIComponent(prompt);
		const spiritEncoded = encodeURIComponent(spirit.toString());

		const url = `${env.PUBLIC_URL}/openai?prompt=${promptEncoded}&spirit=${spiritEncoded}`;

		const response = await fetch(url);
		const data = await response.json();
		const repoData = data.response;
		falseData = repoData.replace(".", "");
		cleanString = cleanupAnswer(falseData);
	} catch (error) {
		console.error("Error:", error);
	}
	return cleanString;
}

function cleanupAnswer(str: string): string {
	const cleanedUpAnswer = str.replace(/\[\[]&]+/g, "");
	return cleanedUpAnswer;
}
