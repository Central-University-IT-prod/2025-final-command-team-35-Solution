<script lang="ts">
	import '../pico.indigo.min.css';
	import '../app.css';
	import type { z } from 'zod';
	import type { userSchema } from '$lib/schemas';
	let { children } = $props();

	type User = z.infer<typeof userSchema>;

	let token: string | null = localStorage.getItem('token');
	let user: User | undefined = $state();
	let isAdmin: boolean | undefined = $state();

	if (token) {
		fetch('https://prod-team-35-lg7sic6v.REDACTED/api/check', {
			method: 'POST',
			headers: {
				authorization: 'Bearer ' + token
			}
		}).then(async (response) => {
			const responseJson = await response.json();

			if (!response.ok || responseJson === false) {
				fetch('https://prod-team-35-lg7sic6v.REDACTED/api/user/profile', {
					method: 'GET',
					headers: {
						authorization: 'Bearer ' + token
					}
				}).then(async (response1) => {
					if (response1.ok) {
						user = await response1.json();
					} else {
						localStorage.removeItem('token');
						window.location.href = '/';
					}
				});
			} else isAdmin = responseJson;
		});
	}
</script>

<header>
	<div class="nav-container">
		<div class="logo">
			<p class="logo-title">MENTORMATCH</p>
		</div>
		<nav>
			{@render links()}
		</nav>
		{#if !isAdmin}
			<a href={user ? '/profile' : '/login'} class="auth-btn">
				<p>{user ? 'Профиль' : 'Авторизация'}</p>
			</a>
		{:else}
			<button
				type="button"
				onclick={() => {
					localStorage.clear();
					window.location.href = '/';
				}}>Выйти</button
			>
		{/if}
	</div>
</header>

<div class="container">
	{@render children()}
</div>

<footer>
	<div class="footer-links">
		{@render links()}
	</div>
</footer>

{#snippet links()}
	<ul>
		<li>
			<a href="/" class="active">Главная</a>
		</li>
		<li>
			<a href="/mentors">Наши менторы</a>
		</li>
		{#if user}
			<li>
				<a href="/mentors/apply">Стать ментором</a>
			</li>
		{/if}
		{#if isAdmin}
			<li>
				<a href="/asuy5kjh2i34hk23">Админ-панель</a>
			</li>
		{/if}
	</ul>
{/snippet}

<style>
	.container {
		margin-top: 1em;
	}

	header {
		display: flex;
		align-items: center;
		margin: 12px 0px;
		justify-content: center;

		transform: scale(1.2);
	}

	.nav-container {
		width: 75%;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.nav-container > button {
		padding: 0 0.25em;
		margin-bottom: 0;
		transform: scale(0.9);
	}

	ul {
		display: flex;
		margin: 4px;
		gap: 1em;
		text-decoration: none;
		padding-inline-start: 0px;
	}

	li {
		list-style: none;
		padding: 0;
	}

	/* // button {
	// 	padding: 0;
	// } */

	p {
		margin: 0;
	}

	a {
		text-decoration: none;
		font-size: 16px;
		font-weight: 400;
	}

	.logo-title {
		font-size: 16px;
		font-weight: 600;
	}

	footer {
		margin-top: 32px;
		display: block;
		justify-content: center;
	}

	.footer-links {
		display: flex;
		gap: 32px;
		justify-content: center;
	}
</style>
