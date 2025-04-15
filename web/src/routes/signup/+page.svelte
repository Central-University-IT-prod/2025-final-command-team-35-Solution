<script lang="ts">
	import type { userSchema } from '$lib/schemas';
	import { z } from 'zod';

	type User = z.infer<typeof userSchema>;
	let user: User = $state({
		login: '',
		password: '',
		first_name: '',
		last_name: '',
		age: 0,
		about: undefined,
		contact: '',
		is_mentor: false
	});

	let validationErrorWarning: HTMLParagraphElement | undefined = $state();
	let otherErrorWarning: HTMLParagraphElement | undefined = $state();
	let isVerificationWindowShown = $state(false);

	let emailVerificationLink: string = $state('');

	let promise: any = $state();
	const sendForm = (event: Event) => {
		event.preventDefault();
		localStorage.clear();
		if (user.about === '') user.about = undefined;
		promise = undefined;
		promise = fetch('https://prod-team-35-lg7sic6v.REDACTED/api/user/auth/sign-up', {
			method: 'POST',
			body: JSON.stringify(user),
			headers: {
				'Content-type': 'application/json; charset=UTF-8'
			}
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
			emailVerificationLink = (await response.json()).verify_url;

			isVerificationWindowShown = true;
		});
	};
</script>

{#if !isVerificationWindowShown}
	<hgroup>
		<h1>Регистрация пользователя</h1>
		<p>Уже есть аккаунт? <a href="/login">Войдите</a> в него.</p>
	</hgroup>
	<form onsubmit={sendForm}>
		<h3>Личная информация</h3>
		<fieldset class="grid">
			<label for="first-name">
				Имя*
				<input
					type="text"
					name="first-name"
					id="first-name"
					bind:value={user.first_name}
					required
				/>
			</label>
			<label for="last-name">
				Фамилия*
				<input type="text" name="last-name" id="last-name" bind:value={user.last_name} />
			</label>
			<label for="age">
				Возраст*
				<input
					type="number"
					name="age"
					id="age"
					pattern="^(0?[0-9]?[0-9]|1[01][0-9]|120)$"
					bind:value={user.age}
				/>
			</label>
		</fieldset>
		<label for="about">
			<h3>Напишите немного информации о себе</h3>
			<textarea name="about" id="about" bind:value={user.about}></textarea>
		</label>
		<label for="contact">
			<h3>Электронная почта*</h3>
			<input type="email" name="contact" id="contact" bind:value={user.contact} />
		</label>
		<h3>Данные авторизации</h3>
		<fieldset class="grid">
			<label for="login">
				Логин*
				<input type="text" name="login" id="login" bind:value={user.login} required />
			</label>
			<label for="password">
				Пароль*
				<input type="password" name="password" id="password" bind:value={user.password} required />
			</label>
		</fieldset>
		<p id="validation-error-warning" bind:this={validationErrorWarning} hidden></p>
		<p id="other-error-warning" bind:this={otherErrorWarning} hidden></p>
		{#if promise}
			{#await promise}
				<p id="promise-status">Ожидание ответа от сервера</p>
			{:then}
				<p id="promise-status" class="green">Запрос успешно обработан</p>
			{:catch error}
				{#if error.message}
					<p id="promise-status" class="red">Произошла непредвиденная ошибка: {error.message}</p>
				{/if}
				<button type="submit">Повторить завершение регистрации</button>
			{/await}
		{:else}
			<button type="submit">Завершить регистрацию</button>
		{/if}
	</form>
{:else}
	<article>
		<h3>Верификация почты</h3>
		<p>
			Перейдите по ссылке в письме, отправленной вам на почту, указанную в форме регистрации. Если
			не можете найти письмо, проверьте папку «Спам».
		</p>
		<button
			type="button"
			onclick={() => {
				window.location.href = emailVerificationLink;
			}}
		>
			Подтвердить почту
		</button>
	</article>
{/if}

<style>
	fieldset {
		margin-bottom: 0;
	}

	#validation-error-warning {
		padding: 0.5em;
		padding-left: 1em;
		background-color: sandybrown;
		color: black;
		border-radius: 0.25em;
	}
</style>
