<script lang="ts">
	import type { userSchema } from '$lib/schemas';
	import { watch } from 'runed';
	import type { z } from 'zod';

	type User = z.infer<typeof userSchema>;

	let isMentor: boolean | undefined = $state(false);

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
				const responseJson = await response.json();
				user = responseJson;
				isMentor = user?.is_mentor;
			}
		});
	}

	let studentsList: User[] = $state([]);

	watch(
		() => isMentor,
		() => {
			if (!isMentor) {
				window.location.href = '/';
			} else {
				fetch('https://prod-team-35-lg7sic6v.REDACTED/api/mentors/students', {
					method: 'GET',
					headers: {
						authorization: 'Bearer ' + token
					}
				}).then(async (response) => {
					if (response.ok) {
						const responseJson = await response.json();
						studentsList = responseJson;
					}
				});
			}
		}
	);
</script>

<h1>Мои студенты</h1>
{#if isMentor}
	<ul>
		{#each studentsList as student}
			<li>student.</li>
		{/each}
	</ul>
{/if}
