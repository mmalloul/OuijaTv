import { writable } from "svelte/store";
import toast, { type ToastPosition } from "svelte-french-toast";
import { ToastType } from "$lib/types/ToastType";

/**
 * This store makes it possible to use Toaster in a centralized way, instead of importing the Toaster packages and component separately in each file.
 * Create a toaster easily with given parameters.
 * @param type ToastType -> see ToastType.ts
 * @param msg message that will be shown.
 * @param position change position (default: bottom-center)
 * @param style change style (default: border-radius: 200px; background: #333; color: #fff;)
 */
const showToast = (
	type: ToastType,
	msg: string,
	position = "bottom-center",
	style = "border-radius: 200px; background: #333; color: #fff;"
) => {
	const options = {
		position: position as ToastPosition,
		style
	};

	switch (type) {
		case ToastType.Success:
			toast.success(msg, options);
			break;
		case ToastType.Error:
			toast.error(msg, options);
			break;
	}
};

export const toastStore = writable({
	showToast
});
