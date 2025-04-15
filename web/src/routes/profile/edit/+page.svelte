<script lang="ts">
	import type { userSchema } from '$lib/schemas';
	import { z } from 'zod';

	const schema = z.object({
		first_name: z.string().optional(),
		last_name: z.string().optional(),
		about: z.string().optional()
	});

	type User = z.infer<typeof userSchema>;
	type Body = z.infer<typeof schema>;

	let body_: Body = $state({});

	let validationErrorWarning: HTMLParagraphElement | undefined = $state();

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
			if (response.ok) {
				user = await response.json();
				body_ = {
					first_name: user?.first_name,
					last_name: user?.last_name,
					about: user?.about
				};
			}
		});
	}

	const onsubmit = (event: Event) => {
		event.preventDefault();
		if (body_.about === '') body_.about = undefined;
		fetch('https://prod-team-35-lg7sic6v.REDACTED/api/user/profile', {
			method: 'PATCH',
			headers: {
				'Content-type': 'application/json; charset=UTF-8',
				authorization: 'Bearer ' + token
			},
			body: JSON.stringify(body_)
		}).then(async (response) => {
			if (!response.ok) {
				const responseJson = await response.json();
				if (response.status === 422 && validationErrorWarning) {
					validationErrorWarning.textContent =
						'Данные некорректны: ' +
						responseJson.detail[0].msg +
						`. Location: (${responseJson.detail[0].loc[1]})`;
					validationErrorWarning.hidden = false;
				}
				throw new Error('');
			}

			window.location.href = '/profile';
		});
	};
</script>

{#if promise}
	{#await promise}
		<h1>Проверка авторизации</h1>
	{:then}
		{#if user}
			<h1>Редактирование аккаунта</h1>
			<form {onsubmit}>
				<div class="row">
					<label for="first-name">
						Имя
						<input type="text" name="first-name" id="first-name" bind:value={body_.first_name} />
					</label>
					<label for="last-name">
						Фамилия
						<input type="text" name="last-name" id="last-name" bind:value={body_.last_name} />
					</label>
				</div>
				<label for="about">
					О себе
					<textarea name="about" id="about" bind:value={body_.about}></textarea>
				</label>

				<p id="validation-error-warning" bind:this={validationErrorWarning} hidden></p>
				<input type="submit" value="Сохранить изменения" />
			</form>
		{/if}
	{/await}
{:else}
	<h1>Вы не вошли в акканут</h1>
	<input
		type="button"
		value="Авторизация"
		onclick={() => {
			window.location.href = '/login';
		}}
	/>
{/if}

<style>
	.row {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 1em;
	}

	.row > * {
		width: 100%;
	}

	#validation-error-warning {
		padding: 0.5em;
		padding-left: 1em;
		background-color: sandybrown;
		color: black;
		border-radius: 0.25em;
	}
</style>
