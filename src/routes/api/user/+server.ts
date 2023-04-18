import type { RequestHandler } from "./$types";
import { User } from "$lib/types/User";

export const GET = (() => {
	return new Response(JSON.stringify(new User("John")));
}) satisfies RequestHandler;
