<script lang="ts">
	import type { userSchema } from '$lib/schemas';
	import type { z } from 'zod';

	type User = z.infer<typeof userSchema>;

	let token: string | null = localStorage.getItem('token');
	let user: User | undefined = $state();

	let promise: any = $state();
	if (token) {
		promise = fetch('https://prod-team-35-lg7sic6v.final.prodcontest.ru/api/user/profile', {
			method: 'GET',
			headers: {
				authorization: 'Bearer ' + token
			}
		}).then(async (response) => {
			if (response.ok) user = await response.json();
		});
	}
</script>

{#if promise}
	{#await promise}
		<h1>Проверка авторизации</h1>
	{:then}
		{#if user}
			<h1>{user.first_name} {user.last_name}</h1>
			<h3>Информация об аккаунте</h3>
			<p>
				<b>Имя:</b>
				{user.first_name}
				<br />
				<b>Фамилия:</b>
				{user.last_name}
				<br />
				<b>Возраст:</b>
				{user.age}
				<br />
				<b>Электронная почта:</b>
				{user.contact}
				<br />
				<b>О себе:</b>
				<span class="break-word">{user.about ? user.about : 'Пусто'}</span>
			</p>

			<h3>Управление аккаунтом</h3>
			<input
				type="button"
				value="Редактировать аккаунт"
				onclick={() => {
					window.location.href = '/profile/edit';
				}}
			/>
			<input
				type="button"
				value="Выйти из аккаунта"
				onclick={() => {
					localStorage.clear();
					window.location.href = '/';
				}}
				class="red"
			/>
		{/if}
	{:catch}
		<h1>Что-то пошло не так</h1>
		<input
			type="button"
			value="Повторить проверку"
			onclick={() => {
				window.location.reload();
			}}
		/>
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
	.red {
		background-color: #be3144;
		border: none;
	}

	.break-word {
		word-break: break-all;
	}
</style>
