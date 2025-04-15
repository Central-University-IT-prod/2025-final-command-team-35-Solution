<script lang="ts">
	import type { Snippet } from 'svelte';

	let {
		onclick = () => {
			alert('No function assigned');
		},
		wide,
		square,
		inputSized,
		disableShrinkOnHover,
		autofocus,
		ispositive,
		isnegative,
		isloading,
		disabled,
		children
	}: {
		onclick: (event: MouseEvent) => void;
		backgroundcolor?: string;
		wide?: boolean;
		square?: boolean;
		inputSized?: boolean;
		disableShrinkOnHover?: boolean;
		autofocus?: boolean;
		ispositive?: boolean;
		isnegative?: boolean;
		isloading?: boolean;
		disabled?: boolean;
		children: Snippet;
	} = $props();

	let button: HTMLButtonElement;

	$effect(() => {
		if (isloading) button.classList.add('is-loading');
		else button.classList.remove('is-loading');
	});
</script>

<!-- svelte-ignore a11y_autofocus -->
<button
	type="button"
	class="{ispositive ? 'is-positive' : ''}{isnegative ? 'is-negative' : ''} {disableShrinkOnHover
		? ''
		: 'shrink-on-hover'} {square ? 'square' : ''} {inputSized ? 'input-sized' : ''}"
	style="width: {wide ? '100%' : 'auto'};"
	bind:this={button}
	{autofocus}
	{onclick}
	{disabled}
>
	{@render children()}
</button>

<style>
	:root {
		display: inline-block;
	}

	button {
		display: inline-flex;
		justify-content: center;
		align-items: center;
		gap: 0.5em;

		padding: 0.5em 1em;

		background-color: white;
		border: 1px solid black;
		border-radius: 6px;

		transition: all 0.1s ease-in-out;
	}

	button:hover {
		color: white;
		background-color: black;
		border-color: rgba(0, 0, 0, 255);

		cursor: pointer;
	}

	button:disabled:hover {
		color: black;
		background-color: lightgray;
		border-color: lightgray;

		cursor: not-allowed;
	}

	button.square {
		padding: 0.5em;
	}

	button.input-sized {
		padding: 0.25em;
	}

	.is-positive:hover {
		color: white;
		background-color: #77b254;
		border-color: #77b254;
	}

	.is-negative:hover {
		color: white;
		background-color: #be3144;
		border-color: #be3144;
	}
</style>
