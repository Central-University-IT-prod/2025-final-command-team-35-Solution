<script lang="ts">
	import type { mentorSchema, userSchema } from '$lib/schemas.js';
	import { onMount } from 'svelte';
	import type { z } from 'zod';

	let mentors: Mentor[] = $state([]);

	type Mentor = z.infer<typeof mentorSchema>;
	type User = z.infer<typeof userSchema>;

	let token: string | null = localStorage.getItem('token');
	let user: User | undefined = $state();

	let promise: any = $state();
	if (token) {
		promise = fetch('https://prod-team-35-lg7sic6v.REDACTED/api/user/profile', {
			method: 'GET',
			headers: {
				authorization: 'Bearer ' + token
			}
		}).then(async (response) => {
			if (response.ok) user = await response.json();
		});
	}

	let modal: HTMLDialogElement | undefined = $state();
	let offers: Array<any> = $state([]);
	let currentOfferIndex: number = $state(-1);

	const enroll = (index: number) => {
		fetch('https://prod-team-35-lg7sic6v.REDACTED/api/mentors/offer', {
			method: 'POST',
			headers: {
				'Content-type': 'application/json; charset=UTF-8',
				authorization: 'Bearer ' + token
			},
			body: JSON.stringify({ mentor_id: mentors[index].mentor_id })
		}).then(async (response) => {
			if (response.ok && modal) {
				const responseJson = await response.json();
				offers.push(responseJson);
				currentOfferIndex++;
				modal.open = true;
			}
		});
	};

	onMount(() => {
		fetch('https://prod-team-35-lg7sic6v.REDACTED/api/mentors').then(
			async (response) => {
				if (!response.ok) {
					throw new Error('fafs');
				}
				mentors = await response.json();
			}
		);
	});
</script>

{#if mentors && mentors.length !== 0}
	<h1>Список доступных менторов</h1>
{:else}
	<h1>На данный момент отсутствуют доступные менторы</h1>
{/if}

<ul>
	{#each mentors as mentor, i}
		<li>
			<div class="row">
				<div>
					<b>{mentor.first_name} {mentor.last_name}</b>
					<p>{mentor.age} лет</p>
					<p>
						<b>О себе:</b> <br />
						<span class="word-break">{mentor.about}</span>
					</p>
				</div>
				<button
					onclick={() => {
						enroll(i);
					}}>Записаться</button
				>
			</div>
		</li>
	{/each}
</ul>

<dialog bind:this={modal}>
	<article>
		<h2>Заявка успешно создана</h2>
		<p>Ожидайте подтверждение ментора.</p>
		<footer>
			<button
				type="button"
				onclick={() => {
					if (modal) modal.open = false;
				}}>Закрыть</button
			>
		</footer>
	</article>
</dialog>

<style>
	ul {
		padding: 1em 0;
	}

	li {
		padding: 0.5em;

		border: 1px solid black;
		border-radius: 0.25em;

		list-style: none;
	}

	p {
		margin-bottom: 0.1em;
	}

	.row {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		gap: 1em;
	}

	.word-break {
		word-break: break-all;
	}
</style>
