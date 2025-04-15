<script lang="ts">
	import { page } from '$app/state';
	import type { mentorSchema } from '$lib/schemas.js';
	import { onMount } from 'svelte';
	import type { z } from 'zod';

	let enrollmentModal: HTMLDialogElement | undefined = $state();

	type Mentor = z.infer<typeof mentorSchema>;

	let mentor: Mentor | undefined = $state();

	onMount(() => {
		fetch(
			'https://prod-team-35-lg7sic6v.REDACTED/api/mentors/' +
				page.url.searchParams.get('mentor_id')
		).then(async (response) => {
			mentor = await response.json();
			console.log(mentor);
		});
	});
</script>

{#if mentor}
	<div class="row">
		<hgroup>
			<h1>{mentor.first_name} {mentor.last_name}</h1>
			{#if mentor.age}
				<b>Возраст:</b> {mentor.age}
			{/if}
		</hgroup>
		<button
			onclick={() => {
				if (enrollmentModal) enrollmentModal.open = true;
			}}>Записаться</button
		>
	</div>
	{#if mentor.about}
		<h3>О себе</h3>
		<p>{mentor.about}</p>
	{/if}
	{#if mentor.direction}
		<h3>Напрвления</h3>
		<p>{mentor.direction}</p>
	{/if}
	{#if mentor.contact}
		<h3>Где со мной связаться</h3>
		<p>{mentor.contact}</p>
	{/if}
{:else}
	<h1>Ментор не был найден</h1>
{/if}

<dialog bind:this={enrollmentModal}>
	<article>
		<header>
			<button
				aria-label="Close"
				rel="prev"
				onclick={() => {
					enrollmentModal!.open = false;
				}}
			></button>
			<p><b>Записаться на сеанс к ментору</b></p>
		</header>
	</article>
</dialog>

<style>
	.row {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
</style>
