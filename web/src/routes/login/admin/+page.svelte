<script lang="ts">
	import { z } from 'zod';

	let loginParamsSchema = z.object({
		login: z.string(),
		password: z.string()
	});

	type LoginParams = z.infer<typeof loginParamsSchema>;

	let loginParams: LoginParams = $state({
		login: '',
		password: ''
	});
	let isAdmin: boolean = $state(false);

	let invalidCredentialsWarning: HTMLParagraphElement | undefined;

	let promise = $state();
	const onsubmit = (event: Event) => {
		event.preventDefault();
		localStorage.clear();
		if (invalidCredentialsWarning) invalidCredentialsWarning.hidden = true;
		promise = undefined;
		promise = fetch('https://prod-team-35-lg7sic6v.REDACTED/api/admin/secret-url', {
			method: 'POST',
			body: JSON.stringify(loginParams),
			headers: {
				'Content-type': 'application/json; charset=UTF-8'
			}
		}).then(async (response) => {
			let responseBody;
			if (!response.ok) {
				if (response.status === 404 && invalidCredentialsWarning) {
					invalidCredentialsWarning.hidden = false;
				}
				return;
			} else {
				responseBody = await response.json();
				isAdmin = responseBody;
			}

			const token = responseBody.token;
			localStorage.setItem('token', token);
			window.location.href = '/asuy5kjh2i34hk23';
		});
	};
</script>

<h1>Вход в аккаунт администратора</h1>
<form method="POST" {onsubmit}>
	<label for="login">
		Логин
		<input type="text" name="login" id="login" bind:value={loginParams.login} />
	</label>
	<label for="password">
		Пароль
		<input type="password" name="password" id="password" bind:value={loginParams.password} />
	</label>
	<p id="invalid-credentials" bind:this={invalidCredentialsWarning} hidden>
		Неверный логин или пароль
	</p>
	<button type="submit">Войти в аккаунт</button>
</form>
